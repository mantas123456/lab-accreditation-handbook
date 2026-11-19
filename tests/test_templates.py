"""Tests for the template pack: every file builds and opens, every template is
linked from a clause, and the Excel uncertainty budget agrees with labqc."""

from __future__ import annotations

import math
import shutil
import sys
import warnings
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_templates as bt  # noqa: E402


@pytest.fixture(scope="session")
def built():
    bt.build(force=True, quiet=True)
    return bt.catalog()


def test_catalog_not_empty(built):
    assert len(built) >= 20


@pytest.mark.parametrize("fmt", ["docx", "xlsx"])
def test_every_file_opens(built, fmt):
    from docx import Document
    from openpyxl import load_workbook

    items = [t for t in built if t["format"] == fmt]
    assert items, f"no {fmt} templates"
    for t in items:
        path = bt.output_path(t)
        assert path.exists(), path
        if fmt == "docx":
            doc = Document(str(path))
            text = "\n".join(p.text for p in doc.paragraphs)
            assert t["title"] in text, f"{path.name}: title missing"
            assert "CC BY 4.0" in doc.sections[0].footer.paragraphs[0].text
        else:
            wb = load_workbook(str(path))
            assert wb.sheetnames[0] == "About", path.name
            assert wb["About"]["A1"].value == t["title"]
            assert len(wb.sheetnames) >= 2, f"{path.name}: no working sheet"


def test_every_template_linked_from_a_clause(built):
    clauses = yaml.safe_load((ROOT / "data" / "clauses.yml").read_text(encoding="utf-8"))["clauses"]
    used = {tid for c in clauses for tid in c["templates"]}
    ids = {t["id"] for t in built}
    unknown = used - ids
    assert not unknown, f"clauses.yml names templates that do not exist: {sorted(unknown)}"
    standalone = {"pre-assessment-checklist"}  # linked from the Start here pages instead
    orphans = ids - used - standalone
    assert not orphans, f"templates not linked from any clause: {sorted(orphans)}"


def _recalculate(path: Path) -> dict:
    import formulas

    warnings.filterwarnings("ignore")
    model = formulas.ExcelModel().loads(str(path)).finish()
    solution = model.calculate()
    out = {}
    for key, value in solution.items():
        if "!" not in key or ":" in key.split("!")[-1]:
            continue
        sheet = key.split("]")[-1].split("!")[0].strip("'").upper()
        cell = key.split("!")[-1].upper()
        v = value.value[0, 0] if hasattr(value, "value") else value
        out[f"{sheet}!{cell}"] = v
    return out


@pytest.mark.parametrize(
    "file, expected",
    [
        ("risk-register.xlsx", {"REGISTER!G2": 9, "REGISTER!G3": 6, "REGISTER!G4": ""}),
        ("impartiality-risk-register.xlsx", {"REGISTER!F2": 9, "REGISTER!F3": 4}),
        ("pt-plan.xlsx", {"RESULTS!G2": 0.75, "RESULTS!H2": "Satisfactory", "RESULTS!G3": 2.4, "RESULTS!H3": "Questionable"}),
        ("calibration-schedule.xlsx", {"SCHEDULE!H2": 46399}),  # 2026-01-12 + 12 months = 2027-01-12
        ("internal-audit-plan.xlsx", {"PROGRAMME!O2": "Yes", "PROGRAMME!O5": "NO"}),
    ],
)
def test_sheet_formulas_on_examples(built, file, expected):
    got = _recalculate(bt.OUT / file)
    for cell, value in expected.items():
        actual = got[cell]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            assert actual == pytest.approx(value), cell
        else:
            assert actual == value, cell


BUDGETS = {
    "example from chapter 7.6": dict(
        rows=[
            ("Repeatability", 0.071, "normal", None, 1, 10),
            ("Balance", 0.010, "normal", 2, 1, None),
            ("Temperature", 0.05, "rectangular", None, 1, None),
            ("Weighing hot", 0.06, "rectangular", None, 1, None),
            ("Bias", 0.08, "normal", None, 1, 5),
        ],
        value=7.74,
    ),
    "all infinite dof, sensitivities and other distributions": dict(
        rows=[
            ("A", 0.2, "triangular", None, 2.5, None),
            ("B", 0.03, "u-shaped", None, -1, None),
            ("C", 0.5, "normal", 2, 0.1, None),
        ],
        value=12.0,
    ),
}


