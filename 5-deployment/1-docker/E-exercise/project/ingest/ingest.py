import requests
from pathlib import Path
from loguru import logger


def download(url, datafile: Path):
    datadir = datafile.parent

    if not datadir.exists():
        logger.info(f"Creating directory {datadir}")
        datadir.mkdir(parents=True)

    if datafile.exists():
        logger.info(f"File {datafile} already exists, skipping download")
        return

    logger.info(f"Downloading {url} to {datafile}")

    try:
        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            with datafile.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        logger.info("Download complete")

    except requests.exceptions.RequestException as e:
        logger.error(f"Download failed: {e}")


def main():
    url = "https://raw.githubusercontent.com/jkingsman/JSON-QAnon/main/posts.json"
    datafile = Path("data/raw/posts.json")
    download(url, datafile)


if __name__ == "__main__":
    main()