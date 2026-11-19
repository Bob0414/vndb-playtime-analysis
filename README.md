# Playtime, Content Tags, and Community Reception of Visual Novels

How does visual novel playtime relate to user scores? How do scores and vote
counts vary among works tagged Mystery, Romance, or Comedy?

This CSE 163 project uses data from the [Visual Novel Database (VNDB)](https://vndb.org/).
The saved dataset contains 4,295 completed Japanese-original visual novels
released from 2000 through 2025 with at least 50 rating votes each.

## Project progress

I estimate the project is about 80% complete. The EDA covers missing values,
playtime versus average score, and scores and vote counts by tag. Next I plan
to use SciPy to compare the playtime-score correlation overall and within
each tag, then check how the results change with stricter vote thresholds.

## Run the analysis

From the project directory, use Python 3.11 and install the packages with
`python -m pip install -r requirements.txt`.

The analysis reads `data/vndb_eda.json`. On a fresh checkout, open
[VN.ipynb](VN.ipynb) and run the cells from the top through **Save the
complete dataset** to download the data. On later runs, use the saved
file. A new download can differ as VNDB users add votes and tags.

```sh
python eda.py
python test_eda.py
```

[eda.py](eda.py) prints the summary tables and saves `playtime_scores.png`
and `scores_by_tag.png` in the project directory. The notebook shows both plots
with their interpretations. [test_eda.py](test_eda.py) checks the playtime
and tag rules using small examples.

The playtime analysis uses works with at least five playtime submissions.
For tag comparisons, a work can belong to several groups. Each group
includes works with that tag directly recorded at a tag rating of at least
2 and its lie flag set to false.

## Resources

- [VNDB Kana API](https://api.vndb.org/kana) documents the filters and fields used to collect the works.
- [Python: pathlib basic use](https://docs.python.org/3.11/library/pathlib.html#basic-use) explains how the notebook locates the saved dataset.
- [Python: raising exceptions](https://docs.python.org/3.11/tutorial/errors.html#raising-exceptions) explains the `raise ValueError` checks for incomplete data and repeated work IDs.
