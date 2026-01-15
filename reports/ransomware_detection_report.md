# RansomWatch — Defensive Ransomware Behavior Detection Report

**Project:** RansomWatch (Behavior-based Monitor)  
**Date:** 2026-01-15  
**Environment:** Local machine, monitored folder, Python watchdog + Streamlit

---

## 1) Problem Statement
Ransomware attacks commonly encrypt and rename files rapidly, causing massive data loss. Traditional signature-based defenses may miss new variants.  
A **behavioral detector** can identify ransomware-like activity by observing signals such as:
- High rate of file modifications/renames/deletes
- Extension change spikes
- Entropy increases in file content (encrypted-like randomness)

---

## 2) Objective
Build a safe, educational detection tool that:
- Monitors a folder in real time
- Applies threshold-based behavioral rules
- Generates alerts and logs for investigation

---

## 3) System Design (High Level)
**Data Source:** File system events (create/modify/delete/move)  
**Processing:** Rules within a time window (e.g., 20 seconds)  
**Output:** Alerts + logs + dashboard view

---

## 4) Detection Rules Implemented
1. **MASS_FILE_ACTIVITY**
   - Triggers when total events in window exceed threshold  
2. **EXTENSION_CHANGE_SPIKE**
   - Triggers when too many renames change extensions  
3. **ENTROPY_SPIKE**
   - Triggers when file entropy jumps significantly and crosses threshold  

---

## 5) How to Test (Safe)
1. Start monitor:
   - `python monitor.py`
2. Run dashboard:
   - `streamlit run app_streamlit.py`
3. Generate benign activity:
   - `python monitor.py --safe-test`

**Screenshots to include:**
- Dashboard showing alerts: `reports/screenshots/dashboard_alerts.png`
- Alerts CSV: `reports/screenshots/alerts_csv.png`

---

## 6) Results
Describe:
- Which rules triggered
- Number of events
- Time window used
- Observations

---

## 7) Limitations
- This is a user-space monitor; real EDR uses deeper telemetry (process trees, kernel events).
- Entropy is sampled; small files may be noisy.
- Threshold tuning is needed per environment.

---

## 8) Future Enhancements
- Process correlation (which process modified files)
- Quarantine action (defensive isolation)
- Telegram/Email alerting
- SIEM integration (Syslog / JSON events)
