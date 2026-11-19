---
description: Free browser tools for ISO/IEC 17025 labs - a gap analysis with readiness scores and an internal audit planner. Nothing leaves your browser.
---

# Tools

Two free tools that run entirely in your browser. There is no account and
no server: nothing you enter is sent anywhere. Both remember your work in
this browser and can save it to a file.

<div class="grid cards" markdown>

-   **[Gap analysis](gap-analysis.md)**

    About 140 practical yes / partly / no questions across every clause.
    Get a readiness score per clause, a chart, and a to-do list linked to
    the chapters. Export to Excel or CSV.

-   **[Internal audit planner](audit-planner.md)**

    Plan audits as a grid of clauses by months, mark them done, and see at a
    glance any clause not covered in the year. Export to CSV.

</div>

## Calculations

For uncertainty budgets, method validation, PT scores and QC charts, use
[labqc](https://github.com/mantas123456/lab-quality-toolkit), a free Python
library, or its [web app](https://lab-quality-toolkit-3go33hyzzwjhwpktn8tles.streamlit.app),
which needs no installation; the free app may take about 30 seconds to wake up. Each chapter's side panel links to the right
labqc function.

## Third-party code

The Excel export in the gap analysis uses [SheetJS](https://sheetjs.com)
Community Edition 0.20.3, bundled with the site (no CDN), under the
[Apache 2.0 licence](vendor/SHEETJS-LICENSE.txt).
