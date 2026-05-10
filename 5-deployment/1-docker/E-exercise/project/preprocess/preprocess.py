from pandas import json_normalize
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re
from loguru import logger


def bin_time(time):
    if time < datetime(2017, 12, 1):
        return 0
    elif time < datetime(2018, 1, 1):
        return 1
    elif time < datetime(2018, 8, 10):
        return 2
    elif time < datetime(2019, 8, 1):
        return 3
    else:
        return 4


def remove_url(text):
    return re.sub(r'https?:\/\/\S+', '', text)


def preprocess():
    input_file = Path("data/raw/posts.json")
    output_dir = Path("data/processed")
    output_file = output_dir / "posts.parquet"

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return

    logger.info("Loading JSON")

    try:
        with input_file.open() as f:
            data = json.load(f)

        df = json_normalize(data["posts"], sep="_")

    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        return

    logger.info("Processing data")

    df["time"] = pd.to_datetime(df["post_metadata_time"], unit="s")
    df["bintime"] = df["time"].apply(bin_time)

    df["text"] = df["text"].astype(str)
    df["text"] = df["text"].str.replace("\n", " ")
    df["text"] = df["text"].apply(remove_url)
    df["text"] = df["text"].str.lower()

    df["size"] = df["text"].str.len()
    df = df[df["size"] > 50]

    df.reset_index(drop=True, inplace=True)

    if not output_dir.exists():
        logger.info(f"Creating directory {output_dir}")
        output_dir.mkdir(parents=True)

    logger.info(f"Saving to {output_file}")
    df.to_parquet(output_file)

    logger.info("Preprocessing complete")


def main():
    preprocess()


if __name__ == "__main__":
    main()