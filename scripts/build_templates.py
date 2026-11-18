"""Build the downloadable template pack.

    templates/src/<id>.md      forms, procedures, checklists -> docs/downloads/<id>.docx (Pandoc)
    templates/sheets/<id>.yml  registers, plans, budgets     -> docs/downloads/<id>.xlsx (openpyxl)

Each source starts with metadata (Markdown front matter, or top-level YAML keys):

    title:        the name shown on the site and in the file
    type:         SOP, form, checklist, record, register, plan, budget, ...
    description:  one sentence for the templates library

Which clauses a template belongs to is set in data/clauses.yml, not here.

    python scripts/build_templates.py           # rebuild what changed
    python scripts/build_templates.py --force   # rebuild everything
"""

from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "templates" / "src"
SHEETS = ROOT / "templates" / "sheets"
OUT = ROOT / "docs" / "downloads"
REFERENCE_DOCX = ROOT / "templates" / ".build" / "reference.docx"

SITE = "https://mantas123456.github.io/lab-accreditation-handbook/"
FOOTER = (
    "Lab Accreditation Handbook template · CC BY 4.0 · "
    "Not official guidance; the standard and your accreditation body's documents take priority."
)

TEAL = "00796B"
HEADER_FILL = "E0F2F1"
EXAMPLE_FONT_COLOR = "808080"


# ---------------------------------------------------------------- catalogue


def _front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def catalog() -> list[dict]:
    """Every template with its id, title, type, description, format and source path."""
    items = []
    for path in sorted(SRC.glob("*.md")):
        meta = _front_matter(path.read_text(encoding="utf-8"))
        items.append({**_meta(meta, path), "format": "docx", "source": path})
    for path in sorted(SHEETS.glob("*.yml")):
        meta = yaml.safe_load(path.read_text(encoding="utf-8"))
        items.append({**_meta(meta, path), "format": "xlsx", "source": path})
    ids = [t["id"] for t in items]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"template ids used twice: {sorted(dupes)}")
    return items


def _meta(meta: dict, path: Path) -> dict:
    missing = [k for k in ("title", "type", "description") if not meta.get(k)]
    if missing:
        raise ValueError(f"{path.relative_to(ROOT)}: missing {', '.join(missing)}")
    return {"id": path.stem, "title": meta["title"], "type": meta["type"], "description": meta["description"]}


def output_path(template: dict) -> Path:
    return OUT / f"{template['id']}.{template['format']}"


# ---------------------------------------------------------------- Word


def _reference_docx() -> Path:
    """Pandoc's default reference document, restyled once with python-docx."""
    script_time = Path(__file__).stat().st_mtime
    if REFERENCE_DOCX.exists() and REFERENCE_DOCX.stat().st_mtime >= script_time:
        return REFERENCE_DOCX
    import pypandoc
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor

    import subprocess

    REFERENCE_DOCX.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [pypandoc.get_pandoc_path(), "-o", str(REFERENCE_DOCX), "--print-default-data-file", "reference.docx"],
        check=True,
    )

    doc = Document(str(REFERENCE_DOCX))
    styles = doc.styles
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        if name in [s.name for s in styles]:
            f = styles[name].font
            f.name, f.size = "Calibri", Pt(10.5)
    for name, size in (("Title", 20), ("Heading 1", 15), ("Heading 2", 12.5), ("Heading 3", 11)):
        if name in [s.name for s in styles]:
            f = styles[name].font
            f.name, f.size, f.bold = "Calibri", Pt(size), True
            f.color.rgb = RGBColor.from_string(TEAL)
    # Borders on pandoc's "Table" style, so forms print with visible boxes.
    if "Table" in [s.name for s in styles]:
        style_el = styles["Table"].element
        tbl_pr = style_el.find(qn("w:tblPr"))
        if tbl_pr is None:
            tbl_pr = OxmlElement("w:tblPr")
            # tblPr follows pPr/rPr and precedes trPr/tcPr/tblStylePr in a style.
            after = [style_el.find(qn(t)) for t in ("w:trPr", "w:tcPr", "w:tblStylePr")]
            after = [a for a in after if a is not None]
            if after:
                after[0].addprevious(tbl_pr)
            else:
                style_el.append(tbl_pr)
        old = tbl_pr.find(qn("w:tblBorders"))
        if old is not None:
            tbl_pr.remove(old)
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "999999")):
                el.set(qn(k), v)
            borders.append(el)
        # Schema order inside tblPr: ... tblInd, tblBorders, shd, tblLayout, tblCellMar, tblLook.
        later = [tbl_pr.find(qn(t)) for t in ("w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook")]
        later = [x for x in later if x is not None]
        if later:
            later[0].addprevious(borders)
        else:
            tbl_pr.append(borders)
    footer = doc.sections[0].footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.text = FOOTER
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in para.runs:
        run.font.size = Pt(7.5)
        run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    doc.save(str(REFERENCE_DOCX))
    return REFERENCE_DOCX


