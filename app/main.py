import importlib
import streamlit as st

st.set_page_config(page_title="Face Auth", layout="centered")
st.title("Face Auth")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Login", "Register"])

if page == "Login":
    mod = importlib.import_module("app.pages.login")
    mod.app()
else:
    mod = importlib.import_module("app.pages.register")
    mod.app()
