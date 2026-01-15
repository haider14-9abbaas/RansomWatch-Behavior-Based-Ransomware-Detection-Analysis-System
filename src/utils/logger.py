import csv
import json
from datetime import datetime
from .paths import ensure_parent

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def append_csv(path: str, row: dict, fieldnames: list[str]) -> None:
    ensure_parent(path)
    exists = False
    try:
        with open(path, "r", encoding="utf-8") as _:
            exists = True
    except FileNotFoundError:
        exists = False

    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            w.writeheader()
        w.writerow(row)

def write_json(path: str, obj: dict) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
