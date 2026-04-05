import re

with open('app/main.py', 'r') as f:
    text = f.read()

# 1. Update logout endpoint
logout_repl = """import requests

def logout():
    if st.session_state.user_name:
        try:
            requests.post(f"{API_BASE}/logout", json={"name": st.session_state.user_name}, timeout=3)
        except:
            pass
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.role = None
    st.session_state.login_time = None
    st.session_state.auth_mode = "Login"
    st.rerun()"""
text = re.sub(r'def logout\(\):.*?st\.rerun\(\)', logout_repl, text, flags=re.DOTALL)

# 2. Update auth_page CSS
css_repl = '''    css = """
    <style>
    /* Hide sidebar on login page */
    [data-testid="stSidebar"] { display: none; }
    
    div.stButton > button[kind="primary"] {
        background-color: #38bdf8 !important;
        color: white !important;
        border: 2px solid #38bdf8 !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #94a3b8 !important;
        border: 2px solid #334155 !important;
    }
    div.stButton > button {
        transition: all 0.3s ease;
        font-size: 1.2rem !important;
        padding: 15px !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
    }
    </style>
    """'''
text = re.sub(r'    css = """\n    <style>\n    div.stButton.*?    </style>\n    """', css_repl, text, flags=re.DOTALL)

# 3. Remove Camera from employee_dashboard
# Match from "st.markdown("<br>", unsafe_allow_html=True)" up to "# History Table"
cam_pattern = r'        st\.markdown\("<br>", unsafe_allow_html=True\).*?# History Table'
text = re.sub(cam_pattern, '        # History Table', text, flags=re.DOTALL)

# 4. Update Routing
routing_repl = """# ================= ROUTING =================
login_page = st.Page(auth_page, title="Log In", icon="🔒")

if not st.session_state.authenticated:
    pg = st.navigation([login_page])
else:
    if st.session_state.role == "admin":
        pg = st.navigation({
            "Admin Panels": [
                st.Page(admin_dashboard, title="Admin Dashboard", icon="🛡️"),
                st.Page(attendance_history_page, title="Full Attendance History", icon="📅")
            ],
            "User Access": [
                st.Page(employee_dashboard, title="My Portal", icon="📊")
            ]
        })
    else:
        pg = st.navigation([
            st.Page(employee_dashboard, title="My Portal", icon="📊"),
        ])

pg.run()
"""
text = re.sub(r'# ================= ROUTING =================.*', routing_repl, text, flags=re.DOTALL)

with open('app/main.py', 'w') as f:
    f.write(text)

