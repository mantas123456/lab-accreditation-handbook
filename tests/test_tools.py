"""Browser tests for the gap analysis and the audit planner (Playwright).

The site is built into a temporary folder and served locally; the tests then
answer questions, check the scores, exports, save/load, phone layout, and that
the tools make no network requests of their own.

    pip install -r requirements-dev.txt
    python -m playwright install chromium
    pytest tests/test_tools.py
"""

from __future__ import annotations

import csv
import functools
import http.server
import io
import json
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import urlparse

import pytest

ROOT = Path(__file__).resolve().parent.parent
# Third-party hosts the site itself loads on every page. The tools must add none.
# api.github.com: the theme's repository widget (stars, latest release) in the header.
SITE_ASSET_HOSTS = {"cdn.jsdelivr.net", "fonts.googleapis.com", "fonts.gstatic.com", "api.github.com"}


@pytest.fixture(scope="session")
def site_url(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "--site-dir", str(out)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        env={**__import__("os").environ, "NO_MKDOCS_2_WARNING": "1"},
    )
    handler = functools.partial(_QuietHandler, directory=str(out))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}/"
    server.shutdown()


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(autouse=True)
def offline(context, site_url):
    """Keep the tests hermetic: block every request that leaves the local test
    server, and record it so tests can check what the page tried to fetch."""
    origin = urlparse(site_url).netloc
    attempts: list[tuple[str, str]] = []

    def handle(route):
        url = route.request.url
        if urlparse(url).netloc == origin:
            route.continue_()
        else:
            attempts.append((route.request.method, url))
            route.abort()

    context.route("**/*", handle)
    return attempts


@pytest.fixture()
def gap(page, site_url):
    page.on("dialog", lambda d: d.accept())
    page.goto(site_url + "tools/gap-analysis/")
    page.wait_for_selector("#gap-app[data-ready='true']")
    return page


def _answer(page, clause: str, index: int, value: str) -> None:
    details = page.locator(f"details.gap-clause[data-clause='{clause}']")
    if not details.evaluate("d => d.open"):
        details.locator("summary").click()
    page.locator(f"label[for='q-{clause}-{index}-{value}']").click()


def _answer_41(page) -> None:
    # 4.1 has five questions: yes, yes, partly, no, n/a -> (1 + 1 + 0.5 + 0) / 4 = 0.625
    for i, v in enumerate(["yes", "yes", "partly", "no", "na"]):
        _answer(page, "4.1", i, v)


def test_gap_scores_and_todo(gap):
    assert gap.locator("#overall-score").inner_text() == "Not started"
    assert gap.locator("[data-score-for='4.1']").inner_text() == "Not started"
    _answer_41(gap)
    badge = gap.locator("[data-score-for='4.1']")
    assert badge.get_attribute("data-score") == "0.625"
    assert badge.inner_text().startswith("63%")
    assert "5/5 answered" in badge.inner_text()
    # Overall: 2.5 points over every applicable question (all but the one N/A).
    total = gap.evaluate(
        "() => JSON.parse(document.getElementById('tool-data').textContent)"
        ".clauses.reduce((n, c) => n + c.questions.length, 0)"
    )
    expected = round(2.5 / (total - 1), 3)
    assert float(gap.locator("#overall-score").get_attribute("data-score")) == pytest.approx(expected)
    items = gap.locator("#todo-list li")
    assert items.count() == 2
    assert sorted(items.nth(i).get_attribute("data-answer") for i in range(2)) == ["no", "partly"]
    # The to-do item links to the chapter.
    href = items.first.locator("a").get_attribute("href")
    assert href.endswith("general/4-1-impartiality/")


def test_gap_answers_survive_reload(gap):
    _answer_41(gap)
    gap.reload()
    gap.wait_for_selector("#gap-app[data-ready='true']")
    assert gap.locator("[data-score-for='4.1']").get_attribute("data-score") == "0.625"


