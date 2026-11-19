"""MkDocs hook: builds clause badges, chapter side panels, the clause map and
the templates library from data/clauses.yml and the template sources, so
they never drift out of step with the chapters.

A chapter opts in with front matter:

    ---
    clause: "7.6"
    ---

Markers replaced on any page:

    <!-- clause-map -->        the full clause table
    <!-- template-library -->  every downloadable template
    <!-- template-count -->    the number of templates in the pack
    <!-- template-pack -->     a button to download every template as one zip
    <!-- templates -->         on a chapter: links to that clause's templates

Before each build, templates whose sources changed are rebuilt into
docs/downloads/ (see scripts/build_templates.py).
"""

from __future__ import annotations

import html
import posixpath
import sys
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_templates  # noqa: E402

LABQC_DOCS = "https://mantas123456.github.io/lab-quality-toolkit/api/"
LABQC_APP = "https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/"
# Status keys must also be defined under extra.status in mkdocs.yml (nav tooltips)
# and have an icon in docs/stylesheets/extra.css.
STATUS_LABEL = {
    "planned": "Planned",
    "draft": "Draft",
    "examples-checked": "Examples checked",
    "reviewed": "Reviewed",
}
FORMAT_LABEL = {"docx": "Word", "xlsx": "Excel"}

_data: dict = {}


def load_clauses(root: Path) -> dict:
    """Read data/clauses.yml and index it by clause number."""
    path = root / "data" / "clauses.yml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    by_number: dict[str, dict] = {}
    for c in raw["clauses"]:
        num = str(c["number"])
        if num in by_number:
            raise PluginError(f"clauses.yml: clause {num} is listed twice")
        if c.get("status") not in STATUS_LABEL:
            raise PluginError(f"clauses.yml: clause {num} has unknown status {c.get('status')!r}")
        by_number[num] = c
    for num, c in by_number.items():
        for rel in c.get("related", []):
            if str(rel) not in by_number:
                raise PluginError(f"clauses.yml: clause {num} relates to unknown clause {rel}")
    return {"edition": raw["edition"], "clauses": by_number}


def on_config(config, **kwargs):
    _data.update(load_clauses(ROOT))
    defined = set((config.extra or {}).get("status") or {})
    missing = sorted(set(STATUS_LABEL) - defined)
    if missing:
        raise PluginError(f"mkdocs.yml: extra.status has no tooltip for {', '.join(missing)}")
    try:
        templates = {t["id"]: t for t in build_templates.catalog()}
    except ValueError as e:
        raise PluginError(str(e)) from e
    for num, c in _data["clauses"].items():
        for tid in c.get("templates", []):
            if tid not in templates:
                raise PluginError(f"clauses.yml: clause {num} names unknown template {tid!r}")
    _data["templates"] = templates
    return config


def on_pre_build(config, **kwargs):
    # Only stale files are rebuilt, and the zip is rewritten only when its
    # content changed, so `mkdocs serve` does not loop on its own output.
    build_templates.build(quiet=True)
    import json

    # Written by build_templates.write_pack(): template count and zip size.
    _data["pack"] = json.loads(build_templates.PACK_DATA.read_text(encoding="utf-8"))


def _size(n: int) -> str:
    return f"{n / 1024 / 1024:.1f} MB" if n >= 1024 * 1024 else f"{round(n / 1024)} KB"


def _pack_button(page_path: str) -> str:
    pack = _data["pack"]
    href = _link(page_path, pack["zip"])
    return (
        f"[Download all {pack['count']} templates (.zip, {_size(pack['bytes'])})]({href})"
        "{ .md-button .md-button--primary }"
    )


def _link(from_page: str, to_doc: str) -> str:
    """Relative link target from one docs page to another file in docs/."""
    return posixpath.relpath(to_doc, posixpath.dirname(from_page) or ".")


def _download(template: dict) -> str:
    return f"downloads/{template['id']}.{template['format']}"


def _clauses_for_template(tid: str) -> list[str]:
    return [num for num, c in _data["clauses"].items() if tid in c.get("templates", [])]


def _labqc_items(entries: list[dict]) -> list[str]:
    items = []
    for e in entries:
        ref = e["ref"]
        module = ref.split(".")[1]
        # anchor: false links to the module page when the function has no
        # entry of its own in the labqc API reference.
        anchor = "" if ref.count(".") == 1 or e.get("anchor") is False else f"#{ref}"
        line = f'<a href="{LABQC_DOCS}{module}/{anchor}"><code>{html.escape(ref)}</code></a>'
        if e.get("app"):
            line += (
                f' · <a href="{LABQC_APP}{e["app"]}">open in the labqc app</a>'
                ' <span class="clause-panel__note">(free; may take about 30 seconds to wake up)</span>'
            )
        items.append(f"<li>{line}</li>")
    return items


def _panel(clause: dict, page_path: str) -> str:
    clauses, templates = _data["clauses"], _data["templates"]
    status = clause["status"]
    parts = [
        '<aside class="clause-panel" markdown>',
        f'<p class="clause-badge clause-badge--{status}">'
        f'Clause {clause["number"]} · {STATUS_LABEL[status]}</p>',
        '<p class="clause-panel__head">Templates</p>',
    ]
    if clause["templates"]:
        # Markdown links, so MkDocs rewrites them for directory URLs and checks them.
        items = "\n".join(
            f"- [{templates[tid]['title']}]({_link(page_path, _download(templates[tid]))}) "
            f"({FORMAT_LABEL[templates[tid]['format']]})"
            for tid in clause["templates"]
        )
        parts.append(f"\n{items}\n")
    else:
        parts.append('<p class="clause-panel__note">None for this clause.</p>')
    parts.append('<p class="clause-panel__head">Tools</p>')
    if clause["labqc"]:
        parts.append("<ul>" + "".join(_labqc_items(clause["labqc"])) + "</ul>")
    else:
        parts.append('<p class="clause-panel__note">No calculation needed.</p>')
    parts.append('<p class="clause-panel__head">Related clauses</p>')
    related = "\n".join(
        f"- [{r} {clauses[str(r)]['title']}]({_link(page_path, clauses[str(r)]['chapter'])})"
        for r in clause["related"]
    )
    # The related list is Markdown so MkDocs checks the links in --strict builds.
    return "\n".join(parts) + f"\n\n{related}\n\n</aside>\n"


