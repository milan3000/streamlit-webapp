import streamlit as st
from global_page_elements import insert_header, langwrite, local_css, hide_image_fullscreen

# ---- CONFIG ----
st.set_page_config(page_title="Ecowhen About Us", page_icon="favicon_nobackground.ico", layout="wide", initial_sidebar_state="collapsed")
hide_image_fullscreen()
local_css("style/style.css")

# ---- HEADER ----
insert_header()

with st.container():
    st.write("---")
    st.header("About Us", anchor=False)
    st.write(
        """
    This is where we describe ourselves!
    """
    )