def test_gap_exports(gap):
    from openpyxl import load_workbook

    _answer_41(gap)
    with gap.expect_download() as dl:
        gap.click("#export-csv")
    text = Path(dl.value.path()).read_text(encoding="utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))
    assert rows[0] == ["Clause", "Topic", "Question", "Answer", "Clause score"]
    answers_41 = [r[3] for r in rows[1:] if r[0] == "4.1"]
    assert answers_41 == ["Yes", "Yes", "Partly", "No", "N/A"]

    with gap.expect_download() as dl:
        gap.click("#export-xlsx")
    assert dl.value.suggested_filename.endswith(".xlsx")
    wb = load_workbook(io.BytesIO(Path(dl.value.path()).read_bytes()))
    assert wb.sheetnames == ["Scores", "To-do", "Answers"]
    scores = {r[0]: r[2] for r in wb["Scores"].iter_rows(min_row=2, values_only=True) if r and r[0]}
    assert scores["4.1"] == pytest.approx(0.625)
    assert wb["To-do"].max_row == 3  # header + 2 items


def test_gap_save_reset_load(gap):
    _answer_41(gap)
    with gap.expect_download() as dl:
        gap.click("#save-json")
    saved = Path(dl.value.path())
    assert json.loads(saved.read_text(encoding="utf-8"))["tool"] == "gap-analysis"
    gap.click("#reset")
    assert gap.locator("[data-score-for='4.1']").get_attribute("data-score") == ""
    gap.set_input_files("#load-json", str(saved))
    # The file is read asynchronously (FileReader), so wait for the score.
    from playwright.sync_api import expect

    expect(gap.locator("[data-score-for='4.1']")).to_have_attribute("data-score", "0.625")


@pytest.fixture()
def planner(page, site_url):
    page.on("dialog", lambda d: d.accept())
    page.goto(site_url + "tools/audit-planner/")
    page.wait_for_selector("#planner-app[data-ready='true']")
    return page


def test_planner_flags_and_export(planner):
    summary = planner.locator("#planner-summary")
    n = int(summary.get_attribute("data-flagged"))
    assert n == planner.locator("tr[data-clause]").count() == 29
    cell = planner.locator("tr[data-clause='4.1'] button[data-month='0']")
    cell.click()
    assert planner.locator("tr[data-clause='4.1'] button[data-month='0']").inner_text() == "P"
    assert summary.get_attribute("data-flagged") == "28"
    planner.locator("tr[data-clause='4.1'] button[data-month='0']").click()
    assert planner.locator("tr[data-clause='4.1'] button[data-month='0']").inner_text() == "D"
    assert "planner-row--flagged" not in (planner.locator("tr[data-clause='4.1']").get_attribute("class") or "")
    assert "planner-row--flagged" in planner.locator("tr[data-clause='4.2']").get_attribute("class")

    with planner.expect_download() as dl:
        planner.click("#export-csv")
    rows = list(csv.reader(io.StringIO(Path(dl.value.path()).read_text(encoding="utf-8-sig"))))
    row_41 = next(r for r in rows if r[0] == "4.1")
    assert row_41[2] == "Done" and row_41[-2] == "Yes"
    assert next(r for r in rows if r[0] == "4.2")[-2] == "NO"

    # A third tap clears the cell again.
    planner.locator("tr[data-clause='4.1'] button[data-month='0']").click()
    assert summary.get_attribute("data-flagged") == "29"


@pytest.mark.parametrize("path", ["tools/gap-analysis/", "tools/audit-planner/"])
def test_phone_layout_has_no_page_scroll(browser, site_url, path):
    context = browser.new_context(viewport={"width": 375, "height": 740}, is_mobile=True, has_touch=True)
    origin = urlparse(site_url).netloc
    context.route("**/*", lambda r: r.continue_() if urlparse(r.request.url).netloc == origin else r.abort())
    page = context.new_page()
    page.goto(site_url + path)
    page.wait_for_selector("[data-ready='true']")
    page.locator("details.gap-clause").first.evaluate("d => d && (d.open = true)") if "gap" in path else None
    overflow = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 1, f"page scrolls sideways by {overflow}px on a phone"
    context.close()


def test_tools_make_no_network_requests_of_their_own(page, site_url, offline):
    page.on("dialog", lambda d: d.accept())
    page.goto(site_url + "tools/gap-analysis/")
    page.wait_for_selector("#gap-app[data-ready='true']")
    # The site's own pages may ask for fonts, MathJax and the repo widget; nothing else.
    loaded = list(offline)
    for method, url in loaded:
        assert method == "GET", url
        assert urlparse(url).netloc in SITE_ASSET_HOSTS, url
    # Using the tool, exporting and saving must not reach out at all.
    _answer_41(page)
    with page.expect_download():
        page.click("#export-xlsx")
    with page.expect_download():
        page.click("#export-csv")
    with page.expect_download():
        page.click("#save-json")
    assert offline[len(loaded):] == [], offline[len(loaded):]
