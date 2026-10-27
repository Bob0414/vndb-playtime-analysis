# VNDB playtime and content-tag project

This CSE 163 project is currently at the proposal stage. The research
analysis and complete dataset collection have not been implemented yet.

## Current local environment

- Python 3.11.9
- VS Code notebook kernel: `CSE163 (Python 3.11)`
- Interpreter: `C:\Users\baolurier\AppData\Local\Programs\Python\Python311\python.exe`
- Direct project dependencies are recorded in `requirements.txt`.

Run this in a PowerShell terminal opened in the project directory:

```powershell
python check_environment.py
```

The script checks package imports, a pandas/SciPy calculation with artificial
test values, and saving a plot in a temporary directory. It does not download
VNDB data or run the project analysis. The temporary plot is removed afterward.

For another computer or a fresh environment, use Python 3.11 and install the
dependencies before running the check:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe check_environment.py
```

The existing working interpreter on this computer was retained; no new
virtual environment or package installation was needed for the setup check.

## Files

- `Untitled-1.ipynb`: current exploratory notebook.
- `vndb_proposal_draft.md`: editable English proposal draft.
- `output/pdf/vndb_proposal_draft.pdf`: generated proposal PDF, stored locally.
- `proposal_feasibility_notes.md`: notes from the preliminary data check.
- `check_environment.py`: local environment check, separate from research code.

## Local Git workflow

Git records local versions. A GitHub repository is optional remote hosting;
no remote repository is configured by this setup.

After saving changes, inspect them before recording a new version:

```powershell
git status
git diff
git add vndb_proposal_draft.md
git commit -m "Revise project proposal"
git log --oneline
```

Stage whichever specific files you intend to include. Notebook changes must
be saved in VS Code before Git sees them. A local commit is not an off-device
backup; remote backup can be configured separately.

Downloaded data, generated outputs, local environments, and credentials are
ignored by Git. They are not deleted. If needed, small test fixtures can later
be stored under `tests/fixtures/`. The final project will need actual collection
scripts and clear data-access instructions; this README is only the current
setup guide.

## Dataset and challenge goals

The proposal uses VNDB as the central data source:
https://api.vndb.org/kana

The selected challenge goals are **Messy Data** and **New Library**.
The separate **Multiple Datasets** challenge is not being claimed. Splitting
VNDB records into a work table and a tag table does not automatically turn
them into independent datasets.
