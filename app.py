import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from transactions import SeafoodTransactions
import base64

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Seafood Blockchain Traceability",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- HELPER: LOAD IMAGE ---------------- #

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Try to load ocean.jpg
try:
    img_base64 = get_base64_of_bin_file("ocean.jpg")
    background_style = f"""
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    """
except FileNotFoundError:
    background_style = """
        background: linear-gradient(-45deg, #006994, #003366, #00c6ff);
    """

# ---------------- CSS STYLING ---------------- #

st.markdown(f"""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif;
    }}

    /* BACKGROUND */
    [data-testid="stAppViewContainer"] {{
        {background_style}
    }}

    /* ---------------- SIDEBAR (DARK TRANSPARENT) ---------------- */
    [data-testid="stSidebar"] {{
        background: rgba(10, 25, 50, 0.85);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }}

    /* Sidebar Text - WHITE */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] div {{
        color: white !important;
    }}

    /* ---------------- BUTTONS (FORCED SKY BLUE) ---------------- */
    .stButton > button, 
    div[data-testid="stFormSubmitButton"] > button {{
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        transition: transform 0.2s;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }}

    .stButton > button:hover, 
    div[data-testid="stFormSubmitButton"] > button:hover {{
        transform: scale(1.02);
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
        color: white !important;
    }}

    /* ---------------- GLASS CARDS (MAIN CONTENT) ---------------- */
    .glass-card {{
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    }}

    /* MAIN CONTENT TEXT - BLACK */
    .glass-card h1, .glass-card h2, .glass-card h3, .glass-card p, .glass-card div {{
        color: black !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.8);
    }}

    h1, h2, h3, h4, h5 {{
        color: black !important;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(255,255,255,0.6);
    }}

    /* ---------------- FORM STYLING ---------------- */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.5);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}

    [data-testid="stForm"] h3, [data-testid="stForm"] p {{
        color: black !important;
    }}

    /* INPUT FIELDS */
    .stTextInput input, .stNumberInput input, .stSelectbox, .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.7) !important;
        color: black !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        border-radius: 10px !important;
    }}

    /* INPUT LABELS */
    .stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label, .stCheckbox label {{
        color: black !important;
        font-weight: 700;
        text-shadow: 0 0 2px rgba(255,255,255,0.8);
    }}
    
    /* CUSTOM LINK BOX FOR QR */
    .qr-link-box {{
        background: rgba(0,0,0,0.6);
        padding: 15px;
        border-radius: 10px;
        color: #00f2fe;
        font-weight: bold;
        text-align: center;
        border: 1px solid #4facfe;
    }}

</style>
""", unsafe_allow_html=True)

# ---------------- INIT SYSTEM ---------------- #

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

# ---------------- PUBLIC CONSUMER VERIFICATION (QR) ---------------- #

qr_batch_id = st.query_params.get("batch_id")

if qr_batch_id:
    st.markdown(f"""
    <div class="glass-card">
        <h1>🔍 Consumer Verification</h1>
        <p>Public Blockchain Record for Batch: <b>{qr_batch_id}</b></p>
    </div>
    """, unsafe_allow_html=True)

    history = system.get_batch_history(qr_batch_id)

    if history:
        # History Table
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(history), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-left: 8px solid #00f260; margin-top: 20px;">
             <h3 style="color: black; margin: 0;">✔ Verified Immutable Record</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("No records found for this Batch ID")

    st.stop()

# ---------------- LOGIN LOGIC ---------------- #

if "role" not in st.session_state:
    st.session_state.role = None

# ================= LOGIN SCREEN ================= #

