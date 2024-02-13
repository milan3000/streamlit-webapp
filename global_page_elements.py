import streamlit as st

# ---- Load local css file ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

# ---- Remove fullscreen buttons from images ----
def hide_image_fullscreen(): 
    hide_img_fs = ''' 
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)

# ---- LANGUAGE OPTIONS ----
languages = {"Deutsch": "de", "English": "en"}

def get_language():
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

# ---- Insert Header Row with Logo and Language Options
def insert_header():
    st.markdown(" <style> div[class^='block-container'] { padding-top: 0rem; } </style> ", unsafe_allow_html=True) #removes space at the top of the page
    get_language()
    with st.container():
        left_column, middle_column, right_column = st.columns((4,4,2))
        with left_column:
            st.markdown('''<a href="https://ecowhen.streamlit.app/" target="_self">
                        <img src="./app/static/ecowhen_logo-name.png" width="320">''', 
                        unsafe_allow_html=True)
        with middle_column:
            st.empty()
        with right_column:
            sel_lang = st.radio(
            "Sprache/ Language",
            options=languages,
            horizontal=True,
            on_change=set_language,
            key="selected_language",
            index=(0 if st.query_params.lang=='de' else 1)
    )