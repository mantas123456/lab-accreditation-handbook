/* Gap analysis: answer yes / partly / no / not applicable for each question,
 * get a readiness score per clause, a bar chart and a to-do list, and export.
 * Score per clause = (yes + 0.5 × partly) / (questions − not applicable).
 * Unanswered questions count as 0 until answered. */
(function () {
  "use strict";
  var T = window.HandbookTools;
  var STORE_KEY = "lah-gap-analysis-v1";
  var ANSWERS = [
    { value: "yes", label: "Yes", points: 1 },
    { value: "partly", label: "Partly", points: 0.5 },
    { value: "no", label: "No", points: 0 },
    { value: "na", label: "N/A", points: null },
  ];
  var POINTS = { yes: 1, partly: 0.5, no: 0 };

  var data, answers, root;

  function key(num, i) {
    return num + "#" + i;
  }

  function clauseScore(c) {
    var applicable = 0, points = 0, answered = 0;
    c.questions.forEach(function (_, i) {
      var a = answers[key(c.number, i)];
      if (a) answered++;
      if (a === "na") return;
      applicable++;
      if (a && POINTS[a] !== undefined) points += POINTS[a];
    });
    return {
      // No answers yet: no score, rather than a misleading 0 %.
      score: applicable && answered ? points / applicable : null,
      points: points,
      applicable: applicable,
      answered: answered,
      total: c.questions.length,
    };
  }

  function overall() {
    var points = 0, applicable = 0, answered = 0, total = 0;
    data.clauses.forEach(function (c) {
      var s = clauseScore(c);
      points += s.points;
      applicable += s.applicable;
      answered += s.answered;
      total += s.total;
    });
    return { score: applicable && answered ? points / applicable : null, answered: answered, total: total };
  }

  function pct(x) {
    return x === null ? "–" : Math.round(x * 100) + "%";
  }

  function level(x) {
    if (x === null) return "na";
    if (x >= 0.8) return "good";
    if (x >= 0.5) return "fair";
    return "poor";
  }

  // ------------------------------------------------------------ rendering

  function renderQuestions(container) {
    var parts = [];
    data.clauses.forEach(function (c) {
      if (parts.indexOf(c.part) < 0) parts.push(c.part);
    });
    parts.forEach(function (part) {
      container.appendChild(T.el("h2", { text: part, className: "gap-part" }));
      data.clauses.filter(function (c) { return c.part === part; }).forEach(function (c) {
        var details = T.el("details", { className: "gap-clause", "data-clause": c.number });
        var summary = T.el("summary", {}, [
          T.el("span", { className: "gap-clause__title", text: c.number + " " + c.title }),
          T.el("span", { className: "gap-clause__score", "data-score-for": c.number }),
        ]);
        details.appendChild(summary);
        details.appendChild(
          T.el("p", { className: "gap-clause__link" }, [
            T.el("a", { href: c.href, text: "Read the chapter for " + c.number }),
          ])
        );
        c.questions.forEach(function (q, i) {
          var name = "q-" + c.number + "-" + i;
          var fs = T.el("fieldset", { className: "gap-q" }, [T.el("legend", { text: q })]);
          var choices = T.el("div", { className: "gap-choices" });
          ANSWERS.forEach(function (a) {
            var id = name + "-" + a.value;
            var input = T.el("input", { type: "radio", name: name, id: id, value: a.value });
            if (answers[key(c.number, i)] === a.value) input.checked = true;
            input.addEventListener("change", function () {
              answers[key(c.number, i)] = a.value;
              save();
              update();
            });
            choices.appendChild(input);
            choices.appendChild(T.el("label", { for: id, className: "gap-choice gap-choice--" + a.value, text: a.label }));
          });
          fs.appendChild(choices);
          details.appendChild(fs);
        });
        container.appendChild(details);
      });
    });
  }

  function renderChart(svgHost) {
    var rowH = 18, labelW = 44, width = 320, barW = width - labelW - 40;
    var h = data.clauses.length * rowH + 4;
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 " + width + " " + h);
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Readiness score per clause");
    svg.setAttribute("class", "gap-chart");
    data.clauses.forEach(function (c, i) {
      var s = clauseScore(c).score;
      var y = i * rowH + 2;
      var label = document.createElementNS(ns, "text");
      label.setAttribute("x", labelW - 6);
      label.setAttribute("y", y + rowH * 0.7);
      label.setAttribute("text-anchor", "end");
      label.setAttribute("class", "gap-chart__label");
      label.textContent = c.number;
      svg.appendChild(label);
      var track = document.createElementNS(ns, "rect");
      track.setAttribute("x", labelW);
      track.setAttribute("y", y + 3);
      track.setAttribute("width", barW);
      track.setAttribute("height", rowH - 6);
      track.setAttribute("rx", 3);
      track.setAttribute("class", "gap-chart__track");
      svg.appendChild(track);
      if (s !== null && s > 0) {
        var bar = document.createElementNS(ns, "rect");
        bar.setAttribute("x", labelW);
        bar.setAttribute("y", y + 3);
        bar.setAttribute("width", Math.max(2, barW * s));
        bar.setAttribute("height", rowH - 6);
        bar.setAttribute("rx", 3);
        bar.setAttribute("class", "gap-chart__bar gap-chart__bar--" + level(s));
        svg.appendChild(bar);
      }
      var val = document.createElementNS(ns, "text");
      val.setAttribute("x", labelW + barW + 4);
      val.setAttribute("y", y + rowH * 0.7);
      val.setAttribute("class", "gap-chart__value");
      val.textContent = pct(s);
      svg.appendChild(val);
    });
    svgHost.innerHTML = "";
    svgHost.appendChild(svg);
  }

  function todoItems() {
    var items = [];
    data.clauses.forEach(function (c) {
      c.questions.forEach(function (q, i) {
        var a = answers[key(c.number, i)];
        if (a === "no" || a === "partly") items.push({ clause: c, question: q, answer: a });
      });
    });
    return items;
  }

  function renderTodo(host) {
    var items = todoItems();
    host.innerHTML = "";
    if (!items.length) {
      host.appendChild(T.el("p", { className: "gap-todo__empty", text: "Nothing on the list yet. Answers of No or Partly appear here." }));
      return;
    }
    var list = T.el("ol", { id: "todo-list", className: "gap-todo" });
    items.forEach(function (it) {
      list.appendChild(
        T.el("li", { "data-answer": it.answer }, [
          T.el("span", { className: "gap-tag gap-tag--" + it.answer, text: it.answer === "no" ? "No" : "Partly" }),
          " ",
          T.el("a", { href: it.clause.href, text: it.clause.number }),
          " " + it.question,
        ])
      );
    });
    host.appendChild(list);
  }

  function update() {
    data.clauses.forEach(function (c) {
      var s = clauseScore(c);
      var badge = root.querySelector('[data-score-for="' + c.number + '"]');
      badge.textContent = s.answered
        ? (s.score === null ? "All N/A" : pct(s.score)) + " · " + s.answered + "/" + s.total + " answered"
        : "Not started";
      badge.className = "gap-clause__score gap-level--" + level(s.score);
      badge.setAttribute("data-score", s.score === null ? "" : String(Math.round(s.score * 1000) / 1000));
    });
    var o = overall();
    var overallEl = document.getElementById("overall-score");
    overallEl.textContent = o.answered ? pct(o.score) : "Not started";
    overallEl.setAttribute("data-score", o.score === null ? "" : String(Math.round(o.score * 1000) / 1000));
    document.getElementById("overall-answered").textContent = o.answered + " of " + o.total + " questions answered";
    renderChart(document.getElementById("gap-chart"));
    renderTodo(document.getElementById("gap-todo"));
  }

  // ------------------------------------------------------------ persistence and export

  function save() {
    T.storeSet(STORE_KEY, answers);
  }

  function snapshot() {
    return { tool: "gap-analysis", version: 1, saved: new Date().toISOString(), edition: data.edition, answers: answers };
  }

  function load(obj) {
    if (!obj || obj.tool !== "gap-analysis" || typeof obj.answers !== "object") {
      window.alert("This file is not saved gap-analysis progress.");
      return;
    }
    answers = obj.answers;
    save();
    rebuild();
  }

  function rows() {
    var out = [["Clause", "Topic", "Question", "Answer", "Clause score"]];
    data.clauses.forEach(function (c) {
      var s = pct(clauseScore(c).score);
      c.questions.forEach(function (q, i) {
        var a = answers[key(c.number, i)];
        var label = a ? ANSWERS.filter(function (x) { return x.value === a; })[0].label : "";
        out.push([c.number, c.title, q, label, s]);
      });
    });
    return out;
  }

  function exportCsv() {
    T.download(T.toCsv(rows()), "gap-analysis-" + T.today() + ".csv", "text/csv;charset=utf-8");
  }

  function exportXlsx() {
    if (!window.XLSX) {
      window.alert("The Excel export library did not load. Use the CSV export instead.");
      return;
    }
    var wb = XLSX.utils.book_new();
    var scores = [["Clause", "Topic", "Score", "Answered", "Questions"]];
    data.clauses.forEach(function (c) {
      var s = clauseScore(c);
      scores.push([c.number, c.title, s.score === null ? "" : Math.round(s.score * 1000) / 1000, s.answered, s.total]);
    });
    var o = overall();
    scores.push([]);
    scores.push(["Overall", "", o.score === null ? "" : Math.round(o.score * 1000) / 1000, o.answered, o.total]);
    var todo = [["Clause", "Question", "Answer", "Owner", "Due date", "Done"]];
    todoItems().forEach(function (it) {
      todo.push([it.clause.number, it.question, it.answer === "no" ? "No" : "Partly", "", "", ""]);
    });
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(scores), "Scores");
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(todo), "To-do");
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(rows()), "Answers");
    XLSX.writeFile(wb, "gap-analysis-" + T.today() + ".xlsx");
  }

  function rebuild() {
    var q = document.getElementById("gap-questions");
    q.innerHTML = "";
    renderQuestions(q);
    update();
  }

  function init() {
    root = document.getElementById("gap-app");
    if (!root) return;
    data = T.toolData();
    answers = T.storeGet(STORE_KEY) || {};
    document.getElementById("export-csv").addEventListener("click", exportCsv);
    document.getElementById("export-xlsx").addEventListener("click", exportXlsx);
    document.getElementById("save-json").addEventListener("click", function () {
      T.download(JSON.stringify(snapshot(), null, 2), "gap-analysis-progress-" + T.today() + ".json", "application/json");
    });
    var fileInput = document.getElementById("load-json");
    fileInput.addEventListener("change", function () { T.readJsonFile(fileInput, load); });
    document.getElementById("reset").addEventListener("click", function () {
      if (window.confirm("Clear all answers in this browser? Save your progress to a file first if you want to keep it.")) {
        answers = {};
        T.storeRemove(STORE_KEY);
        rebuild();
      }
    });
    document.getElementById("expand-all").addEventListener("click", function () {
      var all = root.querySelectorAll("details.gap-clause");
      var open = Array.prototype.some.call(all, function (d) { return !d.open; });
      Array.prototype.forEach.call(all, function (d) { d.open = open; });
    });
    rebuild();
    root.setAttribute("data-ready", "true");
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