if st.session_state.role is None:
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 60px;">🌊</div>
            <h1 style="margin: 10px 0;">Cipher Core</h1>
            <p>Secure Seafood Traceability Platform</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("### 🔐 User Login")
            role = st.selectbox("Select Role", list(CREDENTIALS.keys()))
            password = st.text_input("Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("Access Portal")

        if submit_login:
            if password == CREDENTIALS[role]["password"]:
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid credentials")

# ================= DASHBOARD ================= #

else:
    role = st.session_state.role
    pid = CREDENTIALS[role]["id"]

    # ---------------- SIDEBAR ---------------- #
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2921/2921226.png", width=80)

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; margin: 20px 0;">
            <small style="color: #ccc">LOGGED IN AS</small>
            <h2 style="color: white; margin: 0;">{role}</h2>
            <code style="color: #4facfe;">ID: {pid}</code>
        </div>
        """, unsafe_allow_html=True)

        # 1. Logout Button
        if st.button("Logout"):
            st.session_state.role = None
            st.rerun()
        
        st.markdown("---")

        # 2. Blockchain Integrity Check (FIXED METHOD NAME HERE)
        if st.button("Check Blockchain Integrity"):
             # Changed .validate_chain() to .is_valid()
             if system.blockchain.is_valid():
                 st.success("✔ Chain Valid")
             else:
                 st.error("❌ Chain Invalid")

    # ---------------- HEADER ---------------- #

    st.markdown(f"""
    <div class="glass-card">
        <h1>{role} Dashboard</h1>
        <p>Manage your blockchain transactions securely.</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- FISHERMAN VIEW ---------------- #

    if role == "Fisherman":
        with st.form("create_batch"):
            st.markdown("### 🛥️ Register Catch")
            
            c1, c2 = st.columns(2)
            with c1:
                batch_id = st.text_input("Batch ID")
                species = st.text_input("Species")
                certified = st.checkbox("Claim Sustainable Certification")
            with c2:
                weight = st.number_input("Weight (kg)", min_value=0.1)
                location = st.text_input("Catch Location")

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Create Batch")

        if submit:
            res = system.create_batch(pid, batch_id, species, weight, location, certified)
            if res["success"]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-left: 8px solid #00f260;">
                    <h3 style="color: black; margin: 0;">✅ Success!</h3>
                    <p style="color: black;">{res['message']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-left: 8px solid #ff4b4b;">
                    <h3 style="color: black; margin: 0;">❌ Error</h3>
                    <p style="color: black;">{res['message']}</p>
                </div>
                """, unsafe_allow_html=True)

    # ---------------- DISTRIBUTOR VIEW ---------------- #

    elif role == "Distributor":
        with st.form("transfer"):
            st.markdown("### 📦 Ownership Transfer")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                batch_id = st.text_input("Batch ID")
                new_owner = st.text_input("New Owner ID")
            with c2:
                species = st.text_input("Species (Exact)")
                location = st.text_input("Location")
            with c3:
                weight = st.number_input("Weight (Exact)", min_value=0.1)
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Transfer")

        if submit:
            res = system.transfer_ownership(pid, batch_id, new_owner, species, weight, location)
            if res["success"]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-left: 8px solid #4facfe;">
                     <h3 style="color: black; margin: 0;">✅ Success!</h3>
                     <p style="color: black;">{res['message']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(res["message"])

    # ---------------- TRANSPORTER VIEW ---------------- #

    elif role == "Transporter":
        with st.form("transport"):
            st.markdown("### 🚚 Logistics Update")
            
            c1, c2 = st.columns(2)
            with c1:
                batch_id = st.text_input("Batch ID")
                location = st.text_input("Current Location")
                details = st.text_area("Transport Details")
            with c2:
                species = st.text_input("Species (Exact)")
                weight = st.number_input("Weight (Exact)", min_value=0.1)
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Update Transport")

        if submit:
            res = system.update_transport(pid, batch_id, species, weight, location, details)
            if res["success"]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-left: 8px solid #4facfe;">
                     <h3 style="color: black; margin: 0;">✅ Success!</h3>
                     <p style="color: black;">{res['message']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(res["message"])

    # ---------------- RETAILER VIEW ---------------- #

    elif role == "Retailer":
        # 1. Retail Receipt Form
        with st.form("retail_receipt"):
            st.markdown("### 🏪 Confirm Retail Receipt")
            
            c1, c2 = st.columns(2)
            with c1:
                batch_id = st.text_input("Batch ID")
                species = st.text_input("Species (Exact)")
            with c2:
                weight = st.number_input("Weight (Exact)", min_value=0.1)
                location = st.text_input("Retail Location")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Confirm Receipt")

        if submit:
            res = system.retail_receipt(pid, batch_id, species, weight, location)
            if res["success"]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-left: 8px solid #4facfe;">
                     <h3 style="color: black; margin: 0;">✅ Success!</h3>
                     <p style="color: black;">{res['message']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(res["message"])

        # 2. Generate QR Code
        

        st.markdown("""
<div class="card">
<h3>📱 Generate Consumer QR</h3>
</div>
""", unsafe_allow_html=True)
        
        qr_batch = st.text_input("Batch ID for QR")
        if st.button("Generate QR"):
            qr_url = f"http://localhost:8501/?batch_id={qr_batch}"
            qr = qrcode.make(qr_url)
            buf = BytesIO()
            qr.save(buf)
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(buf.getvalue(), width=200)
            with c2:
                st.markdown(f"""
                <div class="qr-link-box">
                    🔗 Scan Link: <span style="color: white;">{qr_url}</span>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- GLOBAL HISTORY (FOR ALL ROLES) ---------------- #
    
   
    st.markdown("""
<div class="card">
<h3>🔎 View Batch History</h3>
</div>
""", unsafe_allow_html=True)

    
    col_search, col_btn = st.columns([3, 1])
    with col_search:
        query = st.text_input("Batch ID", label_visibility="collapsed", placeholder="Enter Batch ID...")
    with col_btn:
        view_history = st.button("View Records")

    if view_history and query:
        history = system.get_batch_history(query)
        if history:
            # Table View
            st.dataframe(pd.DataFrame(history), use_container_width=True)
        else:
            st.error("No records found")
            
    st.markdown('</div>', unsafe_allow_html=True)