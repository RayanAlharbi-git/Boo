from csv import DictReader
from pathlib import Path

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    with path.open("r", encoding="utf-8", newline="") as f:
        return [dict(row) for row in DictReader(f)]



def get_columns(rows: list[dict[str,  str]]) -> list[str]:
    if not rows:
     return []
    return list(rows[0].keys())