def build_docx(template: dict, out: Path) -> None:
    import pypandoc

    pypandoc.convert_file(
        str(template["source"]),
        "docx",
        format="markdown",
        outputfile=str(out),
        extra_args=["--reference-doc", str(_reference_docx())],
    )


# ---------------------------------------------------------------- Excel


def _styles():
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    thin = Side(style="thin", color="BBBBBB")
    return {
        "header_font": Font(bold=True, color="FFFFFF"),
        "header_fill": PatternFill("solid", fgColor=TEAL),
        "label_fill": PatternFill("solid", fgColor=HEADER_FILL),
        "border": Border(left=thin, right=thin, top=thin, bottom=thin),
        "wrap": Alignment(wrap_text=True, vertical="top"),
        "example_font": Font(italic=True, color=EXAMPLE_FONT_COLOR),
        "title_font": Font(bold=True, size=14, color=TEAL),
        "bold": Font(bold=True),
    }


def _about_sheet(wb, spec: dict) -> None:
    from openpyxl.styles import Font

    st = _styles()
    ws = wb.create_sheet("About", 0)
    ws.column_dimensions["A"].width = 100
    rows = [(spec["title"], st["title_font"]), (spec["description"], None), ("", None), ("How to use", st["bold"])]
    rows += [(f"• {line}", None) for line in spec.get("instructions", [])]
    rows += [
        ("• Rows in grey italics are examples from a made-up lab. Replace or delete them.", None),
        ("", None),
        (FOOTER, Font(size=8, color="808080")),
        (f"Source and guidance: {SITE}", Font(size=8, color="808080")),
    ]
    for i, (text, font) in enumerate(rows, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        cell.alignment = st["wrap"]
        if font:
            cell.font = font


def _table_sheet(wb, sheet: dict) -> None:
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    st = _styles()
    ws = wb.create_sheet(sheet["name"])
    cols = sheet["columns"]
    n_rows = sheet.get("rows", 50)
    examples = sheet.get("examples", [])
    last = 1 + max(n_rows, len(examples))

    for j, col in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=col["header"])
        cell.font, cell.fill, cell.alignment, cell.border = st["header_font"], st["header_fill"], st["wrap"], st["border"]
        ws.column_dimensions[get_column_letter(j)].width = col.get("width", 16)
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "B2" if sheet.get("freeze_first_column") else "A2"

    for i in range(2, last + 1):
        example = examples[i - 2] if i - 2 < len(examples) else None
        for j, col in enumerate(cols, start=1):
            cell = ws.cell(row=i, column=j)
            cell.border, cell.alignment = st["border"], st["wrap"]
            if "formula" in col:
                cell.value = col["formula"].format(r=i)
            elif example is not None and j - 1 < len(example):
                cell.value = example[j - 1]
            if example is not None:
                cell.font = st["example_font"]
            if col.get("format") == "date":
                cell.number_format = "yyyy-mm-dd"
            elif col.get("format") == "percent":
                cell.number_format = "0%"
            elif col.get("format"):
                cell.number_format = col["format"]

    for j, col in enumerate(cols, start=1):
        letter = get_column_letter(j)
        if col.get("choices"):
            dv = DataValidation(type="list", formula1='"' + ",".join(col["choices"]) + '"', allow_blank=True)
            dv.error, dv.errorTitle = "Choose a value from the list.", "Not in the list"
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{last}")
        if col.get("format") == "date" and "formula" not in col:
            dv = DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True)
            dv.error = "Enter a date, for example 2026-03-14."
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{last}")

    for rule in sheet.get("highlights", []):
        fill = PatternFill("solid", fgColor=rule.get("color", "FFCDD2"))
        rng = f"A2:{get_column_letter(len(cols))}{last}"
        ws.conditional_formatting.add(rng, FormulaRule(formula=[rule["formula"]], fill=fill))

    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{last}"
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToHeight = 0


