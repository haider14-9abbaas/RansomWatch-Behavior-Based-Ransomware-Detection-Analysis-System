from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    # Folder to monitor
    WATCH_PATH: str = "data/watch_folder"

    # Behavioral window for counting events
    WINDOW_SECONDS: int = 20

    # Alert thresholds (tune based on your machine)
    MASS_CHANGE_THRESHOLD: int = 25         # total events (create/modify/move/delete) in window
    EXTENSION_SPIKE_THRESHOLD: int = 10     # number of extension changes in window

    # Entropy threshold (0..8 for byte entropy). Encrypted/random files tend to be high.
    ENTROPY_ALERT_THRESHOLD: float = 7.2

    # File types to compute entropy for (to reduce noise)
    ENTROPY_EXT_ALLOWLIST = {".txt", ".csv", ".log", ".json", ".md", ".html", ".js", ".css"}

    # Logging paths
    EVENTS_CSV: str = "logs/events.csv"
    ALERTS_CSV: str = "logs/alerts.csv"
    STATE_JSON: str = "logs/state.json"
