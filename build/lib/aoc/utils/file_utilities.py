from pathlib import Path
import csv
from typing import Generator

def clear_folder(folder: str) -> None:
    p = Path(folder)
    p.mkdir(parents=True, exist_ok=True)
    for file in p.iterdir():
        file.unlink()

def read_csv(path: str) -> Generator[str, None, None]:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row