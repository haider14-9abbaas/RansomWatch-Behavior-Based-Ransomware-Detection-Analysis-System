from __future__ import annotations
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

from .config import Config
from .utils.entropy import shannon_entropy_bytes
from .utils.paths import safe_suffix
from .utils.logger import append_csv, now_iso
from .event_bus import push_alert

EVENT_FIELDS = ["ts", "type", "src_path", "dest_path", "ext_before", "ext_after"]
ALERT_FIELDS = ["ts", "rule", "severity", "details"]

class BehaviorDetector:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.events: list[dict] = []  # in-memory recent events
        self.last_entropy: dict[str, float] = {}  # path -> last entropy

    def _trim_window(self) -> None:
        cutoff = datetime.now() - timedelta(seconds=self.cfg.WINDOW_SECONDS)
        self.events = [e for e in self.events if datetime.fromisoformat(e["ts"]) >= cutoff]

    def record_event(self, ev_type: str, src_path: str, dest_path: Optional[str] = None) -> None:
        src = str(src_path)
        dest = str(dest_path) if dest_path else ""

        ext_before = safe_suffix(src)
        ext_after = safe_suffix(dest) if dest else ext_before

        row = {
            "ts": now_iso(),
            "type": ev_type,
            "src_path": src,
            "dest_path": dest,
            "ext_before": ext_before,
            "ext_after": ext_after,
        }
        self.events.append(row)
        self._trim_window()

        append_csv(self.cfg.EVENTS_CSV, row, EVENT_FIELDS)

        # run rules
        self._rule_mass_change()
        self._rule_extension_spike()
        self._rule_entropy_spike(ev_type, dest_path or src_path)

    def _emit_alert(self, rule: str, severity: str, details: str) -> None:
        alert = {"ts": now_iso(), "rule": rule, "severity": severity, "details": details}
        append_csv(self.cfg.ALERTS_CSV, alert, ALERT_FIELDS)
        push_alert(self.cfg.STATE_JSON, alert)

    def _rule_mass_change(self) -> None:
        n = len(self.events)
        if n >= self.cfg.MASS_CHANGE_THRESHOLD:
            self._emit_alert(
                rule="MASS_FILE_ACTIVITY",
                severity="HIGH",
                details=f"{n} file events within {self.cfg.WINDOW_SECONDS}s (threshold={self.cfg.MASS_CHANGE_THRESHOLD}).",
            )
            # reset window to avoid repeated spam
            self.events = self.events[-max(5, self.cfg.MASS_CHANGE_THRESHOLD // 4):]

    def _rule_extension_spike(self) -> None:
        changes = 0
        for e in self.events:
            if e["type"] in ("moved", "renamed") and e["ext_before"] != e["ext_after"]:
                changes += 1
        if changes >= self.cfg.EXTENSION_SPIKE_THRESHOLD:
            self._emit_alert(
                rule="EXTENSION_CHANGE_SPIKE",
                severity="HIGH",
                details=f"{changes} extension changes within {self.cfg.WINDOW_SECONDS}s (threshold={self.cfg.EXTENSION_SPIKE_THRESHOLD}).",
            )

    def _rule_entropy_spike(self, ev_type: str, path: str) -> None:
        # Only compute entropy for modify/create events and allowlisted extensions
        p = Path(path)
        ext = p.suffix.lower()

        if ev_type not in ("modified", "created"):
            return
        if ext and ext not in self.cfg.ENTROPY_EXT_ALLOWLIST:
            return
        if not p.exists() or not p.is_file():
            return

        try:
            data = p.read_bytes()[:200_000]  # sample first 200KB
        except Exception:
            return

        ent = shannon_entropy_bytes(data)
        prev = self.last_entropy.get(str(p), 0.0)
        self.last_entropy[str(p)] = ent

        # alert if entropy is very high OR big jump
        if ent >= self.cfg.ENTROPY_ALERT_THRESHOLD and (ent - prev) > 0.8:
            self._emit_alert(
                rule="ENTROPY_SPIKE",
                severity="MEDIUM",
                details=f"Entropy increased for {p.name}: {prev:.2f} -> {ent:.2f} (threshold={self.cfg.ENTROPY_ALERT_THRESHOLD}).",
            )
