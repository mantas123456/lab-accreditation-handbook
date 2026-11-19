"""Run every ```python block in docs/ and check its printed numbers.

This test is what the "examples-checked" status in data/clauses.yml stands
for: the numbers in those chapters' worked examples are re-run on every build.

Expected output is written as comments in the block itself:

    print(z, classify(z))      # 0.75 satisfactory

    for name, ppm in ...:
        print(name, round(c_ref))
    # A 459
    # B 482

A comment is expected output when it sits at the end of a line of a
print() call, or on whole-comment lines directly below one. Other comments
are explanation and are ignored.

The numbers (and True / False) in the expected output must match the
numbers printed, one for one and in order. Words are not compared. A number
matches when the printed value rounds to it: 0.019 accepts 0.01864, and 459
accepts 459.3.
"""

from __future__ import annotations

import io
import re
import subprocess
import sys
import textwrap
import tokenize
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

FENCE = re.compile(r"^(?P<indent>[ \t]*)```python[^\n]*\n(?P<body>.*?)^(?P=indent)```[ \t]*$", re.M | re.S)
TOKEN = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\w.])|\b(?:True|False)\b")
OFFLINE_MARKER = "without labqc"
OFFLINE_MODULES = {"numpy", "scipy", "math", "statistics"}


def find_blocks() -> list[tuple[str, int, str, bool]]:
    """(page, line, code, offline) for every Python block in docs/."""
    blocks = []
    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for m in FENCE.finditer(text):
            indent = len(m.group("indent"))
            code = textwrap.dedent("\n".join(line[indent:] for line in m.group("body").splitlines()))
            line = text.count("\n", 0, m.start()) + 1
            # Offline blocks sit inside a ??? example "Run it without labqc ..." admonition.
            headers = [h for h in text[: m.start()].splitlines() if re.match(r"\s*(\?\?\?\+?|!!!) ", h)]
            offline = indent > 0 and bool(headers) and OFFLINE_MARKER in headers[-1]
            blocks.append((path.relative_to(DOCS).as_posix(), line, code, offline))
    return blocks


def expected_output(code: str) -> str:
    """The expected-output comments of a block, joined in order."""
    tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    # Every row of a statement that calls print(), so a print() spread over
    # several lines counts as one.
    print_rows: set[int] = set()
    start, has_print = None, False
    for t in tokens:
        if t.type in (tokenize.COMMENT, tokenize.NL, tokenize.INDENT, tokenize.DEDENT):
            continue
        if start is None:
            start = t.start[0]
        has_print |= t.type == tokenize.NAME and t.string == "print"
        if t.type in (tokenize.NEWLINE, tokenize.ENDMARKER):
            if has_print:
                print_rows |= set(range(start, t.start[0] + 1))
            start, has_print = None, False
    comments = {t.start[0]: t.string.lstrip("#").strip() for t in tokens if t.type == tokenize.COMMENT}
    code_rows = {t.start[0] for t in tokens if t.type not in (
        tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER)}
    out, after_print = [], False
    for row in range(1, len(code.splitlines()) + 1):
        if row in print_rows:
            after_print = True
            if row in comments:
                out.append(comments[row])
        elif row in code_rows or row not in comments:
            after_print = False  # other code, or a blank line, ends the expected output
        elif after_print:
            out.append(comments[row])
    return "\n".join(out)


def values(text: str) -> list[str]:
    return TOKEN.findall(text)


def matches(printed: str, expected: str) -> bool:
    if expected in ("True", "False") or printed in ("True", "False"):
        return printed == expected
    decimals = len(expected.split(".")[1]) if "." in expected else 0
    return abs(float(printed) - float(expected)) <= 0.5 * 10**-decimals + 1e-9


BLOCKS = find_blocks()


def test_blocks_found():
    assert BLOCKS, "no ```python blocks found in docs/"


@pytest.mark.parametrize("page,line,code,offline", BLOCKS, ids=[f"{p}:{n}" for p, n, _, _ in BLOCKS])
def test_block_prints_what_its_comments_say(page, line, code, offline):
    expected = values(expected_output(code))
    assert expected, f"{page}:{line}: no expected-output comments with numbers"
    run = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8", cwd=ROOT, timeout=120,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert run.returncode == 0, f"{page}:{line} failed:\n{run.stderr}"
    printed = values(run.stdout)
    assert len(printed) == len(expected), (
        f"{page}:{line}: printed {len(printed)} numbers, comments expect {len(expected)}\n"
        f"printed:\n{run.stdout}\nexpected:\n{expected_output(code)}"
    )
    wrong = [(i, p, e) for i, (p, e) in enumerate(zip(printed, expected)) if not matches(p, e)]
    assert not wrong, f"{page}:{line}: printed vs expected (index, printed, expected): {wrong}\n{run.stdout}"


OFFLINE_BLOCKS = [b for b in BLOCKS if b[3]]


@pytest.mark.parametrize("page,line,code,offline", OFFLINE_BLOCKS, ids=[f"{p}:{n}" for p, n, _, _ in OFFLINE_BLOCKS])
def test_offline_blocks_need_only_numpy_and_scipy(page, line, code, offline):
    imported = set(re.findall(r"^\s*(?:import|from)\s+(\w+)", code, re.M))
    assert imported <= OFFLINE_MODULES, f"{page}:{line} imports {sorted(imported - OFFLINE_MODULES)}"


def test_examples_checked_chapters_have_blocks():
    clauses = yaml.safe_load((ROOT / "data" / "clauses.yml").read_text(encoding="utf-8"))["clauses"]
    pages_with_blocks = {p for p, _, _, _ in BLOCKS}
    for c in clauses:
        if c["status"] == "examples-checked":
            assert c["chapter"] in pages_with_blocks, f"{c['chapter']} is examples-checked but has no Python block"
