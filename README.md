# 🛡️ Aegis-SeqGuard: AI Password Anti-Breach Microservice

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-7%20passed-10b981.svg?style=flat-square)](./tests)
[![Defense Grade](https://img.shields.io/badge/defense-active%20lockout-f43f5e.svg?style=flat-square)](#)

> **Aegis-SeqGuard** is a real-time authentication entry sequence anomaly detection microservice. Built with **FastAPI** and **Pydantic**, it uses sliding trajectory window algorithms to intercept ordered credential-stuffing and dictionary attacks while safely allowing legitimate users to retry forgotten passwords.

---

## 🌟 Key Features

- ⚡ **Real-Time Sequence Anomaly Detector**: Computes composite risk scores ($0.0 \rightarrow 1.0$) based on attempt velocity, temporal regularity, single-source origin isolation, and target account diversity.
- 🔒 **Automated Security Lockout Service**: Instantly isolates attack vector IPs and locks target accounts when an anomaly score breaches the threat threshold ($\ge 0.75$).
- 🔐 **Privacy-Preserving Telemetry Anonymizer**: Hashes sensitive account identifiers and IP vectors using salted SHA-256 before trajectory evaluation.
- 📊 **Interactive Command Center Dashboard**: A cyber-security dark-mode web dashboard featuring live risk radar gauges, real-time threat console logs, automated attack simulators, and lockout resolution tools.
- 🧪 **Built-In Attack & Defense Simulators**: One-click interactive simulation triggers for credential-stuffing bot bursts vs. single-user password retries.

---

## 🚀 Quick Start

### 1. Environment Setup

Clone the repository and set up the virtual environment:

```bash
git clone https://github.com/YOUR_USERNAME/Aegis-SeqGuard.git
cd Aegis-SeqGuard

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Application & Command Center

Run the entrypoint script to start the server:

```bash
python src/main.py
```

Open your browser and navigate to:
- 💻 **Interactive Dashboard**: [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)
- 📖 **OpenAPI / Swagger Docs**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

---

## 🧪 Testing & Attack Simulations

### Run Automated Unit & Integration Tests

```bash
source .venv/bin/activate
pytest -v
```

### Run Attack Vector Simulations via CLI

- **Simulate Credential Stuffing Attack**:
  ```bash
  python scripts/simulate_attack.py
  ```
- **Simulate Legitimate User Retries**:
  ```bash
  python scripts/simulate_legit_user.py
  ```

---

## 🧠 How the AI Model Distinguishes Attacks from Legitimate Users

The `AIAnomalyDetector` evaluates a 60-second sliding trajectory window using the composite risk formula:

$$\text{Composite Score} = 0.45 \cdot (\text{Account Diversity} \times \text{IP Isolation}) + 0.35 \cdot \text{Velocity} + 0.20 \cdot \text{Temporal Regularity}$$

| Metric | Legitimate User Retries | Automated Bot Attack |
|---|---|---|
| **Account Target Diversity** | **1 Account** (Low weight $\approx 0.2$) | **5+ Accounts** (High weight $= 1.0$) |
| **Attempt Velocity** | **Human Speed** (2–5 seconds apart) | **Bot Speed** ($\le 50\text{ms}$ intervals) |
| **Temporal Regularity** | **Irregular** (Natural typing delays) | **Precise** (Scripted machine loops) |
| **Outcome Score** | **$\sim 0.35 - 0.47$ (Safe)** | **$1.00$ ($\rightarrow$ AUTOMATED LOCKOUT)** |

---

## 📡 API Endpoint Reference

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/telemetry/ingest` | Ingests raw authentication telemetry and evaluates threat anomaly score. |
| `GET` | `/api/v1/stats` | Retrieves live telemetry metrics (total ingested, lockouts, isolated IPs). |
| `GET` | `/api/v1/lockups/active` | Lists all active security lockouts. |
| `POST` | `/api/v1/lockup/resolve/{lockup_id}` | Resolves an active lockout event and unblocks isolated IPs. |
| `GET` | `/api/v1/incidents` | Fetches historical security incident audit trail. |
| `POST` / `GET` | `/api/v1/simulation/attack` | Server-side trigger for credential-stuffing attack simulation. |
| `POST` / `GET` | `/api/v1/simulation/legit` | Server-side trigger for single-user password retry simulation. |

---

## 📂 Directory Structure

```text
Aegis-SeqGuard/
├── src/
│   ├── api/
│   │   ├── routes.py          # API route definitions
│   │   └── server.py          # FastAPI application server & CORS setup
│   ├── models/
│   │   ├── lockup.py          # Security lockup event models
│   │   ├── telemetry.py       # Raw telemetry & digest models
│   │   └── trajectory.py      # Trajectory window models
│   ├── services/
│   │   ├── anomaly_detector.py # AI sequence order & risk evaluation
│   │   ├── anonymizer.py      # Salted SHA-256 telemetry anonymization
│   │   ├── audit_logger.py    # Audit logging service
│   │   └── lockup_service.py  # Lockout state & IP isolation manager
│   ├── static/
│   │   └── index.html         # Command Center Web Dashboard UI
│   └── main.py                # Server entry point
├── scripts/
│   ├── simulate_attack.py     # Multi-account attack simulation script
│   └── simulate_legit_user.py # Single-user retry simulation script
├── tests/
│   ├── unit/                  # Unit tests for core services
│   └── integration/           # Integration tests for end-to-end flows
├── pyrightconfig.json         # Python static analysis config
├── pytest.ini                 # Pytest configuration
└── requirements.txt           # Python dependencies
```

---

## 📄 License

MIT License © 2026 Aegis-SeqGuard Contributors
