import pandas as pd
from pathlib import Path
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
from model import TextClustering


class TextClustering:
    # tijdelijke dummy zodat je pipeline werkt
    def __call__(self, texts, k=100, batch=True, method="PCA"):
        import numpy as np
        return np.random.rand(len(texts), 2)

    def get_labels(self, df):
        import numpy as np
        return np.random.randint(0, 5, size=len(df))


def run_model():
    input_file = Path("data/processed/posts.parquet")
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return None

    logger.info("Loading data")
    df = pd.read_parquet(input_file)

    logger.info("Running clustering")
    clustering = TextClustering()

    X = clustering(df["text"], k=100, batch=True, method="PCA")
    labels = clustering.get_labels(df)

    logger.info("Creating plot")
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, legend=False)

    output_file = output_dir / "clustering.png"
    plt.savefig(output_file)
    plt.close()

    logger.info(f"Saved plot to {output_file}")

    return output_file


def main():
    run_model()


if __name__ == "__main__":
    main()