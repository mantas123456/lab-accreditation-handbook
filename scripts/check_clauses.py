"""Check that data/clauses.yml, the chapter files and mkdocs.yml agree.

Fails (exit code 1) when:
- a clause in clauses.yml has no chapter file;
- a chapter's front matter names a different clause, or none;
- a chapter marked draft or reviewed is missing one of the standard headings;
- a chapter file in a clause folder is not listed in clauses.yml;
- a chapter is not in the mkdocs.yml navigation.

    python scripts/check_clauses.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CLAUSE_FOLDERS = ("general", "structure", "resources", "process", "management")
HEADINGS = (
    "In one sentence",
    "What an assessor looks for",
    "How to do it in a small lab",
    "Worked example",
    "Common findings",
    "Templates",
    "Tools",
    "Related clauses",
)


def front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) or {} if m else {}


def nav_paths(nav) -> set[str]:
    out: set[str] = set()
    if isinstance(nav, str):
        out.add(nav)
    elif isinstance(nav, list):
        for item in nav:
            out |= nav_paths(item)
    elif isinstance(nav, dict):
        for value in nav.values():
            out |= nav_paths(value)
    return out


def main() -> int:
    data = yaml.safe_load((ROOT / "data" / "clauses.yml").read_text(encoding="utf-8"))
    # mkdocs.yml uses no custom tags, so safe_load is enough.
    nav = nav_paths(yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))["nav"])
    errors: list[str] = []
    listed: set[str] = set()

    for c in data["clauses"]:
        num, chapter = str(c["number"]), c["chapter"]
        listed.add(chapter)
        path = DOCS / chapter
        if not path.exists():
            errors.append(f"clause {num}: chapter file {chapter} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        fm_clause = str(front_matter(text).get("clause", ""))
        if fm_clause != num:
            errors.append(f"{chapter}: front matter clause is {fm_clause or 'missing'}, expected {num}")
        if c["status"] in ("draft", "reviewed"):
            for h in HEADINGS:
                if not re.search(rf"^## {re.escape(h)}\s*$", text, re.M):
                    errors.append(f"{chapter}: status {c['status']} but heading '## {h}' is missing")
        if chapter not in nav:
            errors.append(f"{chapter}: not in the mkdocs.yml nav")

    for folder in CLAUSE_FOLDERS:
        for path in sorted((DOCS / folder).glob("*.md")):
            rel = path.relative_to(DOCS).as_posix()
            if rel not in listed:
                errors.append(f"{rel}: chapter file is not listed in clauses.yml")

    if errors:
        print("Clause check failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Clause check passed: {len(data['clauses'])} clauses, all with chapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
