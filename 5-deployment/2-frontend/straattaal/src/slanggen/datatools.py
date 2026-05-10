import re
from pathlib import Path

import requests
import torch
from bs4 import BeautifulSoup
from slanggen.custom_logger import logger
from torch.nn.utils.rnn import pad_sequence


def get_data(filename: Path) -> list[str]:
    logger.info("Getting data from local scraping source only")

    # NOTE: URL removed, scraping no longer used externally
    raise RuntimeError(
        "URL-based scraping removed. Use local dataset instead."
    )


def load_data(filename: Path) -> list[str]:
    if not filename.exists():
        logger.info(f"File {filename} not found. expected local dataset file")

        # URL removed → no downloading anymore
        processed_words = get_data(filename)
    else:
        logger.info(f"Loading processed words from {filename}")
        with open(filename, "r", encoding="utf-8") as file:
            processed_words = [line.strip() for line in file]

    logger.info(f"Loaded {len(processed_words)} words")
    return processed_words


def preprocess(corpus: list[str], tokenizer) -> torch.Tensor:
    encoded_sequences = [tokenizer.encode(word).ids for word in corpus]
    padded_sequences = pad_sequence(
        [torch.tensor(seq) for seq in encoded_sequences], batch_first=True
    )
    return padded_sequences


class ShiftedDataset:
    def __init__(self, sequences: torch.Tensor):
        self.X = sequences[:, :-1]
        self.y = sequences[:, 1:]

    def to(self, device):
        self.X = self.X.to(device)
        self.y = self.y.to(device)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

    def __repr__(self):
        return f"ShiftedDataset {self.X.shape}"