# Uncertainty budget layout. The tests in tests/ rely on these cells.
UB_FIRST, UB_LAST = 6, 25  # component rows
UB_CELLS = {"value": "C28", "coverage": "C29", "fixed_k": "C30", "u_c": "C32", "v_eff": "C33", "k": "C34", "U": "C35", "U_rel": "C36"}


def _uncertainty_budget(wb, spec: dict) -> None:
    from openpyxl.styles import Font
    from openpyxl.worksheet.datavalidation import DataValidation

    st = _styles()
    ws = wb.create_sheet("Budget")
    ws["A1"] = "Uncertainty budget"
    ws["A1"].font = st["title_font"]
    ws["A2"] = "Measurand:"
    ws["B2"] = "e.g. Moisture content of wood pellets as received, % (m/m), oven drying at 105 °C"
    ws["B2"].font = st["example_font"]
    ws["A3"] = "Method, version, date, prepared by:"
    headers = [
        ("Source of uncertainty", 34), ("Value", 10), ("Distribution", 13), ("k (normal only)", 9),
        ("Sensitivity c", 10), ("Degrees of freedom (blank = infinite)", 13), ("Unit", 9),
        ("Divisor", 9), ("Standard uncertainty u", 12), ("Contribution |c|·u", 12),
        ("Share of variance", 10), ("Welch–Satterthwaite term", 12),
    ]
    from openpyxl.utils import get_column_letter

    for j, (h, w) in enumerate(headers, start=1):
        c = ws.cell(row=5, column=j, value=h)
        c.font, c.fill, c.alignment, c.border = st["header_font"], st["header_fill"], st["wrap"], st["border"]
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[5].height = 45
    ws.freeze_panes = "B6"

    examples = spec.get("examples", [])
    for r in range(UB_FIRST, UB_LAST + 1):
        ex = examples[r - UB_FIRST] if r - UB_FIRST < len(examples) else None
        if ex:
            for j, v in enumerate(ex, start=1):
                ws.cell(row=r, column=j, value=v).font = st["example_font"]
        ws[f"H{r}"] = (
            f'=IF(A{r}="","",IF(C{r}="normal",IF(D{r}="",1,D{r}),IF(C{r}="rectangular",SQRT(3),'
            f'IF(C{r}="triangular",SQRT(6),IF(C{r}="u-shaped",SQRT(2),NA())))))'
        )
        ws[f"I{r}"] = f'=IF(A{r}="","",ABS(B{r})/H{r})'
        ws[f"J{r}"] = f'=IF(A{r}="","",ABS(IF(E{r}="",1,E{r}))*I{r})'
        ws[f"K{r}"] = f'=IF(A{r}="","",J{r}^2/{UB_CELLS["u_c"]}^2)'
        ws[f"L{r}"] = f'=IF(OR(A{r}="",F{r}=""),0,J{r}^4/F{r})'
        for j in range(1, 13):
            cell = ws.cell(row=r, column=j)
            cell.border = st["border"]
            if j >= 8:
                cell.fill = st["label_fill"]
        ws[f"I{r}"].number_format = ws[f"J{r}"].number_format = "0.0000"
        ws[f"K{r}"].number_format = "0.0%"

    dv = DataValidation(type="list", formula1='"normal,rectangular,triangular,u-shaped"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"C{UB_FIRST}:C{UB_LAST}")

    rng = lambda col: f"{col}{UB_FIRST}:{col}{UB_LAST}"  # noqa: E731
    summary = [
        ("value", "Result y (needed only for the relative uncertainty)", spec.get("example_value")),
        ("coverage", "Coverage probability", 0.95),
        ("fixed_k", "Fixed k (optional; leave blank to use v_eff)", None),
        (None, "", None),
        ("u_c", "Combined standard uncertainty u_c", f"=SQRT(SUMSQ({rng('J')}))"),
        ("v_eff", "Effective degrees of freedom v_eff", f'=IF(SUM({rng("L")})=0,"infinite",{UB_CELLS["u_c"]}^4/SUM({rng("L")}))'),
        ("k", "Coverage factor k", (
            f'=IF({UB_CELLS["fixed_k"]}<>"",{UB_CELLS["fixed_k"]},IF({UB_CELLS["v_eff"]}="infinite",'
            f'_xlfn.NORM.S.INV(0.5+{UB_CELLS["coverage"]}/2),_xlfn.T.INV.2T(1-{UB_CELLS["coverage"]},{UB_CELLS["v_eff"]})))'
        )),
        ("U", "Expanded uncertainty U = k · u_c", f'={UB_CELLS["k"]}*{UB_CELLS["u_c"]}'),
        ("U_rel", "Relative expanded uncertainty U / |y|", f'=IF({UB_CELLS["value"]}="","",{UB_CELLS["U"]}/ABS({UB_CELLS["value"]}))'),
    ]
    row = 28
    for key, label, value in summary:
        ws.cell(row=row, column=1, value=label).font = st["bold"] if key in ("U",) else Font()
        if key:
            cell = ws.cell(row=row, column=3, value=value)
            cell.border = st["border"]
            if key in ("u_c", "v_eff", "k", "U", "U_rel"):
                cell.fill = st["label_fill"]
            if key == "value" and value is not None:
                cell.font = st["example_font"]
            assert f"C{row}" == UB_CELLS[key], (key, row)
        row += 1
    ws[UB_CELLS["coverage"]].number_format = "0%"
    ws[UB_CELLS["U_rel"]].number_format = "0.00%"
    for key in ("u_c", "U"):
        ws[UB_CELLS[key]].number_format = "0.0000"
    ws[UB_CELLS["v_eff"]].number_format = ws[UB_CELLS["k"]].number_format = "0.00"
    ws[UB_CELLS["U"]].font = st["bold"]

    notes = [
        "Value: for normal, a standard uncertainty (or an expanded one with its k in column D); for the other distributions, the half-width a.",
        "Divisors: rectangular √3, triangular √6, u-shaped √2. Sensitivity c is 1 when the source is already in the units of the result.",
        "Same calculation as labqc.uncertainty.combine for independent inputs. Excel rounds degrees of freedom down to a whole number in "
        "T.INV.2T, so k can be very slightly larger than labqc's.",
    ]
    for i, n in enumerate(notes, start=38):
        ws.cell(row=i, column=1, value=n).alignment = st["wrap"]
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=12)
        ws.row_dimensions[i].height = 30


