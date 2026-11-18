---
description: A free ISO/IEC 17025 gap analysis that runs in your browser. Answer yes, partly, no or not applicable for each clause, get a readiness score and a to-do list, and export to Excel or CSV.
hide:
  - toc
---

# Gap analysis

Work through each clause and answer every question for **your lab as it is
today**. You get a readiness score per clause, a chart, and a to-do list of
everything answered *No* or *Partly*, with a link to the chapter that
explains what to do.

!!! info "Your answers stay in your browser"
    Nothing is sent anywhere. Answers are kept in this browser so you can come
    back later; use **Save progress** to keep a file you can load on another
    computer or share with a colleague.

<div id="gap-app" class="tool-app">

<div class="tool-bar">
  <button type="button" id="export-xlsx" class="md-button md-button--primary">Export Excel</button>
  <button type="button" id="export-csv" class="md-button">Export CSV</button>
  <button type="button" id="save-json" class="md-button">Save progress</button>
  <label class="md-button tool-file">Load progress<input type="file" id="load-json" accept="application/json,.json"></label>
  <button type="button" id="reset" class="md-button tool-reset">Reset</button>
</div>

<div class="gap-summary">
  <div class="gap-summary__overall">
    <span class="gap-summary__label">Overall readiness</span>
    <span id="overall-score" class="gap-summary__score">Not started</span>
    <span id="overall-answered" class="gap-summary__answered"></span>
  </div>
  <div id="gap-chart" class="gap-chart-host"></div>
</div>

<h2 id="questions">Questions</h2>
<p class="tool-hint">Scores: Yes = 1, Partly = 0.5, No = 0. <em>N/A</em> questions are left out. Unanswered questions count as 0, so the overall score only reaches its true value once every clause is answered. <button type="button" id="expand-all" class="tool-link">Open or close all clauses</button></p>
<div id="gap-questions"></div>

<h2 id="to-do">To-do list</h2>
<div id="gap-todo"></div>

</div>

<!-- tool-data -->
<script src="../tools-common.js"></script>
<script src="../vendor/xlsx.mini.min.js"></script>
<script src="../gap-analysis.js"></script>

The questions are this handbook's own practical checks, written in plain
English; they are not the text of the standard. A high score is a good sign,
not a guarantee: an assessor looks at evidence, so for every *Yes* make sure
you could show the record.
