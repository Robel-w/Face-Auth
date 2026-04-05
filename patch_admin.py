import re
with open("app/main.py", "r") as f:
    text = f.read()

# Replace the hardcoded admin logic with something that can also read from env variables
old_logic = '''                                if name.lower() == "admin" or "yabets maregn" in name.lower() or "yabet" in name.lower():'''
new_logic = '''                                admin_users = os.getenv("ADMIN_USERS", "admin,yabets maregn,yabet").split(",")
                                is_admin = any(admin.strip().lower() in name.lower() for admin in admin_users)
                                
                                if is_admin:'''

text = text.replace(old_logic, new_logic)

with open("app/main.py", "w") as f:
    f.write(text)
