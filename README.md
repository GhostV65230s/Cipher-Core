# Blockchain-Enabled Seafood Supply Chain Traceability

**Team Name:** Cipher Core

## Problem Statement
The seafood supply chain lacks transparency, making it difficult to verify
where fish was caught, who handled it, and whether sustainability standards
were followed. This leads to fraud, mislabeling, and loss of consumer trust.

Our solution implements a permissioned blockchain-based traceability system
that records every handoff of seafood from fisherman to retailer in an
immutable and verifiable manner.

## Technical Stack ##

### Programming Language
- Python 3

### Frameworks & Libraries
- Streamlit – Web interface and dashboards
- Pandas – Data visualization
- qrcode – QR code generation
- Pillow – Image handling for QR codes
- hashlib – SHA-256 hashing
- datetime – Timestamping blockchain events

### Concepts Used
- Permissioned Blockchain (Simulated)
- Role-Based Access Control (RBAC)
- Smart-contract-like validation logic
- QR-based public verification


## Features
- Permissioned blockchain with hash-linked immutable records
- Role-based access for Fisherman, Distributor, Transporter, and Retailer
- Strict supply chain order enforcement
- Duplicate batch ID prevention
- Immutable species and weight verification at every handoff
- Authority-based sustainable fishing certification
- QR code generation for consumer transparency
- Public read-only verification without login
- Tamper detection through blockchain validation

## 🚀 Setup Instructions

### Step 1: Clone the Repository
--bash
git clone https://github.com/GhostV65230s/Cipher-Core
cd seafood_traceability

## Step 2: Create and Activate Virtual Environment (Recommended)
python -m venv venv

## Windows
venv\Scripts\activate

## macOS / Linux
source venv/bin/activate

## Step 3: Install Dependencies
pip install -r requirements.txt

## Step 4: Run the Application
streamlit run app.py

The application will be available at:
http://localhost:8501

## Login credentials: ##

| Role        | Password  |
| ----------- | --------- |
| Fisherman   | fish123   |
| Distributor | dist123   |
| Transporter | trans123  |
| Retailer    | retail123 |

## 📱 QR Code Verification ##

-QR codes are generated at the Retailer level.

-Scanning the QR opens a public verification page.

-Consumers can view the complete seafood supply chain history
without logging in.

## ⚠️ Limitations

- The blockchain is implemented as a **permissioned, single-node simulation** and does not include distributed consensus or peer-to-peer networking.
- Blockchain data is stored **in memory during runtime** and is not persisted across application restarts.
- Authentication is implemented using **mock credentials** for demonstration purposes.
- Certification authority logic is simulated and not integrated with real-world regulatory databases.
- The system enforces strict weight immutability; real-world scenarios such as spoilage or loss are not currently modeled.

---

## 🚀 Future Scope

- Integrate **persistent storage** (database or distributed ledger) to retain blockchain data across sessions.
- Extend to a **multi-node or decentralized blockchain architecture** with consensus mechanisms.
- Add **cryptographic signatures** to strengthen tamper resistance against privileged attackers.
- Integrate with **external certification authorities or government APIs** for real sustainability verification.
- Introduce **AI-based anomaly detection** for fraud, weight discrepancies, or suspicious transfer patterns.
- Support **mobile-first consumer interfaces** for large-scale QR-based verification.
- Enable **role-to-role transfer constraints** and configurable supply chain workflows.




