# VS Code Step-by-Step — Role 5 (based on YOUR screenshot)

Your setup right now: Ubuntu · VS Code · folder `~/34-data-cleaning-pipeline`
· branch `develop` (bottom-left corner) · existing files: `.gitignore`,
`integrate.py`, `rant.py`, `README.md`, `requirements.txt`.
Your terminal (bottom panel) is already open in the right folder. 

**Golden rules:** Save every file with `Ctrl+S` (a dot ● on the tab = unsaved).
Never work directly on `main`/`develop`. Never delete a teammate's file
without asking. Test after every stage, not only at the end.

---
## STAGE 0 — Inspect what already exists (10 min, DO NOT SKIP)

1. In the **Explorer** (left sidebar), click each file and read it:
   `integrate.py` → `rant.py` → `requirements.txt` → `README.md` → `.gitignore`.
   `integrate.py` may already be a teammate's attempt at joining modules —
   your `main.py` must not blindly duplicate/conflict with it.
2. Click in the **Terminal** panel and run, one at a time:
   ```bash
   git status
   git branch -a
   git log --oneline -10
   cat requirements.txt
   ls -la
   ```
3. Get the latest team code (only if `git status` says "working tree clean"):
   ```bash
   git pull
   ```
4. 📸 **Send me** (paste or screenshot): the contents of `integrate.py`,
   `rant.py`, and `requirements.txt`, plus the `git log` output. I will tell
   you if `main.py` needs adapting to a teammate's function names.

## STAGE 1 — Create YOUR branch (2 min)
```bash
git checkout develop
git checkout -b feature/api-ui-deployment
```
✅ Check: bottom-left of VS Code now says `feature/api-ui-deployment`.
(In VS Code you can also click the branch name bottom-left → *Create new branch*.)

## STAGE 2 — Python environment inside VS Code (10 min)
In the Terminal (`Ctrl+`` ` toggles it):
```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]" python-multipart pytest httpx
```
✅ Check: your prompt now starts with `(.venv)`.
Then tell VS Code to use it: `Ctrl+Shift+P` → type **Python: Select Interpreter**
→ pick `.venv/bin/python`. Confirm `.gitignore` contains `.venv/` and `jobs.db`
(add them if missing — never commit these).

## STAGE 3 — Create the file structure (5 min)
Either right-click in Explorer → **New Folder / New File**, or faster in Terminal:
```bash
mkdir -p static sample_data tests
touch main.py ingest.py validate.py transform.py report.py database.py
touch static/index.html static/style.css static/app.js
touch sample_data/messy_customers.csv tests/test_api.py render.yaml
```
Target tree (existing `integrate.py` / `rant.py` stay untouched for now):
```
34-data-cleaning-pipeline/
├── main.py            ★ YOU (Role 5)
├── static/            ★ YOU — index.html, style.css, app.js
├── render.yaml        ★ YOU — deployment
├── requirements.txt   (exists — merge, don't blindly overwrite)
├── ingest.py  validate.py  transform.py  report.py  database.py   (Roles 1–4 / fallbacks)
├── sample_data/messy_customers.csv
├── tests/test_api.py
├── integrate.py  rant.py   ← inspect in Stage 0; ask owners before touching
└── README.md
```

## STAGE 4 — Put the code in (30–45 min)
**Option A (fastest):** download `role5-starter.zip` from this chat, unzip it
to a *separate* folder (e.g. `~/Downloads/role5/`), then copy files one-by-one
into your repo. Do NOT unzip over your repo — you'd overwrite your existing
`README.md` / `requirements.txt` and team files.

**Option B:** open each file in the Arena workspace, `Ctrl+A` → `Ctrl+C`,
click the same file in VS Code, `Ctrl+A` → `Ctrl+V` → `Ctrl+S`.

Copy in this order (dependencies first, yours last so you understand them best):
`ingest.py` → `validate.py` → `transform.py` → `report.py` → `database.py` →
`sample_data/messy_customers.csv` → **`main.py`** → `static/index.html` →
`static/style.css` → `static/app.js` → `tests/test_api.py` → `render.yaml`.
For `requirements.txt`, make sure yours ends up containing exactly:
```
fastapi
uvicorn[standard]
python-multipart
```
Read `main.py` top-to-bottom as you paste it — judges will ask YOU about it.

