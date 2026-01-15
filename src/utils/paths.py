from pathlib import Path

def ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def safe_suffix(p: str) -> str:
    return Path(p).suffix.lower()
