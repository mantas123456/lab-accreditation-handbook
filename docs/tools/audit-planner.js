/* Internal audit planner: a grid of clauses × 12 months. Tap a cell to cycle
 * empty → Planned → Done. Clauses with nothing planned or done in the 12
 * months are flagged. Export to CSV; save and load progress as a JSON file. */
(function () {
  "use strict";
  var T = window.HandbookTools;
  var STORE_KEY = "lah-audit-planner-v1";
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var NEXT = { "": "P", P: "D", D: "" };
  var LABEL = { "": "", P: "Planned", D: "Done" };

  var data, state, root;

  function blank() {
    var now = new Date();
    return { startYear: now.getFullYear(), startMonth: 0, cells: {}, auditors: {} };
  }

  function months() {
    var out = [];
    for (var i = 0; i < 12; i++) {
      var m = (state.startMonth + i) % 12;
      var y = state.startYear + Math.floor((state.startMonth + i) / 12);
      out.push({ index: i, label: MONTHS[m] + " " + String(y).slice(2), full: MONTHS[m] + " " + y });
    }
    return out;
  }

  function cell(num, i) {
    return state.cells[num + "#" + i] || "";
  }

  function covered(num) {
    for (var i = 0; i < 12; i++) if (cell(num, i)) return true;
    return false;
  }

  function render() {
    var table = document.getElementById("planner-grid");
    table.innerHTML = "";
    var head = T.el("tr", {}, [T.el("th", { scope: "col", className: "planner-clause", text: "Clause" })]);
    months().forEach(function (m) {
      head.appendChild(T.el("th", { scope: "col", text: m.label, title: m.full }));
    });
    head.appendChild(T.el("th", { scope: "col", text: "Auditor" }));
    table.appendChild(T.el("thead", {}, [head]));
    var body = T.el("tbody");
    data.clauses.forEach(function (c) {
      var row = T.el("tr", { "data-clause": c.number });
      row.appendChild(
        T.el("th", { scope: "row", className: "planner-clause" }, [
          T.el("a", { href: c.href, text: c.number }),
          T.el("span", { className: "planner-clause__title", text: " " + c.title }),
        ])
      );
      months().forEach(function (m) {
        var v = cell(c.number, m.index);
        var btn = T.el("button", {
          type: "button",
          className: "planner-cell planner-cell--" + (v || "empty"),
          "data-month": String(m.index),
          "aria-label": c.number + " " + m.full + ": " + (LABEL[v] || "nothing planned"),
          text: v,
        });
        btn.addEventListener("click", function () {
          var k = c.number + "#" + m.index;
          var nv = NEXT[cell(c.number, m.index)];
          if (nv) state.cells[k] = nv;
          else delete state.cells[k];
          save();
          render();
        });
        row.appendChild(T.el("td", {}, [btn]));
      });
      var input = T.el("input", { type: "text", className: "planner-auditor", "aria-label": "Auditor for " + c.number });
      input.value = state.auditors[c.number] || "";
      input.addEventListener("change", function () {
        state.auditors[c.number] = input.value;
        save();
      });
      row.appendChild(T.el("td", {}, [input]));
      if (!covered(c.number)) row.classList.add("planner-row--flagged");
      body.appendChild(row);
    });
    table.appendChild(body);

    var flagged = data.clauses.filter(function (c) { return !covered(c.number); });
    var done = data.clauses.filter(function (c) {
      for (var i = 0; i < 12; i++) if (cell(c.number, i) === "D") return true;
      return false;
    });
    var summary = document.getElementById("planner-summary");
    summary.setAttribute("data-flagged", String(flagged.length));
    summary.textContent =
      flagged.length === 0
        ? "Every clause is planned or audited in these 12 months. " + done.length + " of " + data.clauses.length + " done."
        : flagged.length + " of " + data.clauses.length + " clauses are not covered in these 12 months: " +
          flagged.map(function (c) { return c.number; }).join(", ") + ". " + done.length + " done.";
    summary.className = "planner-summary " + (flagged.length ? "planner-summary--warn" : "planner-summary--ok");
  }

  function save() {
    T.storeSet(STORE_KEY, state);
  }

  function exportCsv() {
    var ms = months();
    var rows = [["Clause", "Topic"].concat(ms.map(function (m) { return m.full; })).concat(["Covered", "Auditor"])];
    data.clauses.forEach(function (c) {
      rows.push(
        [c.number, c.title]
          .concat(ms.map(function (m) { return LABEL[cell(c.number, m.index)]; }))
          .concat([covered(c.number) ? "Yes" : "NO", state.auditors[c.number] || ""])
      );
    });
    T.download(T.toCsv(rows), "audit-plan-" + T.today() + ".csv", "text/csv;charset=utf-8");
  }

  function load(obj) {
    if (!obj || obj.tool !== "audit-planner" || typeof obj.state !== "object") {
      window.alert("This file is not a saved audit plan.");
      return;
    }
    state = Object.assign(blank(), obj.state);
    save();
    syncControls();
    render();
  }

  function syncControls() {
    document.getElementById("start-month").value = String(state.startMonth);
    document.getElementById("start-year").value = String(state.startYear);
  }

  function init() {
    root = document.getElementById("planner-app");
    if (!root) return;
    data = T.toolData();
    state = Object.assign(blank(), T.storeGet(STORE_KEY) || {});
    var monthSel = document.getElementById("start-month");
    MONTHS.forEach(function (m, i) {
      monthSel.appendChild(T.el("option", { value: String(i), text: m }));
    });
    syncControls();
    monthSel.addEventListener("change", function () {
      state.startMonth = parseInt(monthSel.value, 10);
      save();
      render();
    });
    var yearIn = document.getElementById("start-year");
    yearIn.addEventListener("change", function () {
      var y = parseInt(yearIn.value, 10);
      if (y > 1999 && y < 2200) {
        state.startYear = y;
        save();
        render();
      }
    });
    document.getElementById("export-csv").addEventListener("click", exportCsv);
    document.getElementById("save-json").addEventListener("click", function () {
      T.download(
        JSON.stringify({ tool: "audit-planner", version: 1, saved: new Date().toISOString(), state: state }, null, 2),
        "audit-plan-" + T.today() + ".json",
        "application/json"
      );
    });
    var fileInput = document.getElementById("load-json");
    fileInput.addEventListener("change", function () { T.readJsonFile(fileInput, load); });
    document.getElementById("reset").addEventListener("click", function () {
      if (window.confirm("Clear the whole plan in this browser? Save it to a file first if you want to keep it.")) {
        state = blank();
        T.storeRemove(STORE_KEY);
        syncControls();
        render();
      }
    });
    render();
    root.setAttribute("data-ready", "true");
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