## STAGE 5 — Run it in VS Code (10 min)
Terminal 1 (with `(.venv)` active, from the project folder — you already are):
```bash
uvicorn main:app --reload --port 8000
```
`Ctrl+click` the `http://127.0.0.1:8000` link, then test in the browser:
1. Click **▶ Use Sample Data** → expect 11 in / 9 out / 2 duplicates / 10 issues
2. **Download cleaned CSV** → open the file, check dates look like `2024-02-15`
3. Upload an empty `.csv` → red friendly error (app must NOT crash)
4. Open `http://localhost:8000/docs` and `http://localhost:8000/health`
Stop the server with `Ctrl+C`. (`--reload` = auto-restarts when you save code.)

## STAGE 6 — Run the automated tests (5 min)
Click the **+** in the Terminal panel to open a second terminal, activate
the venv again (`source .venv/bin/activate`), then:
```bash
pytest -v
```
✅ Expect: **8 passed**. Screenshot this — it's evidence for the 15-pt Testing criterion.

## STAGE 7 — Commit with VS Code Source Control (10 min)
1. Click the **Source Control icon** (branch/fork icon, left sidebar).
2. Review every changed file. You should NOT see `.venv/` or `jobs.db`.
3. Click **+** next to files to stage. Commit in small, honest chunks, e.g.:
   - `feat(api): add FastAPI app in main.py (Role 5)`
   - `feat(ui): add dashboard in static/`
   - `chore(deploy): add render.yaml and requirements`
   - `test: add API tests for happy and failure paths`
4. Type the message → **Commit** → repeat. (Terminal equivalent: `git add`, `git commit -m`, `git status`.)

## STAGE 8 — Push + Pull Request (10 min)
```bash
git push -u origin feature/api-ui-deployment
```
GitHub → your repo → **Compare & pull request** → base branch: **`develop`**
(confirm with your lead, Tega — screenshot shows `develop` is your working
branch) → write what you built + how to test it → request a teammate review → merge after approval.
🚫 Never `git push` straight to `main` — the brief explicitly forbids it.

## STAGE 9 — Deploy on Render (after merge, Wed night/Thu morning)
render.com → **New + → Blueprint** → select repo (reads `render.yaml`) → **Apply** →
wait for **Live** → test live URL end-to-end (sample, error, download, `/health`) →
paste URL into `README.md` via a new small PR.
⚠️ Friday: open the URL **30 min before** presenting to wake the free tier.

## STAGE 10 — Thursday integration
- `git checkout develop && git pull` → new branch or update yours → swap in
  teammates' real modules (same signatures — see ROLE5_GUIDE §1) →
  `pytest -v` after EACH swap → full browser test → freeze features at noon →
  rehearse `DEMO_SCRIPT.md` → practise offline backup (`uvicorn main:app --port 8000`).

---
## Common VS Code errors — quick fixes
| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'fastapi'` | venv not active / wrong interpreter | `source .venv/bin/activate`, re-run `pip install ...`, check interpreter (Stage 2) |
| `Address already in use` (port 8000) | old server still running | `Ctrl+C` it, or use `--port 8001` |
| Page loads but buttons do nothing / 404 on `/static/...` | server started from wrong folder | `Ctrl+C`, `cd ~/34-data-cleaning-pipeline`, start again |
| Changes don't appear in browser | file unsaved (● on tab) | `Ctrl+S`, `--reload` restarts, hard-refresh browser `Ctrl+Shift+R` |
| `pytest: command not found` | pytest not in this venv/terminal | activate venv, `pip install pytest httpx` |
| Git says merge conflict | teammate edited same file | Don't panic/delete: open file, VS Code highlights `<<<<<<< ======= >>>>>>>`, pick correct lines, save, stage, commit — or send me a screenshot first |
| Accidental file in commit (`.venv`, `jobs.db`) | missing `.gitignore` entry | Add to `.gitignore`, `git rm -r --cached .venv jobs.db` |

## VS Code shortcuts you'll use all week
`Ctrl+S` save · `Ctrl+`` ` terminal · `Ctrl+P` jump to file · `Ctrl+Shift+P`
command palette · `Ctrl+Shift+F` search whole project · `Ctrl+/` comment line
