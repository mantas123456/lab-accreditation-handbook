/* Shared helpers for the handbook's browser tools.
 * Everything runs in the reader's browser: no server, no network calls,
 * nothing stored outside this browser unless the reader saves a file. */
(function () {
  "use strict";

  function toolData() {
    var el = document.getElementById("tool-data");
    return el ? JSON.parse(el.textContent) : { clauses: [] };
  }

  // localStorage can be missing or blocked (private windows, strict settings);
  // the tools still work, they just do not remember answers between visits.
  function storeGet(key) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function storeSet(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      /* not available: ignore */
    }
  }

  function storeRemove(key) {
    try {
      window.localStorage.removeItem(key);
    } catch (e) {
      /* ignore */
    }
  }

  function download(content, filename, type) {
    var blob = content instanceof Blob ? content : new Blob([content], { type: type || "text/plain" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () {
      URL.revokeObjectURL(url);
      a.remove();
    }, 0);
  }

  function csvCell(value) {
    var s = value === null || value === undefined ? "" : String(value);
    return /[",\n\r;]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  }

  function toCsv(rows) {
    // Byte order mark so Excel opens UTF-8 (°, ±, Lithuanian letters) correctly.
    return "﻿" + rows.map(function (r) { return r.map(csvCell).join(","); }).join("\r\n") + "\r\n";
  }

  function readJsonFile(input, onLoad) {
    var file = input.files && input.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      try {
        onLoad(JSON.parse(reader.result));
      } catch (e) {
        window.alert("This file could not be read as saved progress.");
      }
      input.value = "";
    };
    reader.readAsText(file);
  }

  function today() {
    var d = new Date();
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "className") node.className = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) {
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  window.HandbookTools = {
    toolData: toolData,
    storeGet: storeGet,
    storeSet: storeSet,
    storeRemove: storeRemove,
    download: download,
    toCsv: toCsv,
    readJsonFile: readJsonFile,
    today: today,
    el: el,
  };
})();
