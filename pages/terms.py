import streamlit as st
from global_page_elements import insert_header, langwrite, local_css, hide_image_fullscreen

# ---- CONFIG ----
st.set_page_config(page_title="Ecowhen Terms of Use and License", page_icon="favicon_nobackground.ico", layout="wide", initial_sidebar_state="collapsed")
hide_image_fullscreen()
local_css("style/style.css")

# ---- HEADER ----
insert_header()

# ---- TERMS ----
with st.container():
    st.write("---")
    st.header(langwrite("Terms of Use", "Nutzungsbedingungen"), anchor=False)
    st.write(langwrite(
        """
    Ecowhen disclaims all responsibility for any inaccuracies in the data, 
    its availability or for any loss or damage arising from its use. 
    The accuracy and completeness of the data and their uninterrupted 
    provision are not guaranteed by Ecowhen and are provided without warranty.
    Ecowhen expressly disclaims all liability under these Terms of Use.
    """,
    """
    Ecowhen lehnt jede Verantwortung für eventuelle Ungenauigkeiten in den Daten ab, 
    ihre Verfügbarkeit oder für Verluste oder Schäden, die durch ihre Nutzung entstehen. 
    Die Richtigkeit und Vollständigkeit der Daten und ihre ununterbrochene Bereitstellung 
    werden von Ecowhen nicht garantiert; die Daten werden ohne Gewähr bereitgestellt.
    Ecowhen lehnt ausdrücklich jede Haftung im Rahmen dieser Nutzungsbedingungen ab.
    """
    ))
    st.write(langwrite(
        """
    Our services are free for non-commercial use. If you plan to use our forecasts 
    for commercial purposes, we kindly request that you [get in touch](../?lang=en#get-in-touch) with us. 
    """,
    """
    Unsere Dienste sind für die nicht-kommerzielle Nutzung kostenlos. Wenn Sie planen, unsere Prognosen 
    für kommerzielle Zwecke zu nutzen, bitten wir Sie, sich mit uns [in Verbindung zu setzen](../?lang=de#kontaktieren-sie-uns).
    """
    ))
    left_column,middle_column, right_column = st.columns((4,1,4))
    with left_column:
        st.header(langwrite("License", "Lizenz"), anchor=False)
        st.write(langwrite("By using Ecowhen, you agree to the following Terms of Use:",
                           "Durch die Nutzung von Ecowhen erklären Sie sich mit den folgenden Nutzungsbedingungen einverstanden:"))
        st.subheader(langwrite("You are free to:", "Sie dürfen:"), anchor=False)
        st.write(langwrite("**Share** — copy and redistribute the material in any medium or format.",
                           """**Teilen** — das Material in jedwedem Format oder Medium vervielfältigen 
                           und weiterverbreiten und zwar für beliebige Zwecke, sogar kommerziell."""))
        st.write(langwrite("**Adapt** — remix, transform, and build upon the material.",
                           """**Bearbeiten** — das Material remixen, verändern und darauf aufbauen 
                           und zwar für beliebige Zwecke, sogar kommerziell."""))
        st.subheader(langwrite("Under the following terms:", "Unter folgenden Bedingungen:"), anchor=False)
        st.write(langwrite("""
                **Attribution** — You must give appropriate credit , provide a link to the license, 
                and indicate if changes were made . You may do so in any reasonable manner, 
                but not in any way that suggests the licensor endorses you or your use.
                """,
                """
                **Namensnennung** — Sie müssen angemessene Urheber- und Rechteangaben machen , 
                einen Link zur Lizenz beifügen und angeben, ob Änderungen vorgenommen wurden. 
                Diese Angaben dürfen in jeder angemessenen Art und Weise gemacht werden, 
                allerdings nicht so, dass der Eindruck entsteht, der Lizenzgeber unterstütze 
                gerade Sie oder Ihre Nutzung besonders.
                """))
#        st.write("**NonCommercial** — You may not use the material for commercial purposes .")
        st.write(langwrite("""
                **No additional restrictions** — You may not apply legal terms or technological measures 
                that legally restrict others from doing anything the license permits.
                """,
                """
                **Keine weiteren Einschränkungen** — Sie dürfen keine zusätzlichen Klauseln oder technische 
                Verfahren einsetzen, die anderen rechtlich irgendetwas untersagen, was die Lizenz erlaubt.
                """
                ))
        st.write(langwrite("The licensor cannot revoke these freedoms as long as you follow the license terms.",
                 "Der Lizenzgeber kann diese Freiheiten nicht widerrufen solange Sie sich an die Lizenzbedingungen halten."))
        st.write(langwrite("[CC BY 4.0 DEED Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)",
                 "[CC BY 4.0 DEED Namensnennung 4.0 International](https://creativecommons.org/licenses/by/4.0/deed.de)"))
    with middle_column:
        st.empty()
    with right_column:
        st.header(langwrite("Attribution", "Datenquellen"), anchor=False)
        st.write(langwrite("""
                Ecowhen uses meteorological data from [open-meteo.com](https://open-meteo.com/).
                This data is licensed under the 
                [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://open-meteo.com/en/license).
                No direct modifications are made; the data is used for machine learning and modeling purposes.
                """,
                """
                Ecowhen verwendet meteorologische Daten von [open-meteo.com](https://open-meteo.com/).
                Diese Daten sind lizenziert unter der 
                [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://open-meteo.com/en/license).
                Es werden keine direkten Änderungen vorgenommen; die Daten werden für maschinelles Lernen und Modellierungszwecke verwendet.
                """
                ))
        st.write(langwrite("""
                Ecowhen uses data on electricity generation and consumption from [Bundesnetzagentur | SMARD.de](https://www.smard.de/home).
                This data is licensed under the
                [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://www.smard.de/en/datennutzung).
                No direct modifications are made; the data is used for machine learning and modeling purposes.
                """,
                """
                Ecowhen verwendet Daten über Stromerzeugung und -verbrauch von [Bundesnetzagentur | SMARD.de](https://www.smard.de/home).
                Diese Daten sind lizenziert unter der
                [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://www.smard.de/en/datennutzung).
                Es werden keine direkten Änderungen vorgenommen; die Daten werden für maschinelles Lernen und Modellierungszwecke verwendet.
                """
                ))