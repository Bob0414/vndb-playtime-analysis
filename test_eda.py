"""
Bob
CSE 163 AE
Check the VNDB analysis rules on a few small examples.
"""

import pandas as pd

from eda import make_tag_table, select_playtimes


def test_select_playtimes() -> None:
    """Keep the five-vote boundary and convert minutes to hours."""
    data = pd.DataFrame({
        "id": ["v1", "v2", "v3", "v4", "v5"],
        "length_votes": [5, 4, 10, 8, 6],
        "length_minutes": [120, 180, None, 0, 90],
        "average": [75, 88, 82, 79, None],
    })
    result = select_playtimes(data)
    assert result["id"].tolist() == ["v1"]
    assert result["length_hours"].tolist() == [2.0]


def test_make_tag_table() -> None:
    """A work can have two qualifying tags even with no playtime."""
    tags = [
        {"id": "g19", "name": "Mystery", "rating": 2, "lie": False},
        {"id": "g104", "name": "Comedy", "rating": 2.5, "lie": False},
        {"id": "g96", "name": "Romance", "rating": 1.5, "lie": False},
        {"id": "g96", "name": "Romance", "rating": 3, "lie": True},
        {"id": "g999", "name": "Other", "rating": 3, "lie": False},
    ]
    data = pd.DataFrame([
        {"id": "v1", "title": "Demo", "average": 78, "votecount": 120,
         "length_minutes": None, "tags": tags},
        {"id": "v2", "title": "Demo 2", "average": 70, "votecount": 50,
         "length_minutes": 90, "tags": []},
    ])
    result = make_tag_table(data)
    assert result["id"].tolist() == ["v1", "v1"]
    assert result["tag"].tolist() == ["Mystery", "Comedy"]
    assert result["average"].tolist() == [78, 78]
    assert result["votecount"].tolist() == [120, 120]


def main():
    test_select_playtimes()
    test_make_tag_table()
    print("Both EDA tests passed.")


if __name__ == "__main__":
    main()
