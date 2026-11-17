"""Lightweight source-file integrity checks; not a notebook runtime test."""
import csv
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    notebooks = sorted(
        p for p in root.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts
    )
    datasets = sorted(
        p for p in root.rglob("*.csv") if ".ipynb_checkpoints" not in p.parts
    )

    if not notebooks:
        raise RuntimeError("No Jupyter notebooks found")

    for path in notebooks:
        with path.open(encoding="utf-8") as stream:
            document = json.load(stream)
        if not isinstance(document.get("cells"), list) or not document["cells"]:
            raise ValueError(f"Missing notebook cells: {path}")
        if document.get("nbformat", 0) < 4:
            raise ValueError(f"Unsupported Jupyter notebook format: {path}")
        print(f"OK notebook: {path.relative_to(root)}")

    for path in datasets:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream)
            header = next(reader, None)
            if not header or not all(value.strip() for value in header):
                raise ValueError(f"Missing CSV header: {path}")
        print(f"OK data header: {path.relative_to(root)}")

    print(f"Checked {len(notebooks)} notebook(s) and {len(datasets)} CSV file(s)")


if __name__ == "__main__":
    main()
