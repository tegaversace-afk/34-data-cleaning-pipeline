// app.js — Role 5 UI logic. Plain fetch() calls to our own FastAPI endpoints.
// Relative URLs (/api/...) mean the SAME code works locally and on Render.
const $ = (id) => document.getElementById(id);
const fileInput = $("fileInput"), dropzone = $("dropzone");

// ---------- file picking + drag & drop ----------
fileInput.addEventListener("change", () => showFileName());
["dragover", "dragenter"].forEach(e => dropzone.addEventListener(e, ev => {
  ev.preventDefault(); dropzone.classList.add("over");
}));
["dragleave", "drop"].forEach(e => dropzone.addEventListener(e, ev => {
  ev.preventDefault(); dropzone.classList.remove("over");
}));
dropzone.addEventListener("drop", ev => {
  if (ev.dataTransfer.files.length) { fileInput.files = ev.dataTransfer.files; showFileName(); }
});
function showFileName() {
  $("fileName").textContent = fileInput.files.length ? fileInput.files[0].name : "No file chosen · max 5 MB";
}

// ---------- run the pipeline ----------
$("uploadBtn").addEventListener("click", async () => {
  if (!fileInput.files.length) return showError("Choose a .csv file first — or click 'Use Sample Data'.");
  const body = new FormData(); body.append("file", fileInput.files[0]);
  await run("/api/upload", { method: "POST", body });
});
$("sampleBtn").addEventListener("click", () => run("/api/run-sample", { method: "POST" }));

async function run(url, options) {
  hideError(); $("loading").hidden = false;
  try {
    const res = await fetch(url, options);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Something went wrong. Please try again.");
    render(data);
    loadHistory();
  } catch (err) { showError(err.message); }
  finally { $("loading").hidden = true; }
}

// ---------- rendering results ----------
function esc(v) { const d = document.createElement("div"); d.textContent = v ?? ""; return d.innerHTML; }

function render(data) {
  $("results").hidden = false;
  $("resultFile").textContent = "— " + data.filename;
  const r = data.report;
  const stats = [
    [r.total_rows_in, "Rows in"], [r.rows_out, "Rows out"],
    [r.duplicates_removed, "Duplicates removed"], [r.cells_changed, "Cells fixed"],
    [r.total_issues, "Issues found"], [r.rows_with_issues, "Rows with issues"],
  ];
  $("stats").innerHTML = stats.map(([n, label]) =>
    `<div class="stat"><b>${n}</b><span>${label}</span></div>`).join("");

  $("byColumn").innerHTML = Object.entries(r.issues_by_column)
    .map(([col, n]) => `<span class="pill">${esc(col)}: ${n} issue(s)</span>`).join("");

  $("noIssues").hidden = data.issues.length > 0;
  $("issuesTable").innerHTML =
    "<tr><th>Row</th><th>Column</th><th>Value</th><th>Problem</th></tr>" +
    data.issues.map(i =>
      `<tr><td>${i.row}</td><td>${esc(i.column)}</td><td>${esc(i.value) || "(empty)"}</td><td>${esc(i.error)}</td></tr>`).join("");

  fillTable($("beforeTable"), data.headers, data.preview_before);
  fillTable($("afterTable"), data.headers, data.preview_after);
  $("downloadBtn").href = data.download_url;
  $("results").scrollIntoView({ behavior: "smooth" });
}

function fillTable(table, headers, rows) {
  table.innerHTML =
    "<tr>" + headers.map(h => `<th>${esc(h)}</th>`).join("") + "</tr>" +
    rows.map(row => "<tr>" + headers.map(h => `<td>${esc(row[h])}</td>`).join("") + "</tr>").join("");
}

// ---------- history ----------
async function loadHistory() {
  try {
    const { jobs } = await (await fetch("/api/jobs")).json();
    if (!jobs.length) return;
    $("history").innerHTML = jobs.map(j =>
      `<div>🕑 <strong>${esc(j.filename)}</strong> — ${j.report.rows_out}/${j.report.total_rows_in} rows kept,
       ${j.report.total_issues} issue(s) · <a href="/api/download/${j.id}">download cleaned</a></div>`).join("");
  } catch { /* history is a nice-to-have; never break the page for it */ }
}

function showError(msg) { const b = $("errorBox"); b.textContent = "⚠️ " + msg; b.hidden = false; }
function hideError() { $("errorBox").hidden = true; }
loadHistory();
