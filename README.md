# Playtime, Content Tags, and Community Reception of Visual Novels

An independent CSE 163 project by Bob investigating how visual novel
playtime and content tags relate to user scores and voting activity.

## Current progress

- The proposal has been submitted.
- The collected VNDB snapshot contains 4,295 Japanese-original works marked
  as finished, released from 2000 through 2025, with at least 50 rating votes.
- `VN.ipynb` checks missing values, summarizes the main variables, and plots
  playtime against average user score for 1,968 works with at least five
  playtime submissions.
- The notebook also compares scores and vote counts across Mystery, Romance,
  and Comedy. A work can qualify for more than one group.

This project repository is public as required by the Part 2 EDA instructions:
https://courses.cs.washington.edu/courses/cse163/26au/eda/

## Research questions

1. What is the relationship between playtime and average user scores?
2. How do scores and vote counts differ among works with the Mystery,
   Romance, and Comedy tags?
3. Does the playtime-score relationship differ across these tags?

These questions concern associations within the selected VNDB records.
Rating-vote counts do not measure total readership or sales.

## Data source

[VNDB](https://vndb.org/) is a community-maintained visual novel database.
Each work has a record containing information such as its title, release
date, user scores, and user-submitted playtime estimates. Content tags are
labels describing a work's themes or genres, such as Mystery or Romance.
A work can have multiple tags.

- [Kana API documentation](https://api.vndb.org/kana)
- Data-query endpoint: `POST https://api.vndb.org/kana/vn`

An API request asks VNDB for specified records and fields. The server
returns JSON, which the notebook converts into a pandas DataFrame.
The public work queries used here do not require an account or API token.

Important fields include `average` (raw average user score), `rating`
(Bayesian rating), `votecount` (number of rating votes), `length_minutes`
(average submitted playtime in minutes), `length_votes` (number of submitted
playtimes), and `tags` (nested tag records).

Open `VN.ipynb` from the project directory after installing the dependencies
below. If you already have `data/vndb_eda.json`, start at **Load the saved
data for EDA** and run the remaining cells in order.

On a fresh checkout, run the notebook from the top with an internet
connection. The collection cells retrieve the first 200 works and then save
each subsequent page. The complete dataset is saved to `data/vndb_eda.json`.
VNDB changes over time, so a fresh download may give different counts or scores.

## Current local environment

- Python 3.11.9
- VS Code notebook kernel: `CSE163 (Python 3.11)`
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

- `VN.ipynb`: current exploratory notebook.
- `vndb_proposal_draft.md`: editable English proposal draft.
- `output/pdf/vndb_proposal_draft.pdf`: proposal PDF.
- `proposal_feasibility_notes.md`: notes from the preliminary data check.
- `check_environment.py`: local environment check, separate from research code.

## Git and GitHub workflow

Git records local versions. GitHub hosts the uploaded history:
https://github.com/Bob0414/vndb-playtime-analysis

The project currently uses the `main` branch. A separate branch is optional
for an isolated experiment; it is not needed just to upload progress.

After saving changes, inspect them before recording a new version:

```powershell
git status
git diff
git add README.md VN.ipynb
git commit -m "Update project exploration"
git push
git log --oneline
```

Stage whichever specific files you intend to include. Notebook changes must
be saved in VS Code before Git sees them. A local commit is not an off-device
backup; `git push` uploads committed changes to GitHub.

The downloaded data and intermediate collection files are kept locally.
The notebook includes the summary tables and figures from the saved snapshot.

## Dataset and challenge goals

The proposal uses VNDB as the central data source:
https://api.vndb.org/kana

The selected challenge goals are **Messy Data** and **New Library**.
The separate **Multiple Datasets** challenge is not being claimed. Splitting
VNDB records into a work table and a tag table does not automatically turn
them into independent datasets.
