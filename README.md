# Lab Accreditation Handbook

[![docs](https://github.com/mantas123456/lab-accreditation-handbook/actions/workflows/docs.yml/badge.svg)](https://github.com/mantas123456/lab-accreditation-handbook/actions/workflows/docs.yml)
[![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey.svg)](LICENSE-docs)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)

**Read it here: https://mantas123456.github.io/lab-accreditation-handbook/**

A free, practical guide to ISO/IEC 17025 accreditation for testing and
calibration labs. One page per clause, each with what an assessor looks
for, practical steps for a small lab, a worked example, common findings,
templates and links to calculation tools.

Calculations link to [labqc](https://github.com/mantas123456/lab-quality-toolkit),
a Python library and web app for uncertainty budgets, method validation,
PT scores and QC charts.

**Status:** version 0.3. Every clause of ISO/IEC 17025:2017 (4.1 to 8.9)
has a draft chapter, plus the Start here guides; templates and tools come
next. See the [roadmap](https://mantas123456.github.io/lab-accreditation-handbook/roadmap/).

> Not official guidance. The handbook never reproduces the text of the
> standard; it cites clause numbers and explains them in its own words. The
> standard and your accreditation body's documents always take priority.

## Build locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve            # live preview at http://127.0.0.1:8000
python scripts/check_clauses.py
mkdocs build --strict   # the same checks CI runs
```

## How it is built

- `data/clauses.yml` is the single source for the clause list: titles,
  chapter paths, templates, labqc links, related clauses and status.
- `hooks/clauses.py` reads it at build time and adds each chapter's clause
  badge and side panel, and the clause map table.
- `docs/_chapter_template.md` is the format every chapter follows.
- `scripts/make_placeholders.py` creates a "Planned" page for any clause
  that has no chapter yet.
- `scripts/check_clauses.py` (run in CI) fails if a clause has no chapter,
  a chapter names the wrong clause, a draft chapter lacks a standard
  heading, or a chapter is missing from the navigation.
- `.github/workflows/docs.yml` builds with `--strict` on every push and
  pull request, and deploys `main` to GitHub Pages.

## Licence

Text and templates: [CC BY 4.0](LICENSE-docs). Code: [MIT](LICENSE).
