import json
import os
from typing import Any
from .utils.paths import ensure_parent
from .utils.logger import write_json

def read_state(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"events": [], "alerts": []}
    except json.JSONDecodeError:
        return {"events": [], "alerts": []}

def push_event(state_path: str, event: dict) -> None:
    state = read_state(state_path)
    state.setdefault("events", []).append(event)
    # keep it bounded
    state["events"] = state["events"][-500:]
    write_json(state_path, state)

def push_alert(state_path: str, alert: dict) -> None:
    state = read_state(state_path)
    state.setdefault("alerts", []).append(alert)
    state["alerts"] = state["alerts"][-200:]
    write_json(state_path, state)