BUILDERS = {"uncertainty_budget": _uncertainty_budget}


def build_xlsx(template: dict, out: Path) -> None:
    from openpyxl import Workbook

    spec = yaml.safe_load(template["source"].read_text(encoding="utf-8"))
    wb = Workbook()
    wb.remove(wb.active)
    _about_sheet(wb, spec)
    if spec.get("builder"):
        BUILDERS[spec["builder"]](wb, spec)
    for sheet in spec.get("sheets", []):
        _table_sheet(wb, copy.deepcopy(sheet))
    wb.active = 1 if len(wb.sheetnames) > 1 else 0
    wb.properties.title = template["title"]
    wb.properties.creator = "Lab Accreditation Handbook"
    wb.save(str(out))


# ---------------------------------------------------------------- driver


def build(force: bool = False, quiet: bool = False) -> list[Path]:
    """Build every template whose output is missing or older than its source or this script."""
    OUT.mkdir(parents=True, exist_ok=True)
    script_time = Path(__file__).stat().st_mtime
    built = []
    for t in catalog():
        out = output_path(t)
        stale = force or not out.exists() or out.stat().st_mtime < max(t["source"].stat().st_mtime, script_time)
        if not stale:
            continue
        (build_docx if t["format"] == "docx" else build_xlsx)(t, out)
        built.append(out)
        if not quiet:
            print(f"built {out.relative_to(ROOT)}")
    known = {output_path(t).name for t in catalog()}
    for old in OUT.iterdir():
        if old.is_file() and old.name not in known:
            old.unlink()
            if not quiet:
                print(f"removed {old.relative_to(ROOT)}")
    return built


if __name__ == "__main__":
    built = build(force="--force" in sys.argv)
    print(f"{len(built)} template(s) built")
