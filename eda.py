"""
Bob
CSE 163 AE
Explore playtime, average scores, and content tags in VNDB.
"""

import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_works(path: str) -> pd.DataFrame:
    """Read the VNDB file at path and return a table with one row per work.

    Raise ValueError if more pages are pending or a work ID is repeated.
    """
    with open(path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    works = saved_data["records"]
    data = pd.DataFrame(works)

    if saved_data["more"]:
        raise ValueError("There are more VNDB pages to collect.")
    work_ids = data["id"]
    if not work_ids.is_unique:
        raise ValueError("The data contains repeated work IDs.")
    return data


def select_playtimes(data: pd.DataFrame) -> pd.DataFrame:
    """Return works in data with a score, positive playtime, and at least
    five playtime estimates. Include their playtime in hours.
    """
    enough_votes = data["length_votes"] >= 5
    has_playtime = data["length_minutes"] > 0
    has_score = data["average"].notna()
    keep = enough_votes & has_playtime & has_score
    playtimes = data[keep].copy()
    playtimes["length_hours"] = playtimes["length_minutes"] / 60
    return playtimes


def get_study_tags(tags: list) -> list:
    """Return the study tag names rated at least 2 and not flagged as lies
    in one work's list of VNDB tags. Return an empty list if none qualify.
    """
    target_ids = ["g19", "g96", "g104"]
    names = []
    for tag in tags:
        if (tag["id"] in target_ids
                and tag["rating"] >= 2
                and not tag["lie"]):
            names.append(tag["name"])
    return names


def make_tag_table(data: pd.DataFrame) -> pd.DataFrame:
    """Return one row per scored work and qualifying tag in data.

    Each row includes the work ID, tag name, average score, and vote count.
    """
    has_score = data["average"].notna()
    scored_works = data[has_score].copy()
    scored_works["tag"] = scored_works["tags"].apply(get_study_tags)
    columns = ["id", "tag", "average", "votecount"]
    tag_table = scored_works[columns].explode("tag")
    tag_table = tag_table[tag_table["tag"].notna()]
    return tag_table.drop_duplicates(["id", "tag"], ignore_index=True)


def save_plots(playtimes: pd.DataFrame, tag_data: pd.DataFrame) -> None:
    """Plot hours vs. score from playtimes and scores by tag from tag_data.

    Save both figures as PNG files in the current working directory.
    """
    fig, ax = plt.subplots()
    sns.scatterplot(data=playtimes, x="length_hours", y="average",
                    color="black", alpha=0.3, ax=ax)
    ax.set(title="Playtime and Average User Score",
           xlabel="Playtime (hours)", ylabel="Average user score")
    fig.savefig("playtime_scores.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots()
    sns.boxplot(data=tag_data, x="tag", y="average", color="lightgray", ax=ax)
    ax.set(title="Distribution of Average User Scores by Tag",
           xlabel="Content tag", ylabel="Average user score")
    fig.savefig("scores_by_tag.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    data = load_works("data/vndb_eda.json")
    print("Rows and columns:", data.shape)
    missing = data.isna()
    missing_counts = missing.sum()
    print("Missing values by column")
    print(missing_counts)

    columns = ["length_minutes", "average", "votecount", "length_votes"]
    main_variables = data[columns]
    summary = main_variables.describe()
    summary = summary.round(2)
    print("Summary of the main variables")
    print(summary)

    playtimes = select_playtimes(data)
    print("Works in the playtime analysis:", len(playtimes))
    tag_data = make_tag_table(data)
    by_tag = tag_data.groupby("tag")
    work_counts = by_tag["id"].nunique()
    print("Works per tag")
    print(work_counts)

    score_summary = by_tag["average"].describe()
    score_summary = score_summary.round(2)
    print("Average scores by tag")
    print(score_summary)

    vote_summary = by_tag["votecount"].describe()
    vote_summary = vote_summary.round(2)
    print("Rating vote counts by tag")
    print(vote_summary)

    save_plots(playtimes, tag_data)
    print("Saved playtime_scores.png and scores_by_tag.png.")


if __name__ == "__main__":
    main()
