import streamlit as st
from global_page_elements import insert_header, langwrite, local_css, hide_image_fullscreen

# ---- CONFIG ----
st.set_page_config(page_title=langwrite("Ecowhen - About Us", "Ecowhen - Über Uns"), page_icon="static/favicon.ico", layout="wide", initial_sidebar_state="collapsed")
hide_image_fullscreen()
local_css("style/style.css")

# ---- HEADER ----
insert_header()

# ---- ABOUT US ----
with st.container():
    st.write("---")
    st.header(langwrite("About Us", "Über Uns"), anchor=False)
    st.write(langwrite(
            """
            This is a project that is passionately maintained and further developed by:""",
            """ 
            Dieses Projekt wird leidenschaftlicht weiter entwickelt von:"""
            ))
st.write("""Andreas Geiges - Frauenstätt 8a - 83313 Siegsdorf""")
st.write("""Milan Wanek - Weisestrasse 50 - 12049 Berlin""")
        
st.write('---')
st.write(langwrite(
        """Contact:""", 
        """Kontakt:"""
        ))
st.write("""info@ecowhen.de""")
