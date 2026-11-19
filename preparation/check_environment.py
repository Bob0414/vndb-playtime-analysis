"""Check the local VNDB project environment without downloading any data."""

import sys
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from scipy.stats import spearmanr


def main():
    """Check imports, a small calculation, and saving a temporary plot."""
    print("Python:", sys.version.split()[0])
    print("Interpreter:", sys.executable)
    for package in ["pandas", "requests", "matplotlib", "seaborn",
                    "scipy", "ipykernel"]:
        print(package + ":", version(package))

    # These are artificial test values, not research observations.
    example = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})
    result = spearmanr(example["x"], example["y"])
    assert abs(result.statistic - 1.0) < 0.000001
    assert requests.Session is not None

    with TemporaryDirectory(prefix="vndb_environment_") as directory:
        fig, ax = plt.subplots()
        sns.scatterplot(data=example, x="x", y="y", ax=ax)
        image_path = Path(directory) / "environment_check.png"
        fig.savefig(image_path)
        plt.close(fig)
        assert image_path.stat().st_size > 0

    print("PASS: imports, pandas, SciPy, and plot saving work.")
    print("No research data was downloaded or changed.")


if __name__ == "__main__":
    main()
