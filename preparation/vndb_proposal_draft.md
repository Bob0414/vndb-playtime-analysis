# Playtime, Content Tags, and Community Reception of Visual Novels
Bob | CSE 163 | Project Proposal | October 27, 2026

## Research Questions
1. What is the relationship between visual novel playtime and average user scores? I will examine whether longer works tend to receive higher scores within the eligible dataset.
2. How do average user scores and vote counts differ among works with the Mystery, Romance, and Comedy tags? I will compare score distributions and typical voting activity, rather than treating vote counts as total readership.
3. Does the relationship between playtime and average user scores differ across these three tags? I will compare the direction and strength of the relationship within each tag, recognizing that a work can have multiple tags.

## Motivation
I enjoy reading visual novels and am interested in how their length and subject matter relate to readers' evaluations. Some require many hours to complete, while others offer much shorter experiences. Comparing these characteristics could help describe whether the apparent relationship between length and evaluation is consistent across different kinds of stories. This project will examine associations, not prove that longer stories cause higher scores.

## Dataset and Scope
I will use the public VNDB Kana API [1]. Each observation will represent one visual novel. I plan to include Japanese-original works marked as finished, released from 2000 through 2025, with at least 50 rating votes at collection time. This covers completed calendar years and sets a practical participation floor without selecting only high scores. The conclusions will concern this eligible VNDB cohort, not all visual novels.

I will retrieve IDs, titles, release dates, average scores, Bayesian ratings, rating-vote counts, playtime estimates, playtime-vote counts, and nested tag records. The API reports playtime in minutes. For tag membership, I will use directly recorded Mystery (g19), Romance (g96), and Comedy (g104) tags with tag rating at least 2, excluding records marked as a lie. I will not automatically include child tags. Tag rating measures the tag association, not the work's review score.

A feasibility query on October 27 found 4,272 works meeting the proposed cohort criteria, before exclusions for missing playtime or insufficient playtime submissions. Before applying the 50-vote threshold, a preliminary check of three selected ID-sorted pages from the broader cohort found substantial variation in missingness. These pages are not a random sample and will not be used to estimate population rates. The API requests and raw responses will be saved with a collection timestamp so the analysis can be reproduced from a fixed snapshot.

## Challenge Goals
**Messy Data:** I will collect paginated API responses, handle request failures and rate limits, normalize nested tags into a VN-tag table, validate dates and numeric values, remove duplicate IDs, and document missingness and exclusions. All cleaning will be implemented in Python.

**New Library:** I plan to learn SciPy [2] and use its Spearman correlation function to answer Questions 1 and 3. This will add numerical summaries of association to the visual analysis. I will learn how to interpret the coefficient and handle missing or constant inputs, rather than treating a library output as an explanation by itself.

## Method
**Collection and cleaning.** I will send POST requests to https://api.vndb.org/kana/vn using original-language, development-status, release-date, and vote-count filters. I will retrieve up to 100 records per request in ID order and continue while the response reports more records, following the documented ID-pagination approach. I will save the exact queries and raw JSON, then create a deduplicated VN table and a separate tag-membership table. Partial release dates with a known year will be retained; unknown years will be excluded by the date criteria. An accompanying script and README will explain downloading and rebuilding the tables.

**Question 1.** I will retain records with a nonmissing average score, positive playtime, and at least five playtime submissions. I will convert minutes to hours, plot playtime against average score, and use scipy.stats.spearmanr to summarize whether higher playtime tends to accompany higher scores. Spearman correlation is appropriate for an increasing or decreasing tendency without assuming a straight-line relationship. I will also inspect the plot for patterns a single coefficient could miss.

**Question 2.** I will use all eligible records with nonmissing scores and the selected tag, including those without playtime. For each tag, I will report the number of works, median and interquartile range of scores and vote counts, and distribution plots. This will show whether tags with more voting activity also have higher scores. Each work counts once within a tag but may appear in multiple tag groups; the groups will not be treated as independent samples or added together to estimate unique works.

**Question 3.** Within each selected tag, I will apply the Question 1 eligibility rules and calculate a separate Spearman coefficient alongside a scatter plot. I will report group sizes and compare coefficients descriptively, without claiming a formal difference between overlapping groups. Groups with fewer than 30 eligible works or constant values will be reported as insufficient for a stable comparison. I will not replace a tag merely because its results are uninteresting.

**Reliability and limitations.** I will report how many records each rule removes, compare included and excluded works by year and vote count, and repeat Questions 1 and 3 using stricter floors of 100 rating votes and 10 playtime submissions. I will also check whether the broad pattern changes across release periods (2000-2009, 2010-2019, and 2020-2025) or when using Bayesian rating instead of raw average. These checks assess stability but do not eliminate selection bias. Participation is voluntary; playtime and scores may come from different users, tags overlap, and works in the same series may be related. Missing playtime will not be replaced with zero.

## Work Plan and Development
I plan to work independently using the existing local Python 3.11 environment, VS Code, pandas, requests, seaborn, and matplotlib. The Notebook will support exploration; collection, cleaning, and analysis will be moved into runnable Python scripts. The local Python environment has been verified by running a Python script, and a local Git repository is already in use. I will keep course project materials private unless the instructor permits sharing.

1. Learn the needed SciPy concepts and finalize tag definitions and collection rules: 3 hours.
2. Implement API pagination, retries, and saved raw-data snapshots: 4 hours.
3. Clean data, build tag membership, and write validation tests: 4 hours.
4. Complete the three analyses, plots, and sensitivity checks: 5 hours.
5. Write the report, document reproduction steps, and test a clean rerun: 4 hours.

Total estimate: 20 hours. Tests will cover duplicate IDs, threshold boundaries, missing values, and overlapping tags using small fixtures; saved API responses will avoid repeated network calls during tests. If collection is slow, I will cache progress and resume. If a tag has too few usable works, I will report that limitation rather than lower standards to obtain a preferred result.

## Sources
[1] VNDB Kana API documentation and data access: https://api.vndb.org/kana
[2] SciPy Spearman correlation documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
