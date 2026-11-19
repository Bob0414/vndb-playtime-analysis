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
    """Select works with a score, positive playtime, and at least five votes
    on playtime. Convert their playtime from minutes to hours.
    """
    keep = (
        (data["length_votes"] >= 5)
        & (data["length_minutes"] > 0)
        & data["average"].notna()
    )
    playtimes = data.loc[keep].copy()
    playtimes["length_hours"] = playtimes["length_minutes"] / 60
    return playtimes


def tag_determine(work):
    """Return the qualifying study tags for one visual novel."""
    target_ids = ["g19", "g96", "g104"]
    tags_dict = {}
    for tag in work["tags"]:
        if (tag["id"] in target_ids
                and tag["rating"] >= 2
                and not tag["lie"]):
            if work["title"] not in tags_dict:
                tags_dict[work["title"]] = []
            tags_dict[work["title"]].append(tag["name"])
    return tags_dict


def make_tag_table(data):
    """Build one row per work and qualifying tag for works with scores."""
    tag_rows = []
    for _, work in data.dropna(subset=["average"]).iterrows():
        tag_names = tag_determine(work).get(work["title"], [])
        for tag_name in tag_names:
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
    print("\nAverage scores and rating vote counts by tag")
    print(by_tag[["average", "votecount"]].describe().round(2).to_string())
    save_plots(playtimes, tag_data, FIGURES)
    print("\nSaved playtime_scores.png and scores_by_tag.png to", FIGURES)


if __name__ == "__main__":
    main()