@pytest.mark.parametrize("case", list(BUDGETS))
def test_uncertainty_budget_matches_labqc(built, tmp_path, case):
    from labqc.uncertainty import Component, combine
    from openpyxl import load_workbook

    spec = BUDGETS[case]
    src = bt.OUT / "uncertainty-budget.xlsx"
    path = tmp_path / "budget.xlsx"
    shutil.copy(src, path)
    wb = load_workbook(str(path))
    ws = wb["Budget"]
    for r in range(bt.UB_FIRST, bt.UB_LAST + 1):
        for col in "ABCDEFG":
            ws[f"{col}{r}"] = None
    for i, (name, value, dist, k, c, dof) in enumerate(spec["rows"]):
        r = bt.UB_FIRST + i
        ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"], ws[f"E{r}"] = name, value, dist, c
        if k is not None:
            ws[f"D{r}"] = k
        if dof is not None:
            ws[f"F{r}"] = dof
    ws[bt.UB_CELLS["value"]] = spec["value"]
    wb.save(str(path))

    got = _recalculate(path)
    cell = lambda key: got[f"BUDGET!{bt.UB_CELLS[key]}"]  # noqa: E731

    expected = combine(
        [
            Component(name, value, dist, k=k or 1.0, sensitivity=c, dof=math.inf if dof is None else dof)
            for name, value, dist, k, c, dof in spec["rows"]
        ],
        value=spec["value"],
    )
    assert cell("u_c") == pytest.approx(expected.combined, rel=1e-9)
    if math.isinf(expected.effective_dof):
        assert cell("v_eff") == "infinite"
        assert cell("k") == pytest.approx(expected.k, rel=1e-9)
    else:
        assert cell("v_eff") == pytest.approx(expected.effective_dof, rel=1e-9)
        # Excel's T.INV.2T truncates the degrees of freedom to a whole number.
        assert cell("k") == pytest.approx(expected.k, abs=0.01)
        assert cell("k") >= expected.k - 1e-9
    assert cell("U") == pytest.approx(cell("k") * expected.combined, rel=1e-9)
    assert cell("U_rel") == pytest.approx(cell("U") / spec["value"], rel=1e-9)


# ---------------------------------------------------------------- template pack (zip)


def test_pack_has_every_template_and_a_readme(built):
    import io
    import json
    import zipfile

    from docx import Document
    from openpyxl import load_workbook

    assert bt.PACK.exists(), bt.PACK
    with zipfile.ZipFile(bt.PACK) as z:
        names = z.namelist()
        expected = sorted(bt.output_path(t).name for t in built)
        assert names == ["README.txt", *expected], names
        for t in built:
            data = io.BytesIO(z.read(bt.output_path(t).name))
            if t["format"] == "docx":
                assert t["title"] in "\n".join(p.text for p in Document(data).paragraphs)
            else:
                assert load_workbook(data)["About"]["A1"].value == t["title"]
        readme = z.read("README.txt").decode("utf-8")
    assert "CC BY 4.0" in readme and "Adapt before use".upper() in readme and bt.SITE in readme
    for name in expected:
        assert name in readme, f"README.txt does not list {name}"
    assert "7.6 Measurement uncertainty" in readme  # clauses come from data/clauses.yml

    info = json.loads(bt.PACK_DATA.read_text(encoding="utf-8"))
    assert info["count"] == len(built)
    assert info["bytes"] == bt.PACK.stat().st_size


def test_pack_is_reproducible(built, tmp_path):
    """Rebuilding unchanged templates gives byte-identical files and zip."""
    for fmt in ("docx", "xlsx"):
        t = next(t for t in built if t["format"] == fmt)
        out = tmp_path / f"again.{fmt}"
        (bt.build_docx if fmt == "docx" else bt.build_xlsx)(t, out)
        bt.normalise_ooxml(out)
        assert out.read_bytes() == bt.output_path(t).read_bytes(), f"{t['id']}.{fmt} differs between builds"
    templates = sorted(built, key=lambda t: bt.output_path(t).name)
    assert bt.pack_bytes(templates) == bt.PACK.read_bytes()
