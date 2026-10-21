# YOUR Role 5 Playbook — API + UI + Deployment (Wed → Fri)

Today is **Wednesday 21 Oct**. Your deadline to the team is **Thursday**.
Presentation is **Friday**. This file is for you personally — it does not
need to go in the final repo (but it does no harm if it does).

## 0. What you own (from your team's table)
| Deliverable | File | Status in this project |
|---|---|---|
| FastAPI API | `main.py` | ✅ Built + tested |
| Dashboard UI | `static/index.html`, `style.css`, `app.js` | ✅ Built |
| Deployment | `render.yaml`, `requirements.txt` | ✅ Ready — you still click deploy on Render |
| API contract for teammates | function signatures below | ✅ Defined — send TODAY |

The other four modules (`ingest/validate/transform/report.py`, `database.py`)
are included as **working fallbacks**. Rule for Thursday:
> If a teammate delivers their module by **Thursday noon**, drop it in
> (same function name/signature) and re-run `pytest`.
> If they don't, the fallback ships and the demo still works.
> **Never let someone else's delay break Friday.**

## 1. Send this to the team TODAY (copy-paste to WhatsApp/GitHub)

---
Hi team — Role 5 (API/UI) is ready for integration. Please keep these exact
function signatures so `main.py` works with everyone's code unchanged:

- Role 1 `ingest.py`: `read_csv_bytes(content: bytes, filename: str) -> (headers, rows)` — raise `ValueError("friendly message")` for bad files
- Role 2 `validate.py`: `validate_rows(rows, headers) -> [{"row":1,"column":"email","value":"x","error":"..."}]`
- Role 3 `transform.py`: `clean_rows(rows, headers) -> (cleaned_rows, duplicates_removed, changes_made)`
- Role 4 `report.py`: `build_report(original, cleaned, issues, duplicates, changes) -> dict` + `database.py`: `init_db() / save_job(...) / list_jobs() / get_job(id)`

Working starter versions of all four are already in the repo on my branch —
improve/replace yours, just keep the signature, then open a PR (no direct
pushes to main). Deadline to swap in: **Thursday 12pm**, after that we freeze
for testing + rehearsal. Demo script is in `DEMO_SCRIPT.md` — check your 45s part.
---

## 2. Wednesday (today) — 90 minutes
1. Run it yourself until it feels boring:
   ```bash
   cd 34-data-cleaning-pipeline
   pip install -r requirements.txt pytest httpx
   pytest -v                       # expect: 8 passed
   uvicorn main:app --reload --port 8000
   ```
   Open http://localhost:8000 → **Use Sample Data** → **Download cleaned CSV**.
   Also try uploading an empty file and a `.txt` — you should see friendly errors.
2. Read `main.py` once, top to bottom. Use the cheat-sheet in §5.
3. Push via Git workflow (§4) and send the team message (§1).
4. Deploy to Render tonight if you can (§3) — do NOT leave this to Friday.

## 3. Deploy to Render (Wednesday night / Thursday morning latest)
1. Repo is on GitHub under `Modigo/34-data-cleaning-pipeline` (merge your PR first).
2. Go to https://render.com → sign in with GitHub.
3. **New + → Blueprint** → pick the repo → Render reads `render.yaml` → **Apply**.
   (Fallback: New + → Web Service → Build: `pip install -r requirements.txt`
   → Start: `uvicorn main:app --host 0.0.0.0 --port $PORT` → Instance: Free.)
4. Wait for **Live** (~2–4 min). Open the URL → Use Sample Data → Download.
   Check `<url>/health` returns `{"status":"ok"}` and `<url>/docs` loads.
5. Paste the live URL into `README.md` (Live demo section), commit via PR.
6. ⚠️ Free tier sleeps after ~15 min idle. **Open the URL Friday 30+ min
   before presenting** and click Use Sample Data once to wake it.

## 4. Git workflow the judges check (15 points — don't push to main!)
```bash
git checkout -b feature/api-ui-deployment
git add main.py static/ requirements.txt render.yaml README.md DEMO_SCRIPT.md
git add ingest.py validate.py transform.py report.py database.py sample_data/ tests/ .gitignore
git commit -m "feat(api): FastAPI endpoints, dashboard UI and Render config (Role 5)"
git push -u origin feature/api-ui-deployment
```
Then GitHub → **Pull Request** → ask a teammate to review → merge.
Small honest commits > one giant dump. Never commit `jobs.db` or `.env` (in `.gitignore`).

## 5. Explain-your-code cheat sheet (judges WILL ask you)
- **`run_pipeline()`** — the only place modules meet: ingest → validate →
  transform → report → save to SQLite → build JSON (report, first 100 issues,
  10-row before/after previews, download URL).
- **`POST /api/upload`** — `UploadFile` gives us the file; `await file.read()`
  gets bytes; any `ValueError` from ingestion becomes **HTTP 400** with the
  friendly message shown in the red banner. App never crashes on bad input.
- **`POST /api/run-sample`** — same pipeline, built-in file. Exists so the
  demo has zero setup friction for judges (usability points).
- **`/api/download/{job_id}`** — looks the run up in SQLite, returns the
  stored cleaned CSV as an attachment; unknown id → **404** (tested).
- **Static UI** — plain `fetch()` with **relative URLs**, so identical code
  works on localhost and Render. Results render from JSON — the UI contains
  no cleaning logic either. Output is HTML-escaped (`esc()`) before display.
- **Your one big technical decision:** *"Orchestration-only API layer —
  `main.py` cleans nothing. Parallel teamwork + swappable modules + each
  module testable alone."* (Second one if pressed: stdlib `csv`, no pandas —
  explainable by beginners, tiny deploy.)

## 6. Thursday — integration day (your real deadline)
- [ ] 12:00 **Feature freeze.** Swap in any teammate modules that arrived; `pytest -v` after each swap.
- [ ] Full manual test: sample flow, own messy CSV, empty file, non-CSV, header-only CSV, download, history.
- [ ] Redeploy (Render auto-deploys on merge to main) and re-test the **live** URL end-to-end.
- [ ] Paste live URL into README; screenshot the report page as backup.
- [ ] **Rehearse `DEMO_SCRIPT.md` out loud with the team, timed.** Each person: contribution + 1 decision.
- [ ] Practise the offline backup once: kill Wi-Fi in your head — `uvicorn main:app --port 8000` locally.
- [ ] Submit the project link on the dashboard when the team lead says go.

## 7. Friday — presentation day
- [ ] 30 min before: open live URL, run sample once (wake Render), open `/docs` in a tab.
- [ ] Tabs ready: 1) App 2) `/docs` 3) Terminal with `pytest -v` already run 4) Downloaded cleaned CSV.
- [ ] You drive the clicks; teammates narrate their module while their output is on screen.
- [ ] Say the disclosure + limitations lines honestly — judges reward it (Scope + safeguards).
- [ ] If anything live fails: switch to localhost backup calmly and say so. A working local demo beats a broken live one.

## 8. Rubric self-check (be able to point at evidence)
| Criterion | Pts | Your evidence |
|---|---|---|
| Core functionality | 25 | Live URL, sample 11→9 rows, download works |
| Engineering/correctness | 20 | 5 modules, validation vs transformation split, 400/404 errors |
| Testing/reliability | 15 | `pytest -v` = 8 passed incl. 4 failure paths |
| Collaboration/Git | 15 | Branch + PR + review per person, Day-1 contract |
| Usability/demo | 10 | One-click sample, before/after preview, plain-English errors |
| Documentation | 10 | README (setup, API table, limitations), this + demo script |
| Scope/delivery | 5 | Small complete MVP, honest "next improvements" |
