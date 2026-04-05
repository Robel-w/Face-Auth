import sys
import os
import streamlit as st
import requests
import datetime
import pandas as pd
import time

st.set_page_config(page_title="FaceTrack | Attendance", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
from app.ui import inject_custom_components
inject_custom_components()

import os
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8001/api")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.role = None
    st.session_state.login_time = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

import requests

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
    st.rerun()

def render_header():
    """Renders the top header for authenticated dashboards."""
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([6, 4])
    with c1:
        st.markdown("<h3 style='margin: 0; color: #38bdf8;'>🛡️ FaceTrack</h3>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='text-align: right; margin-top: 10px; color: #f8fafc; font-size: 1.1rem;'><strong>{st.session_state.user_name}</strong> | {st.session_state.role.capitalize()}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)
    
    # We will also add Logout to sidebar here so it appears on all authenticated pages
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            logout()

def fetch_attendance_data():
    try:
        resp = requests.get(f"{API_BASE}/attendance")
        if resp.status_code == 200:
            data = resp.json()
            if not data:
                return pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])
            df = pd.DataFrame(data)
            if not df.empty and "Date" in df.columns:
                df = df.sort_values(by=["Date", "Time"], ascending=[False, False]).reset_index(drop=True)
            return df
    except Exception:
        pass
    return pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])

# ================= LOGIN / REGISTER (UNAUTHENTICATED) =================
def auth_page():
    st.markdown("<h3 style='margin-bottom: 2rem; color: #38bdf8;'>🛡️ FaceTrack</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #f8fafc;'>Welcome</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Sign in seamlessly with your face.</p><br>", unsafe_allow_html=True)
    
    # BIG CENTERED LOGIN/REGISTER CONSTROLS
    css = """
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
    """
    st.markdown(css, unsafe_allow_html=True)

    spacer_left, col_login, col_reg, spacer_right = st.columns([3, 2, 2, 3])
    with col_login:
        if st.button("Login", use_container_width=True, type="primary" if st.session_state.auth_mode == "Login" else "secondary"):
            st.session_state.auth_mode = "Login"
            st.rerun()
    with col_reg:
        if st.button("Register", use_container_width=True, type="primary" if st.session_state.auth_mode == "Register" else "secondary"):
            st.session_state.auth_mode = "Register"
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.auth_mode == "Login":
            st.markdown("<div style='text-align:center; color:#cbd5e1; margin-bottom:10px;'>Face detection box: Position your face inside.</div>", unsafe_allow_html=True)
            camera_img = st.camera_input("Face Scan", label_visibility="collapsed")
            if camera_img:
                if st.button("Capture Face & Login", type="primary", use_container_width=True):
                    with st.spinner("Verifying face..."):
                        try:
                            files = {"image": camera_img.getvalue()}
                            resp = requests.post(f"{API_BASE}/verify-face", files=files)
                            data = resp.json()
                            if resp.status_code == 200 and data.get("success"):
                                name = data.get("name")
                                st.success(f"Welcome back, {name}!")
                                st.session_state.user_name = name
                                st.session_state.login_time = data.get("loginTime")
                                st.session_state.authenticated = True
                                admin_users = os.getenv("ADMIN_USERS", "admin,yabets maregn,yabet").split(",")
                                is_admin = any(admin.strip().lower() in name.lower() for admin in admin_users)
                                
                                if is_admin:
                                    st.session_state.role = "admin"
                                else:
                                    st.session_state.role = "employee"
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(data.get("message", "Access Denied. Face not recognized."))
                        except Exception as e:
                            st.error(f"Error connecting to backend: {e}")

        elif st.session_state.auth_mode == "Register":
            emp_id = st.text_input("Employee ID / Name", placeholder="e.g., John Doe")
            st.markdown("<div style='text-align:center; color:#cbd5e1; margin-bottom:10px;'>Align face correctly for accurate registration.</div>", unsafe_allow_html=True)
            reg_cam = st.camera_input("Register Scan", label_visibility="collapsed")
            if reg_cam and emp_id:
                if "admin" in emp_id.lower() or "yabet" in emp_id.lower():
                    st.error("Registration Denied: Cannot register as admin.")
                else:
                    if st.button("Capture Face & Register", type="primary", use_container_width=True):
                        with st.spinner("Processing variants & training ML model..."):
                            try:
                                files = {"image": reg_cam.getvalue()}
                                resp = requests.post(f"{API_BASE}/register", data={"employee_id": emp_id}, files=files)
                                data = resp.json()
                                if resp.status_code == 200 and data.get("success"):
                                    st.success(data.get("message", "Registered successfully!"))
                                else:
                                    st.error(data.get("message", "Registration failed."))
                            except Exception as e:
                                st.error(f"Error connecting to backend: {e}")

    st.markdown("<p style='text-align: center; color: #64748b; margin-top: 5rem; font-size: 0.9rem;'>&copy; 2026 FaceTrack Auth System. All rights reserved.</p>", unsafe_allow_html=True)

