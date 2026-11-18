---
description: A free internal audit planner for ISO/IEC 17025 labs that runs in your browser. Plan audits per clause over 12 months, mark them done, see any clause left out, and export to CSV.
hide:
  - toc
---

# Internal audit planner

Plan your internal audits as a grid of clauses by months. Tap a cell once
for **P** (planned) and again for **D** (done); a third tap clears it.
Clauses with nothing planned or done in the 12 months are highlighted, so
none is forgotten. See [8.8 Internal audits](../management/8-8-internal-audits.md)
for how to build a good programme.

!!! info "Your plan stays in your browser"
    Nothing is sent anywhere. The plan is kept in this browser; use **Save
    plan** to keep a file you can load elsewhere, or **Export CSV** to open it
    in a spreadsheet. The [internal audit plan template](../downloads/internal-audit-plan.xlsx)
    does the same in Excel.

<div id="planner-app" class="tool-app">

<div class="tool-bar">
  <label class="tool-field">Start month <select id="start-month"></select></label>
  <label class="tool-field">Year <input type="number" id="start-year" min="2000" max="2199" step="1"></label>
  <button type="button" id="export-csv" class="md-button md-button--primary">Export CSV</button>
  <button type="button" id="save-json" class="md-button">Save plan</button>
  <label class="md-button tool-file">Load plan<input type="file" id="load-json" accept="application/json,.json"></label>
  <button type="button" id="reset" class="md-button tool-reset">Reset</button>
</div>

<p id="planner-summary" class="planner-summary" role="status"></p>

<div class="planner-scroll">
<table id="planner-grid" class="planner-grid"></table>
</div>

</div>

<!-- tool-data -->
<script src="../tools-common.js"></script>
<script src="../audit-planner.js"></script>
