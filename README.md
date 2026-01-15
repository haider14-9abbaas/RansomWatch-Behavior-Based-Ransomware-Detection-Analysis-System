# 🛡️ RansomWatch — Ransomware Behavior Detection System (Defensive Project)

> ⚠️ **Disclaimer:**  
> This project is created strictly for **educational and defensive cybersecurity research**.  
> It does NOT create malware or encrypt files. It only **detects ransomware-like behavior patterns** in a monitored folder.

---

## 🎯 Project Objective

The objective of this project is to design a **behavior-based ransomware detection system** that can identify suspicious file activity such as:

- Rapid file modifications
- Mass renaming of files
- Sudden extension changes
- High-entropy file content (encrypted-like data)

Instead of relying on known malware signatures, this system focuses on **behavioral indicators**, which are commonly used in modern **EDR (Endpoint Detection and Response)** systems.

---

## 🧠 Problem Statement

Ransomware attacks cause massive damage by:

- Encrypting large numbers of files in seconds
- Renaming file extensions
- Deleting or replacing original data

Traditional antivirus systems mostly rely on **signature-based detection**, which fails when:

- A new ransomware variant appears
- Attackers use obfuscation techniques

Students usually learn ransomware only in theory and do not understand **how real detection systems work internally**.

There is a need for a system that demonstrates **how ransomware can be detected using behavior analysis instead of signatures**.

---

## ✅ Proposed Solution

We developed **RansomWatch**, a defensive monitoring tool that:

- Observes file system activity in real time
- Applies rule-based behavioral detection
- Triggers alerts when suspicious activity crosses thresholds
- Logs events for investigation
- Displays alerts on a dashboard

This project follows a **Detection & Incident Response** learning model used in SOC environments.

---

## ⚙️ System Architecture

**Input:**  
File system events (Create, Modify, Delete, Rename)

**Processing:**  
Behavior analysis using time-window thresholds

**Detection Rules:**  
- Mass file activity detection  
- Extension change spike detection  
- Entropy spike detection

**Output:**  
- Alert generation  
- Event logs  
- Dashboard visualization

---

## 🔥 Detection Rules Implemented

| Rule Name | Description |
|--------|------------|
| MASS_FILE_ACTIVITY | Detects many file changes in short time window |
| EXTENSION_CHANGE_SPIKE | Detects mass renaming of file extensions |
| ENTROPY_SPIKE | Detects encrypted-like randomness in files |

These rules simulate how modern endpoint security tools detect ransomware.

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Monitoring:** watchdog (file system events)
- **Dashboard:** Streamlit
- **Data Processing:** Pandas
- **Logging:** CSV + JSON

---

## 📁 Project Structure

RansomWatch/
│── monitor.py
│── app_streamlit.py
│── requirements.txt
│── README.md
│
├── src/
│ ├── detector.py
│ ├── event_bus.py
│ ├── config.py
│ └── utils/
│ ├── entropy.py
│ ├── logger.py
│ └── paths.py
│
├── data/
│ └── watch_folder/ # Folder under monitoring
│
├── logs/
│ ├── events.csv
│ ├── alerts.csv
│ └── state.json
│
└── reports/
└── ransomware_detection_report.md

yaml
Copy code

---

## 🚀 How to Run the Project

### 🔹 Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
🔹 Step 2 — Start Monitor (Terminal 1)
bash
Copy code
python monitor.py
This starts real-time monitoring of:

bash
Copy code
data/watch_folder/
🔹 Step 3 — Start Dashboard (Terminal 2)
bash
Copy code
python -m streamlit run app_streamlit.py
Open in browser:

arduino
Copy code
http://localhost:8501
🔹 Step 4 — Safe Testing (No Malware)
To generate benign activity and test alerts:

bash
Copy code
python monitor.py --safe-test
This simulates:

File edits

File renames

New file creation

⚠️ No encryption or malicious activity is performed.

🧪 Testing Methodology
Testing includes:

Rapid file creation

Extension renaming

File content randomization

Monitoring alert triggers

Alerts are validated using:

Dashboard view

logs/alerts.csv

logs/events.csv

📝 Report Documentation
A structured security report is provided at:

bash
Copy code
reports/ransomware_detection_report.md
It includes:

Problem statement

Detection rules

Test methodology

Results

Limitations

Future improvements

🎓 Learning Outcomes
Through this project, students learn:

How ransomware behaves at file-system level

Behavioral detection logic

Incident detection workflows

Security monitoring concepts

SOC alert analysis approach

This project is suitable for:

Cybersecurity students

SOC analyst training

Blue team practice labs

🚧 Limitations
User-space monitoring only (no kernel telemetry)

No process-level correlation

Threshold tuning required per system

This is a learning-oriented prototype, not a production EDR system.

🔮 Future Enhancements
Process-based detection

Automatic file quarantine

Email / Telegram alerts

Integration with SIEM

Machine learning anomaly detection

👨‍💻 Developers
Name	LinkedIn	GitHub
Muhammad Hamza Kamran	🔗 https://www.linkedin.com/in/hamza-kamran-271872297/	🐙 https://github.com/Hamza-hani


