import streamlit as st

def app():
    st.header("Register")
    st.write("Capture your face images and create an account.")
    name = st.text_input("Name")
    if st.button("Capture"):
        st.info("Capture flow not implemented in template.")