# ================= EMPLOYEE DASHBOARD =================
def employee_dashboard():
    render_header()
    
    # Live Clock
    curr_time = datetime.datetime.now().strftime("%I:%M %p")
    st.markdown(f"<h1 style='text-align: center; font-size: 4rem; color: #f8fafc; font-weight: bold; margin-bottom: 0;'>{curr_time}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; margin-top: 0;'>{datetime.datetime.now().strftime('%A, %B %d, %Y')}</p>", unsafe_allow_html=True)
    
    df = fetch_attendance_data()
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    my_today_logs = pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])
    if not df.empty and "Name" in df.columns:
        my_today_logs = df[(df["Name"] == st.session_state.user_name) & (df["Date"] == today_str)]
    
    status_msg = "NOT Checked In"
    status_color = "#f43f5e" # Red
    if not my_today_logs.empty:
        last_log = my_today_logs.iloc[0]
        status_msg = f"Last Action: {last_log['Type']} at {last_log['Time']}"
        status_color = "#10b981" # Green
        
    # Attendance Card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-radius: 12px; padding: 25px; border-left: 6px solid {status_color}; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="margin: 0; color: #94a3b8; font-size: 1rem;">Today's Status</p>
                <h3 style="margin: 0; color: #f8fafc;">{status_msg}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # History Table
    st.markdown("<hr><h3 style='color: #f8fafc;'>Today's Activity</h3>", unsafe_allow_html=True)
    if not my_today_logs.empty:
        disp_df = my_today_logs[["Date", "Time", "Type", "Status"]]
        st.dataframe(disp_df, use_container_width=True, hide_index=True)
    else:
        st.info("No activity today.")

# ================= ATTENDANCE HISTORY (ADMIN) =================
def attendance_history_page():
    render_header()
    st.markdown("<h2 style='color: #f8fafc;'>📅 Attendance History</h2>", unsafe_allow_html=True)
    
    df = fetch_attendance_data()
    
    # Filters Row
    f1, f2, f3 = st.columns([2, 2, 4])
    with f1:
        start_date = st.date_input("Start Date", value=None)
    with f2:
        end_date = st.date_input("End Date", value=None)
    with f3:
        search_q = st.text_input("Employee Search", placeholder="e.g., John")
        
    filtered = df.copy()
    if not filtered.empty:
        if search_q:
            filtered = filtered[filtered["Name"].str.contains(search_q, case=False, na=False)]
        if start_date:
            filtered = filtered[filtered["Date"] >= str(start_date)]
        if end_date:
            filtered = filtered[filtered["Date"] <= str(end_date)]
            
    if filtered.empty:
        st.info("No records match your filters.")
    else:
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        csv_data = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Data (CSV)", data=csv_data, file_name='attendance_history.csv', mime='text/csv')

# ================= ADMIN DASHBOARD =================
def admin_dashboard():
    render_header()
    st.markdown("<h2 style='color: #f8fafc; margin-bottom: 1.5rem;'>🛡️ System Overview</h2>", unsafe_allow_html=True)
    
    df = fetch_attendance_data()
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    total_emp = df["Name"].nunique() if not df.empty and "Name" in df.columns else 0
    today_df = df[df["Date"] == today_date] if not df.empty and "Date" in df.columns else pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])
    pres_today = today_df["Name"].nunique() if not today_df.empty and "Name" in today_df.columns else 0
    absent_today = max(0, total_emp - pres_today)
    late_today = len(today_df[today_df["Status"].str.contains("Late", na=False)]) if not today_df.empty and "Status" in today_df.columns else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", total_emp)
    c2.metric("Present Today", pres_today)
    c3.metric("Absent Today", absent_today)
    c4.metric("Late Today", late_today)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f8fafc;'>Today's Ledger</h3>", unsafe_allow_html=True)
    
    if not today_df.empty:
        st.dataframe(today_df, use_container_width=True, hide_index=True)
        colA, colB = st.columns([4, 1])
        with colB:
            csv_data = today_df.to_csv(index=False).encode('utf-8')
            st.download_button("Export Today CSV", data=csv_data, file_name=f'attendance_{today_date}.csv', mime='text/csv', use_container_width=True)
    else:
        st.info("No records today.")

# ================= ROUTING =================
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
