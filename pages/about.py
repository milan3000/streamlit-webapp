import streamlit as st
from global_page_elements import insert_header, langwrite

st.set_page_config(page_title="Ecowhen About Us", page_icon="favicon_nobackground.ico", layout="wide", initial_sidebar_state="collapsed")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- HEADER ----
insert_header()

with st.container():
    st.header("About Us", anchor=False)
    st.write(
        """
    This is where we describe ourselves!
    """
    )