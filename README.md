# 🌌 Dreamwalker AI

**Dreamwalker AI** is an autonomous, cross-platform voice and system assistant for PC (Windows) and Android devices. Powered by the Google GenAI SDK (`google-genai`), Python `asyncio`, and native OS/ADB tooling, Dreamwalker AI delivers real-time system execution with robust local security, persistent action auditing, and real-time verification.

---

## 🏗️ Architecture & Core Subsystems

Dreamwalker AI is structured around high-speed tool execution, local security layers ("The Sanctum"), and cross-platform automation:

```
                      +-----------------------------+
                      |     Master Node (main.py)   |
                      +--------------+--------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
+--------v-------+          +--------v-------+          +--------v-------+
| Security Layer |          | Execution Engine|          | Voice Subsystem |
|----------------|          |----------------|          |----------------|
| privacy_masker |          | pc_tools       |          | voice_stream   |
| darkhold_shield|          | phone_tools    |          | (State Machine)|
| ledger (undo)  |          | verifier       |          +----------------+
| guardian daemon|          +----------------+
+----------------+
```

---

## 🛡️ Security & Integrity ("The Sanctum")

1. **The Eye of Agamotto (`ledger.py`)**
   * Classifies actions by risk level (`is_risky`).
   * Prompts for explicit user confirmation (`[y/N]`) before executing high-risk system commands.
   * Maintains persistent audit logging (`sanctum_ledger.json`) allowing voice/text time rewind (`undo`/`rewind`).

2. **Seal the Vault (`privacy_masker.py`)**
   * Scans and redacts passwords, API keys, and PII locally before data ever leaves the machine to external APIs.

3. **Defy the Darkhold (`darkhold_shield.py`)**
   * Scans incoming text, documents, and web content for prompt injection attacks and unauthorized commands.

4. **Pierce the Illusion (`verifier.py`)**
   * Validates OS ground-truth state post-execution (e.g., inspecting process memory via `tasklist` or verifying disk file creation) rather than blindly trusting tool output.

5. **The Watchful Guardian (`guardian.py`)**
   * Continuous background daemon monitoring system health and anomalies without blocking interaction.

---

## ⚙️ Key Tooling Modules

* **PC Automation (`pc_tools.py`)**: 10+ native tools including process launch/close, clipboard management, file system operations, volume control, shell commands with timeouts, and screen captures.
* **Android Talisman (`phone_tools.py`)**: Android Debug Bridge (ADB) automation for screenshots, app launching, coordinate tapping, and text input on connected mobile devices.
* **Routine Engine (`routines.py`)**: Custom multi-step routine registration and persistence across restarts (`sanctum_routines.json`).

---

## 📜 Complete File Directory & Module Purpose

| File Name | Module Description |
| :--- | :--- |
| `main.py` | Central entry point and master node; orchestrates LLM calls, security pipelines, and tool execution. |
| `pc_tools.py` | Windows desktop automation (10+ system function tools). |
| `phone_tools.py` | Android mobile control engine using native Android Debug Bridge (ADB). |
| `ledger.py` | Risk engine authorization, persistent action logging, and Eye of Agamotto rewind logic. |
| `verifier.py` | Post-execution OS state validation (checking `tasklist` and file presence). |
| `privacy_masker.py` | Local sensitive PII and API key masking prior to external transmission. |
| `darkhold_shield.py` | Local prompt injection detection and neutralization engine. |
| `guardian.py` | Background anomaly detection daemon running on an independent thread. |
| `routines.py` | Custom multi-step voice routine manager and JSON persistence engine. |
| `voice_stream.py` | Sound state machine controller (`IDLE`, `LISTENING`, `THINKING`, `SPEAKING`) and audio stream bridge. |
| `.env` | Secret environment file holding API credentials (excluded from version control). |
| `.gitignore` | Git rules excluding sensitive files, virtual environments, and temporary screenshots. |
| `requirements.txt` | Python package dependencies for project setup. |
| `sanctum_ledger.json` | Persistent audit log storage file for action rollbacks. |
| `sanctum_routines.json` | Persistent storage file for user-defined custom routines. |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
* Python 3.10+ (tested on Python 3.14)
* Android Debug Bridge (ADB) installed and added to `PATH` (for mobile features)

### 2. Environment Setup
Clone the repository and set up a virtual environment:

```powershell
# Clone repository
git clone [https://github.com/ankur2603/Dreamwalker-AI.git](https://github.com/ankur2603/Dreamwalker-AI.git)
cd Dreamwalker-AI

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. API Key Configuration
Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run Dreamwalker AI
Launch the master node:

```powershell
.\venv\Scripts\python.exe main.py
```
