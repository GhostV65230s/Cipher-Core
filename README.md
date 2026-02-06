# Blockchain-Enabled Seafood Supply Chain Traceability

**Team Name:** Cipher Code

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
git clone <PRIVATE_GITHUB_REPOSITORY_URL>
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

| Role        | Password  |
| ----------- | --------- |
| Fisherman   | fish123   |
| Distributor | dist123   |
| Transporter | trans123  |
| Retailer    | retail123 |




