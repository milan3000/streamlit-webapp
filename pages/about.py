import streamlit as st

st.set_page_config(page_title="Ecowhen About Us", page_icon="favicon_nobackground.ico", layout="wide", initial_sidebar_state="collapsed")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- LANGUAGE OPTIONS ----
languages = {"Deutsch": "de", "English": "en"}

query_parameters = st.query_params.to_dict()
if "lang" not in query_parameters:
    st.query_params.lang="de"
    st.experimental_rerun()


def set_language() -> None:
    if "selected_language" in st.session_state:
        st.query_params.lang=languages.get(st.session_state["selected_language"]
        )

def langwrite(english_text, german_text):
    if st.query_params.lang == 'en':
        return english_text
    elif st.query_params.lang == 'de':
        return german_text
    return None

# ---- HEADER ----
st.markdown(" <style> div[class^='block-container'] { padding-top: 0rem; } </style> ", unsafe_allow_html=True) #removes space at the top of the page
with st.container():
    left_column, middle_column, right_column = st.columns((4,4,2))
    with left_column:
        st.image("ecowhen_logo-name.svg", width=320)
    with middle_column:
        st.empty()
    with right_column:
        sel_lang = st.radio(
        "Sprache/ Language",
        options=languages,
        horizontal=True,
        on_change=set_language,
        key="selected_language",
)

# ---- HEADER ----
with st.container():
    st.header("About Us", anchor=False)
    st.write(
        """
    This is where we describe ourselves!
    """
    )