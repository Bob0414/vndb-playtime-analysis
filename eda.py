"""Explore playtime, average scores, and content tags in VNDB."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT = Path(__file__).resolve().parent
DATA_FILE = PROJECT / "data" / "vndb_eda.json"
FIGURES = PROJECT / "output" / "figures"


def load_works(path):
    """Read the saved VNDB collection into a table with one row per work."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Run the data collection cells in VN.ipynb to create {path}."
        )
    with path.open(encoding="utf-8") as file:
        snapshot = json.load(file)
    data = pd.DataFrame(snapshot["records"])
    if snapshot["more"] or not data["id"].is_unique:
        raise ValueError("The snapshot is incomplete or has duplicate IDs.")
    return data


def select_playtimes(data):
    """Keep scored works with positive playtime and at least five estimates."""
    enough_votes = data["length_votes"] >= 5
    has_playtime = data["length_minutes"] > 0
    has_score = data["average"].notna()
    mask = enough_votes & has_playtime & has_score
    playtimes = data[mask].copy()
    playtimes["length_hours"] = playtimes["length_minutes"] / 60
    return playtimes


def study_tags(tags):
    """Return the names of the qualifying tags for one visual novel."""
    target_ids = ["g19", "g96", "g104"]
    names = []
    for tag in tags:
        if (tag["id"] in target_ids
                and tag["rating"] >= 2
                and not tag["lie"]):
            names.append(tag["name"])
    return names


def make_tag_table(data):
    """Build one row per work and qualifying tag for works with scores."""
    tag_rows = []
    scored_works = data[data["average"].notna()]
    for _, work in scored_works.iterrows():
        for tag_name in study_tags(work["tags"]):
            tag_rows.append({
                "id": work["id"],
                "tag": tag_name,
                "average": work["average"],
                "votecount": work["votecount"],
            })
    columns = ["id", "tag", "average", "votecount"]
    tag_data = pd.DataFrame(tag_rows, columns=columns)
    return tag_data.drop_duplicates(subset=["id", "tag"])


def save_plots(playtimes, tag_data, directory):
    """Save the playtime scatter plot and the score distributions by tag."""
    directory.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots()
    sns.scatterplot(data=playtimes, x="length_hours", y="average",
                    alpha=0.4, ax=ax)
    ax.set(title="Playtime and Average User Score",
           xlabel="Playtime (hours)", ylabel="Average user score")
    fig.savefig(directory / "playtime_scores.png", dpi=160,
                bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots()
    sns.boxplot(data=tag_data, x="tag", y="average", ax=ax)
    ax.set(title="Distribution of Average User Scores by Tag",
           xlabel="Content tag", ylabel="Average user score")
    fig.savefig(directory / "scores_by_tag.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    """Print the EDA summaries and save both figures."""
    data = load_works(DATA_FILE)
    print("Rows and columns:", data.shape)
    print("\nMissing values by column")
    print(data.isna().sum())
    print("\nSummary of the main variables")
    columns = ["length_minutes", "average", "votecount", "length_votes"]
    print(data[columns].describe().round(2).to_string())

    playtimes = select_playtimes(data)
    print("\nWorks in the playtime analysis:", len(playtimes))
    tag_data = make_tag_table(data)
    by_tag = tag_data.groupby("tag")
    print("\nWorks per tag")
    print(by_tag["id"].nunique())
    print("\nAverage scores by tag")
    print(by_tag["average"].describe().round(2))
    print("\nRating vote counts by tag")
    print(by_tag["votecount"].describe().round(2))
    save_plots(playtimes, tag_data, FIGURES)
    print("\nSaved playtime_scores.png and scores_by_tag.png to", FIGURES)


if __name__ == "__main__":
    main()
