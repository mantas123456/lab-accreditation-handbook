"""MkDocs hook: builds clause badges, chapter side panels and the clause map
from data/clauses.yml, so they never drift out of step with the chapters.

A chapter opts in with front matter:

    ---
    clause: "7.6"
    ---

A page that contains the line ``<!-- clause-map -->`` gets the full clause
table in its place.
"""

from __future__ import annotations

import html
import posixpath
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

LABQC_DOCS = "https://mantas123456.github.io/lab-quality-toolkit/api/"
LABQC_APP = "https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app/"
TEMPLATES_NOTE = "Downloads arrive in version 0.4."
STATUS_LABEL = {"planned": "Planned", "draft": "Draft", "reviewed": "Reviewed"}

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
    root = Path(config.config_file_path).parent
    _data.update(load_clauses(root))
    return config


def _link(from_page: str, to_doc: str) -> str:
    """Relative Markdown link target from one docs page to another."""
    return posixpath.relpath(to_doc, posixpath.dirname(from_page) or ".")


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
            line += f' · <a href="{LABQC_APP}{e["app"]}">open in the labqc app</a>'
        items.append(f"<li>{line}</li>")
    return items


def _panel(clause: dict, page_path: str) -> str:
    clauses = _data["clauses"]
    status = clause["status"]
    parts = [
        '<aside class="clause-panel" markdown>',
        f'<p class="clause-badge clause-badge--{status}">'
        f'Clause {clause["number"]} · {STATUS_LABEL[status]}</p>',
    ]
    parts.append('<p class="clause-panel__head">Templates</p>')
    if clause["templates"]:
        parts.append("<ul>" + "".join(f"<li>{html.escape(t)}</li>" for t in clause["templates"]) + "</ul>")
        parts.append(f'<p class="clause-panel__note">{TEMPLATES_NOTE}</p>')
    else:
        parts.append('<p class="clause-panel__note">None for this clause.</p>')
    parts.append('<p class="clause-panel__head">Tools</p>')
    if clause["labqc"]:
        parts.append("<ul>" + "".join(_labqc_items(clause["labqc"])) + "</ul>")
    else:
        parts.append('<p class="clause-panel__note">No calculation needed.</p>')
    parts.append('<p class="clause-panel__head">Related clauses</p>')
    parts.append("</aside>")
    related = "\n".join(
        f"- [{r} {clauses[str(r)]['title']}]({_link(page_path, clauses[str(r)]['chapter'])})"
        for r in clause["related"]
    )
    # The related list is Markdown so MkDocs checks the links in --strict builds.
    html_head = "\n".join(parts[:-1])
    return f"{html_head}\n\n{related}\n\n</aside>\n"


def _planned_note(clause: dict) -> str:
    return (
        '!!! note "Planned"\n'
        f"    This chapter is not written yet. It is planned for a later version; "
        f"see the [roadmap]({_link(clause['chapter'], 'roadmap.md')}).\n"
    )


def _clause_map(page_path: str) -> str:
    rows = [
        "| Clause | Topic | Part | Templates | labqc | Status |",
        "|---|---|---|---|---|---|",
    ]
    for c in _data["clauses"].values():
        link = _link(page_path, c["chapter"])
        templates = ", ".join(c["templates"]) or "–"
        tools = ", ".join(f"`{e['ref']}`" for e in c["labqc"]) or "–"
        rows.append(
            f"| {c['number']} | [{c['title']}]({link}) | {c['part']} | {templates} | {tools} "
            f"| {STATUS_LABEL[c['status']]} |"
        )
    return "\n".join(rows)


def on_page_markdown(markdown, page, config, files, **kwargs):
    path = page.file.src_uri
    if "<!-- clause-map -->" in markdown:
        markdown = markdown.replace("<!-- clause-map -->", _clause_map(path))
    number = page.meta.get("clause")
    if number is None:
        return markdown
    clause = _data["clauses"].get(str(number))
    if clause is None:
        raise PluginError(f"{path}: front matter names clause {number}, which is not in clauses.yml")
    if clause["chapter"] != path:
        raise PluginError(f"{path}: clauses.yml says clause {number} lives at {clause['chapter']}")
    insert = _panel(clause, path)
    if clause["status"] == "planned":
        insert += "\n" + _planned_note(clause)
    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: i + 1] + ["", insert] + lines[i + 1 :])
    return insert + "\n" + markdown