def _planned_note(clause: dict) -> str:
    return (
        '!!! note "Planned"\n'
        f"    This chapter is not written yet. It is planned for a later version; "
        f"see the [roadmap]({_link(clause['chapter'], 'roadmap.md')}).\n"
    )


def _chapter_templates(clause: dict, page_path: str) -> str:
    if not clause["templates"]:
        return "No template for this clause."
    lines = []
    for tid in clause["templates"]:
        t = _data["templates"][tid]
        lines.append(
            f"- **[{t['title']}]({_link(page_path, _download(t))})** "
            f"({FORMAT_LABEL[t['format']]}): {t['description']}"
        )
    lines.append("")
    lines.append(f"All templates: [templates library]({_link(page_path, 'template-library/index.md')}).")
    return "\n".join(lines)


def _clause_map(page_path: str) -> str:
    rows = [
        "| Clause | Topic | Part | Templates | labqc | Status |",
        "|---|---|---|---|---|---|",
    ]
    for c in _data["clauses"].values():
        link = _link(page_path, c["chapter"])
        templates = ", ".join(
            f"[{_data['templates'][tid]['title']}]({_link(page_path, _download(_data['templates'][tid]))})"
            for tid in c["templates"]
        ) or "–"
        tools = ", ".join(f"`{e['ref']}`" for e in c["labqc"]) or "–"
        rows.append(
            f"| {c['number']} | [{c['title']}]({link}) | {c['part']} | {templates} | {tools} "
            f"| {STATUS_LABEL[c['status']]} |"
        )
    return "\n".join(rows)


def _template_library(page_path: str) -> str:
    def first_clause(t: dict) -> tuple:
        nums = _clauses_for_template(t["id"])
        if not nums:
            return (99,)
        return tuple(int(x) for x in nums[0].split("."))

    rows = [
        "| Template | Type | Format | Clauses | What it is |",
        "|---|---|---|---|---|",
    ]
    for t in sorted(_data["templates"].values(), key=first_clause):
        clause_links = ", ".join(
            f"[{n}]({_link(page_path, _data['clauses'][n]['chapter'])})" for n in _clauses_for_template(t["id"])
        ) or f"[Start here]({_link(page_path, 'start-here/journey.md')})"
        rows.append(
            f"| **[{t['title']}]({_link(page_path, _download(t))})** | {t['type']} "
            f"| {FORMAT_LABEL[t['format']]} | {clause_links} | {t['description']} |"
        )
    return "\n".join(rows)


def _tool_data(page) -> str:
    """Clause list, gap questions and page-relative chapter links for the browser tools."""
    import json

    questions = yaml.safe_load((ROOT / "data" / "gap_questions.yml").read_text(encoding="utf-8"))
    page_url = page.url or ""
    items = []
    for num, c in _data["clauses"].items():
        target = c["chapter"][: -len(".md")] + "/"
        href = posixpath.relpath(target, page_url or ".") + "/"
        items.append(
            {
                "number": num,
                "title": c["title"],
                "part": c["part"],
                "href": href,
                "questions": questions.get(num, []),
            }
        )
    payload = json.dumps({"edition": _data["edition"], "clauses": items}, ensure_ascii=False)
    # Escape "</" so the JSON cannot close the script element early.
    payload = payload.replace("</", "<\\/")
    return f'<script type="application/json" id="tool-data">{payload}</script>'


def on_page_markdown(markdown, page, config, files, **kwargs):
    path = page.file.src_uri
    if "<!-- tool-data -->" in markdown:
        markdown = markdown.replace("<!-- tool-data -->", _tool_data(page))
    if "<!-- clause-map -->" in markdown:
        markdown = markdown.replace("<!-- clause-map -->", _clause_map(path))
    if "<!-- template-count -->" in markdown:
        markdown = markdown.replace("<!-- template-count -->", str(_data["pack"]["count"]))
    if "<!-- template-pack -->" in markdown:
        markdown = markdown.replace("<!-- template-pack -->", _pack_button(path))
    if "<!-- template-library -->" in markdown:
        markdown = markdown.replace("<!-- template-library -->", _template_library(path))
    if "status" in page.meta:
        raise PluginError(f"{path}: remove 'status' from the front matter; it is set from data/clauses.yml")
    number = page.meta.get("clause")
    if number is None:
        return markdown
    clause = _data["clauses"].get(str(number))
    if clause is None:
        raise PluginError(f"{path}: front matter names clause {number}, which is not in clauses.yml")
    if clause["chapter"] != path:
        raise PluginError(f"{path}: clauses.yml says clause {number} lives at {clause['chapter']}")
    # Material shows page.meta.status as an icon in the navigation, with the
    # tooltip from extra.status in mkdocs.yml.
    page.meta["status"] = clause["status"]
    if "<!-- templates -->" in markdown:
        markdown = markdown.replace("<!-- templates -->", _chapter_templates(clause, path))
    insert = _panel(clause, path)
    if clause["status"] == "planned":
        insert += "\n" + _planned_note(clause)
    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: i + 1] + ["", insert] + lines[i + 1 :])
    return insert + "\n" + markdown
