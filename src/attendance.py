import os
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ATTENDANCE_FILE = os.path.join(BASE_DIR, "data", "attendance.csv")

def log_attendance(name):
    """Records the user's check-in/out timestamp to a CSV with Check-In/Out logic."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Initialize the CSV with headers if it doesn't exist
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])
        df.to_csv(ATTENDANCE_FILE, index=False)
    else:
        df = pd.read_csv(ATTENDANCE_FILE)
        
    # Check if user already has a Check-In for today
    today_logs = df[(df["Name"] == name) & (df["Date"] == date_str)]
    if len(today_logs) == 0:
        action_type = "Check-In"
        # Dummy late logic (assuming after 09:00:00 is late)
        status = "Late 🔴" if time_str > "09:00:00" else "On Time ✅"
    else:
        # If they already checked in, it's a check-out (or just subsequent log)
        action_type = "Check-Out"
        status = "Completed ✅"
    
    # Append the new record
    record = pd.DataFrame([{"Name": name, "Date": date_str, "Time": time_str, "Type": action_type, "Status": status}])
    record.to_csv(ATTENDANCE_FILE, mode='a', header=False, index=False)
    
    return f"{date_str} {time_str}"

def get_attendance():
    """Fetches the attendance log."""
    if not os.path.exists(ATTENDANCE_FILE):
        return pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])
    return pd.read_csv(ATTENDANCE_FILE)

def force_check_out(name):
    """Force a Check-Out action for a user when they log out."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Type", "Status"])
        df.to_csv(ATTENDANCE_FILE, index=False)
        
    action_type = "Check-Out"
    status = "Completed ✅"
    record = pd.DataFrame([{"Name": name, "Date": date_str, "Time": time_str, "Type": action_type, "Status": status}])
    record.to_csv(ATTENDANCE_FILE, mode='a', header=False, index=False)
    return f"{date_str} {time_str}"
