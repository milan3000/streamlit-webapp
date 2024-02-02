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
