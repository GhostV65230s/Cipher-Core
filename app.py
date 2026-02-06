import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from transactions import SeafoodTransactions

# ---------------- INIT ---------------- #

if "system" not in st.session_state:
    st.session_state.system = SeafoodTransactions()

system = st.session_state.system

# ---------------- CREDENTIALS ---------------- #

CREDENTIALS = {
    "Fisherman": {"id": "F001", "password": "fish123"},
    "Distributor": {"id": "D001", "password": "dist123"},
    "Transporter": {"id": "T001", "password": "trans123"},
    "Retailer": {"id": "R001", "password": "retail123"},
}

# ---------------- PAGE ---------------- #

st.set_page_config(page_title="Seafood Traceability", layout="wide")
st.title("🐟 Blockchain-Enabled Seafood Supply Chain Traceability")
st.caption("Authority-verified • Tamper-proof • End-to-end transparency")

# ---------------- QR PARAM ---------------- #

qr_batch_id = st.query_params.get("batch_id")

# =================================================
# 🔓 PUBLIC CONSUMER VERIFICATION
# =================================================

if qr_batch_id:
    st.subheader("🔍 Consumer Seafood Verification")
    history = system.get_batch_history(qr_batch_id)

    if history:
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True)
        st.success("✔ Verified immutable blockchain history")
    else:
        st.error("No records found")

    st.stop()

# =================================================
# 🔐 AUTHENTICATION
# =================================================

if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    st.subheader("🔐 Login")

    role = st.selectbox("Select Role", list(CREDENTIALS.keys()))
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == CREDENTIALS[role]["password"]:
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid password")

# =================================================
# 🧠 DASHBOARD
# =================================================

else:
    role = st.session_state.role
    pid = CREDENTIALS[role]["id"]

    st.sidebar.success(f"Logged in as {role}")
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.rerun()

    st.header(f"{role} Dashboard")

    # ---------- FISHERMAN ---------- #
    if role == "Fisherman":
        with st.form("create_batch"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species")
            weight = st.number_input("Weight (kg)", min_value=0.1)
            location = st.text_input("Catch Location")
            certified = st.checkbox("Claim sustainable certification")
            submit = st.form_submit_button("Create Batch")

            if submit:
                res = system.create_batch(pid, batch_id, species, weight, location, certified)
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

    # ---------- DISTRIBUTOR ---------- #
    elif role == "Distributor":
        with st.form("transfer"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species (exact)")
            weight = st.number_input("Weight (exact)", min_value=0.1)
            new_owner = st.text_input("New Owner ID")
            location = st.text_input("Location")
            submit = st.form_submit_button("Transfer")

            if submit:
                res = system.transfer_ownership(pid, batch_id, new_owner, species, weight, location)
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

    # ---------- TRANSPORTER ---------- #
    elif role == "Transporter":
        with st.form("transport"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species (exact)")
            weight = st.number_input("Weight (exact)", min_value=0.1)
            location = st.text_input("Current Location")
            details = st.text_area("Transport Details")
            submit = st.form_submit_button("Update Transport")

            if submit:
                res = system.update_transport(pid, batch_id, species, weight, location, details)
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

    # ---------- RETAILER ---------- #
    elif role == "Retailer":
        st.subheader("🏪 Retail Receipt")

        with st.form("retail_receipt"):
            batch_id = st.text_input("Batch ID")
            species = st.text_input("Species (exact)")
            weight = st.number_input("Weight (exact)", min_value=0.1)
            location = st.text_input("Retail Location")
            submit = st.form_submit_button("Confirm Receipt")

            if submit:
                res = system.retail_receipt(pid, batch_id, species, weight, location)
                if res["success"]:
                    st.success(res["message"])
                else:
                    st.error(res["message"])

        st.subheader("📱 Generate Consumer QR")
        qr_batch = st.text_input("Batch ID for QR")
        if st.button("Generate QR"):
            qr_url = f"http://localhost:8501/?batch_id={qr_batch}"
            qr = qrcode.make(qr_url)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf.getvalue())
            st.code(qr_url)

    # ---------- HISTORY ---------- #
    st.divider()
    st.subheader("🔍 View Batch History")
    query = st.text_input("Batch ID")
    if st.button("View Records"):
        history = system.get_batch_history(query)
        if history:
            st.dataframe(pd.DataFrame(history), use_container_width=True)
        else:
            st.error("No records found")
