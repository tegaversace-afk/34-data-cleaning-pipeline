# Demo Script — Friday (aim: 6 minutes + Q&A)

> Judges score: **Core functionality 25 · Engineering 20 · Testing 15 ·
> Collaboration/Git 15 · Usability/Demo 10 · Docs 10 · Scope 5.**
> Every member must explain **their contribution + one technical decision.**
> Rehearse this exact click-path Thursday. Wake the Render URL Friday morning
> (free tier sleeps — first hit takes ~30–50s).

## Before you start (Role 5 = you, 2 min prep)
- [ ] Open live URL, click **Use Sample Data** once to warm it up, then reload.
- [ ] Have `messy_customers.csv` downloaded locally as backup.
- [ ] Have a terminal ready with `pytest -v` (or screenshot of 8 passed).
- [ ] Backup plan if Wi-Fi/Render dies: run locally —
      `uvicorn main:app --port 8000` → `http://localhost:8000`. Practise this once.

## The script

**[Lead — 30s] Problem + MVP**
"Messy CSVs — bad emails, duplicates, mixed date formats — break every
downstream report. Our MVP takes one messy CSV and returns a quality report
plus a cleaned file. Five modules, five owners, one flow:
Ingest → Validate → Transform → Report → Download."

**[Role 5 — YOU drive the whole live demo, narrate clicks]**
1. Open the homepage. "This dashboard and API are my component —
   `main.py` with FastAPI, plain HTML/CSS/JS in `static/`, deployed on Render."
2. Click **▶ Use Sample Data**. Point at the stat cards:
   "**11 rows in, 9 out, 2 duplicates removed, 19 cells fixed, 10 issues found.**"
3. Hand over *while the screen stays up* ↓

**[Role 1 — Ingestion, 45s]** "My `ingest.py` rejects empty, non-CSV and
>5 MB files with friendly errors — watch:" *(Role 5 uploads an empty .csv →
red error banner appears, app does not crash).* Decision: "stdlib `csv`,
utf-8-sig so Excel exports don't break us."

**[Role 2 — Validation, 45s]** Point at Issues table. "Row 2: `amina.bello@@example`
invalid email; row 4 missing name; age `not_a_number` and `150` caught.
My rules switch on **column names**, so this works on CSVs we've never seen."
Decision: "Validation only *reports* — it never changes data."

**[Role 3 — Transformation, 45s]** Scroll Before → After. "`  John Okafor `
trimmed, email lowercased, `15/02/2024` → `2024-02-15`, exact duplicates
dropped after normalisation." Decision: "Clean first, *then* de-duplicate —
so rows that only differ by spaces/casing still count as duplicates."

**[Role 4 — Reports + Storage, 45s]** Point at stats + Previous runs.
"Every run is summarised and stored in **SQLite** — that's our history list;
each entry can re-download its cleaned file." Decision: "SQLite over Postgres:
zero setup, zero credentials to leak, right-sized for 7 days."

**[Role 5 — YOU close, 60s]**
1. Click **⬇ Download cleaned CSV**, open it briefly. "End-to-end: done."
2. Open `/docs`. "FastAPI gives us interactive API docs for free — every
   endpoint the UI uses is testable here. `/health` is what Render pings."
3. **Your technical decision (say this clearly):** "`main.py` contains zero
   cleaning logic. It only orchestrates the four modules and translates
   errors into HTTP 400s with human messages. That's what let five of us
   build in parallel from Day 2 against fixed function signatures, and it's
   why we could swap in a teammate's improved module without touching the API."
4. Testing: show `pytest -v` → "8 tests: happy path, empty file, non-CSV,
   header-only, unknown download. Failure paths are tested, not just success."
5. Honest limitations: "5 MB cap, SQLite history resets on Render redeploy,
   no auth — synthetic data only. Next: Postgres, configurable rules, bigger files."
6. Disclosure line: "Libraries are FastAPI/Uvicorn plus the Python standard
   library; we used AI pair-programming for scaffolding and can walk through
   any file line by line."

## If judges upload their own CSV
Great — that's why rules are generic. Any CSV with headers will run;
email/age/phone/date checks light up only if those columns exist.

## Judge Q&A — Role 5 answers to have ready
- **"Why FastAPI over Flask?"** Automatic request validation + free `/docs`,
  async file upload, and the team already knew Python — smallest learning curve in 7 days.
- **"What happens with a 100 MB file?"** Rejected at 5 MB by design (MVP scope);
  production answer is streaming/chunked processing — say this, don't bluff.
- **"Is the cleaned file stored forever?"** In SQLite per run; on Render free
  tier the disk is ephemeral, so history resets on redeploy — documented limitation.
- **"How did you integrate five people's code?"** Day-1 contract: fixed function
  signatures per module, branches + PRs, `main.py` as the only integration point.
- **"Security?"** No credentials anywhere, file-type + size checks, output
  escaped in the UI, synthetic data only, no user code is ever executed.
