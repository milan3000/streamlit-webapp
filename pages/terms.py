import streamlit as st

st.set_page_config(page_title="Ecowhen Terms of Use and License", page_icon="favicon_nobackground.ico", layout="wide", initial_sidebar_state="collapsed")

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

with st.container():
    st.header("Terms of Use", anchor=False)
    st.write(
        """
    Ecowhen disclaims all responsibility for any inaccuracies in the data, 
    its availability or for any loss or damage arising from its use. 
    The accuracy and completeness of the data and their uninterrupted 
    provision are not guaranteed by Ecowhen and are provided without warranty.
    Ecowhen expressly disclaims all liability under these Terms of Use.
    """
    )
    st.write(
        """
    Our services are free for non-commercial use. If you plan to use our forecasts 
    for commercial purposes, we kindly request that you [get in touch](../#get-in-touch) with us. 
    """
    )
    left_column,middle_column, right_column = st.columns((4,1,4))
    with left_column:
        st.header("License", anchor=False)
        st.write("By using Ecowhen, you agree to the following Terms of Use:")
        st.subheader("You are free to:", anchor=False)
        st.write("**Share** — copy and redistribute the material in any medium or format.")
        st.write("**Adapt** — remix, transform, and build upon the material.")
        st.subheader("Under the following terms:", anchor=False)
        st.write("""
                **Attribution** — You must give appropriate credit , provide a link to the license, 
                and indicate if changes were made . You may do so in any reasonable manner, 
                but not in any way that suggests the licensor endorses you or your use.
                """)
#        st.write("**NonCommercial** — You may not use the material for commercial purposes .")
        st.write("""
                **No additional restrictions** — You may not apply legal terms or technological measures 
                that legally restrict others from doing anything the license permits.
                """)
        st.write("The licensor cannot revoke these freedoms as long as you follow the license terms.")
        st.write("[CC BY 4.0 DEED](https://creativecommons.org/licenses/by/4.0/)")
    with middle_column:
        st.empty()
    with right_column:
        st.header("Attribution", anchor=False)
        st.write("""
                Ecowhen uses meteorological data from [open-meteo.com](https://open-meteo.com/).
                This data is licensed under the 
                [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://open-meteo.com/en/license).
                No direct modifications are made; the data is used for machine learning and modeling purposes.
                """)
        st.write("""
                Ecowhen uses data on electricity generation and consumption from [Bundesnetzagentur | SMARD.de](https://www.smard.de/home).
                This data is licensed under the
                [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://www.smard.de/en/datennutzung).
                No direct modifications are made; the data is used for machine learning and modeling purposes.
                """)