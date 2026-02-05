import streamlit as st
import pandas as pd
from transactions import SeafoodTransactions

# ---------------- SAFE INITIALIZATION ---------------- #

if "system" not in st.session_state:
    st.session_state.system = SeafoodTransactions()

system = st.session_state.system

# ---------------- DEMO CREDENTIALS ---------------- #

CREDENTIALS = {
    "Fisherman": {"id": "F001", "password": "fish123"},
    "Distributor": {"id": "D001", "password": "dist123"},
    "Transporter": {"id": "T001", "password": "trans123"},
    "Retailer": {"id": "R001", "password": "retail123"},
}

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Seafood Traceability System",
    layout="wide"
)

st.title("🐟 Blockchain-Enabled Seafood Supply Chain Traceability")
st.caption(
    "Strictly ordered, permissioned blockchain ensuring traceable, verifiable, immutable seafood tracking."
)

# ---------------- SESSION STATE ---------------- #

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- LOGIN ---------------- #

if st.session_state.role is None:
    st.subheader("🔐 Login")

    role = st.selectbox("Select Role", list(CREDENTIALS.keys()))
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == CREDENTIALS[role]["password"]:
            st.session_state.role = role
            st.success(f"Logged in as {role}")
            st.rerun()
        else:
            st.error("Invalid password")

# ---------------- MAIN APP ---------------- #

else:
    role = st.session_state.role
    pid = CREDENTIALS[role]["id"]

    st.sidebar.success(f"Logged in as: {role}")
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.rerun()

    st.divider()
    st.header(f"{role} Dashboard")

    # ================= FISHERMAN ================= #

    if role == "Fisherman":
        st.subheader("🛥️ Step 1 — Create Batch (Source of Truth)")

        with st.form("create_batch"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species")
            weight = st.number_input("Weight (kg)", min_value=0.1)
            location = st.text_input("Catch Location")
            submit = st.form_submit_button("Create Batch")

            if submit:
                res = system.create_batch(pid, batch_id, species, weight, location)
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

    # ================= DISTRIBUTOR ================= #

    elif role == "Distributor":
        st.subheader("📦 Step 2 — Ownership Transfer")

        st.warning("Species and weight must EXACTLY match original batch")

        with st.form("distributor_form"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species (exact match)")
            weight = st.number_input("Weight (exact match)", min_value=0.1)
            new_owner = st.text_input("New Owner ID (e.g., T001)")
            location = st.text_input("Location")
            submit = st.form_submit_button("Transfer Ownership")

            if submit:
                res = system.transfer_ownership(
                    pid, batch_id, new_owner, species, weight, location
                )
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

    # ================= TRANSPORTER ================= #

    elif role == "Transporter":
        st.subheader("🚚 Step 3 — Transport Verification")

        st.warning("Any species or weight mismatch will be rejected")

        with st.form("transport_form"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species (exact match)")
            weight = st.number_input("Weight (exact match)", min_value=0.1)
            location = st.text_input("Current Location")
            details = st.text_area("Transport Details")
            submit = st.form_submit_button("Update Transport")

            if submit:
                res = system.update_transport(
                    pid, batch_id, species, weight, location, details
                )
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

    # ================= RETAILER ================= #

    elif role == "Retailer":
        st.subheader("🏪 Step 4 — Retail & Consumer Verification")
        st.info("Retailers and consumers can only verify data, not modify it.")

    # ================= TRACEABILITY ================= #

    st.divider()
    st.subheader("🔍 End-User Traceability Verification")

    query = st.text_input("Enter Batch ID")

    if st.button("View Traceability"):
        history = system.get_batch_history(query)
        if history:
            df = pd.DataFrame(history)
            df = df.rename(columns={
                "event": "Event",
                "performed_by": "Handled By",
                "species": "Species",
                "weight": "Weight (kg)",
                "location": "Location",
                "timestamp": "Date & Time"
            })
            st.dataframe(df)
            st.success("✔ Immutable, verified, ordered blockchain history")
        else:
            st.error("No records found for this batch")

    # ================= BLOCKCHAIN VALIDATION ================= #

    if st.button("Validate Blockchain Integrity"):
        if system.blockchain.validate_chain():
            st.success("Blockchain is valid and tamper-proof")
        else:
            st.error("Blockchain integrity compromised")
