"""Create a 'Planned' placeholder page for every clause in data/clauses.yml
whose chapter file does not exist yet. Existing files are never touched.

    python scripts/make_placeholders.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def main() -> None:
    data = yaml.safe_load((ROOT / "data" / "clauses.yml").read_text(encoding="utf-8"))
    made = 0
    for c in data["clauses"]:
        path = DOCS / c["chapter"]
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f'---\nclause: "{c["number"]}"\n---\n\n# {c["number"]} {c["title"]}\n',
            encoding="utf-8",
        )
        made += 1
        print(f"created {path.relative_to(ROOT)}")
    print(f"{made} placeholder(s) created")


if __name__ == "__main__":
    main()
