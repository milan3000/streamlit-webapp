import pandas as pd
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from datetime import datetime
import pytz
from traffic_light import generate_traffic_light_html
from plots import plot_prediction, plot_renewable_share
from global_page_elements import hide_image_fullscreen, insert_header, langwrite, local_css
#%%

# ---- CONFIG ----
traffic_light_states = {
    0  : (['Red','Rot'], 0),
    1 : (['Yellow','Gelb'], 33),
    2 : (['Green','Grün'], 80),
    }
n_days_ahead=3

st.set_page_config(page_title="Ecowhen", page_icon="static/favicon.ico", layout="wide", initial_sidebar_state="collapsed")
hide_image_fullscreen()
local_css("style/style.css")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_traffic_light_state(forecast_df):
    share_df = forecast_df.loc[:,['time','re_share']].set_index('time')['re_share']
    share_df.index = pd.DatetimeIndex(share_df.index)
    berlin_now = pd.Timestamp.now().floor('h')
    re_share_now = share_df.loc[share_df.index == berlin_now].item()
    
    traffic_state_df = share_df * 0
    for traffic_light_state, (traffic_light_color, level) in traffic_light_states.items():
        traffic_state_df[share_df>level] = traffic_light_state
            
    traffic_light_state = int(traffic_state_df.loc[berlin_now])
    traffic_light_color = traffic_light_states[traffic_light_state][0]
    # compute period until traffic light switches
    future_states = traffic_state_df.loc[traffic_state_df.index >= berlin_now]
    switch_times = future_states[(future_states).diff().fillna(0)!=0]
    
    #compute how low the current state will last and what would be the next state.
    if len(switch_times.index)>0:
        period = int((switch_times.index[0]- pd.Timestamp(berlin_now)) / pd.Timedelta('1h'))
        next_state = switch_times[0]
    else:
        next_state= None
        period = None
    
    return re_share_now, traffic_light_state, traffic_light_color, period, next_state
    
# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://lottie.host/5aee9f59-db21-45f4-8520-7f90f0698b12/Z6EW1TwZI7.json")

# ---- READ DATA ----
forecast_df = pd.read_json("https://reforecast.pythonanywhere.com/api/data")
forecast_df['re_share'] = 100*(forecast_df['wind'] + forecast_df['solar'] + forecast_df['hydropower'] + forecast_df['biomass']) / forecast_df['demand']
forecast_df = forecast_df.iloc[:24*n_days_ahead]
# ---- HEADER ----
insert_header()

# ---- TRAFFIC LIGHT ----
with st.container():
    st.write("---")
    left_column, middle_column, right_column = st.columns((3,1,3))
    with left_column:
        st.subheader(langwrite("Hello, welcome to Ecowhen (beta)", 
                               "Hallo, willkommen bei Ecowhen (beta)"), anchor=False)
        st.write(langwrite("We want to help you consume electricity in a more eco-friendly manner!",
            "Wir wollen dir helfen, deinen Stromverbrauch umweltfreundlicher zu gestalten!"))
        st.write(langwrite("Consuming electricity during high renewable energy periods reduces your **carbon footprint**.",
            "Eine Anpassung des eigenen Verbrauchs an Zeiten mit hohem Anteil an Erneuerbarer Energie reduziert deinen **CO2-Fußabdruck**."))
        st.write(langwrite("Check our forecast of the German electricity mix to make informed usage decisions.",
                "Schau in unsere Vorhersagen für den deutschen Strommix, um die besten Zeiten zu finden."))
        st.write(langwrite("[Learn More >](#what-we-do)", "[Erfahre Mehr >](#was-wir-machen)"))
    with middle_column:
        berlin_now = pd.Timestamp.now().floor('h')
        re_share_now, traffic_light_state, traffic_light_color, period, next_state = get_traffic_light_state(forecast_df)
        st.markdown(generate_traffic_light_html(traffic_light_state, period, next_state), unsafe_allow_html=True)
    with right_column:
        st.subheader(langwrite("Electricity Traffic Light", "Stromampel"), anchor=False)
        st.write(langwrite(f"""The traffic light shows, how eco-friendly the electricity mix is right now. 
                 With a renewable energy share of **{round(re_share_now)}%** the traffic light shows **{traffic_light_color[0]}**.""",
                 f"""Die Stromampel zeigt an, wie umweltfreundlich der aktuelle Strommix ist. 
                 Mit einem Anteil von **{round(re_share_now)}%** Erneuerbarer Energie zeigt die Stromampel **{traffic_light_color[1]}**."""))
        if(traffic_light_state==2):

            st.write(langwrite("""Now is a **good** time to consume electricity, use the dishwasher and washing machine or charge
                     your electric vehicle.""",
                     """Jetzt ist eine **gute** Zeit, um Strom zu verbrauchen, den Geschirrspüler und die Waschmaschine zu benutzen oder
                     Ihr Elektrofahrzeug aufzuladen."""))
                     
        elif(traffic_light_state==1) and (next_state == 2):
            st.write(langwrite("""Now is an **OK** time to consume electricity. 
                     If you have planned to run big devices, maybe hold off on it until more renewable energy is available, if you can!""",
                     """Jetzt ist eine **mittelgute** Zeit, um Strom zu verbrauchen. 
                     Falls du geplant hast, große Geräte zu betreiben, überleg dir, ob du warten kannst, bis mehr erneuerbare Energie zur Verfügung steht."""))
        elif(traffic_light_state==1) and (next_state == 0):
            st.write(langwrite("""Now is an **OK** time to consume electricity. 
                     If you have planned to run big devices, maybe do it now before the traffic light swiches to red!""",
                     """Jetzt ist eine **mittelgute** Zeit, um Strom zu verbrauchen.
                     Falls du geplant hast, große Geräte zu betreiben, mach es am besten jetzt, bevor die Stromampel auf ROT schaltet"""))
        elif(traffic_light_state==1) and (next_state is None):
            st.write(langwrite("""Now is an **OK** time to consume electricity. 
                     If you have planned to run big devices, maybe do it now before the traffic light swiches to red!""",
                     """Jetzt ist eine **mittelgute** Zeit, um Strom zu verbrauchen."""))
        
        else:

            st.write(langwrite("""Now is **not the best time** to consume elctricity. Most of it comes from non-renewable sources like coal and gas 
                     that pollute the atmosphere. The traffic light will approximately switch in {period} hours when more renewables will be available.""",
                     f"""Jetzt ist **nicht der beste Zeitpunkt**, um Strom zu verbrauchen. Der meiste Strom stammt aus nicht erneuerbaren Quellen wie Kohle und Gas, 
                     welche die Atmosphäre verschmutzen. Die Ampel wird ungefähr in {period} Stunde(n) umschalten, wenn mehr erneuerbare Energie verfügbar sein wird."""))
        st.write(langwrite("""To find out, how the next hours and days will look like,
                     check our [Forecasts](#forecasts) below!""",
                     """Um herauszufinden, wie die nächsten Stunden und Tage aussehen werden,
                     wirf einen Blick auf unsere [Vorhersagen](#vorhersagen) weiter unten!"""))

        
# ---- PLOTS ----
with st.container():
    st.write("---")
    st.header(langwrite("Forecasts", "Vorhersagen"), anchor=False)
    tab1, tab2 = st.tabs([langwrite("Electricity Traffic Light", "Stromampel"), langwrite("Electricity Mix", "Strommix")])

    with tab1:
        left_column, right_column = st.columns((7,3))
        with left_column:
            traffic_light_fig = plot_renewable_share(forecast_df, berlin_now, st.query_params.lang)
            st.plotly_chart(traffic_light_fig, use_container_width=True, config = {'displayModeBar': False})
        with right_column:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(langwrite(
                """
                The electricity traffic light shows the share of renewable energy in the electricity mix in an intuitive format. 
                Every hour of the upcoming three days gets assigned a color ranging from green to red depending on the share of renewable energy to overall demand.
                This makes determining times of optimal electricity usage super easy.
                """,
                """
                Die Stromampel zeigt den Anteil der erneuerbaren Energien am Strommix in einem intuitiven Format an. 
                Jeder Stunde der kommendenden drei Tage wird eine Farbe zugewiesen, die von grün bis rot reicht, 
                je nach dem Anteil der erneuerbaren Energien am gesamtdeutschen Stromverbrauch. So lassen sich kinderleicht die besten Zeiten
                zum optimalen Stormverbrauch herausfinden.
                """))
    with tab2:
        left_column, right_column = st.columns((7,3))
        with left_column:
            
            forecast_fig = plot_prediction(forecast_df, berlin_now, st.query_params.lang)
            st.plotly_chart(forecast_fig, use_container_width=True, config = {'displayModeBar': False})
        with right_column:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(langwrite(
                """
                This graph shows the generation from each source of renewable energy 
                in the German electricity mix for each hour of the upcoming week. The power 
                from biomass, hydropower, wind, and solar is shown stacked on top of one 
                another, while the red line represents the overall demand. Any difference 
                between the renewable energy and demand (called residual load) needs to 
                be compensated for by fossil fuels or electricity imports.
                """,
                """
                Diese Grafik zeigt die Erzeugung aus jeder erneuerbaren Energiequelle 
                im deutschen Strommix für jede Stunde der kommenden Woche. Der Strom 
                aus Biomasse, Wasserkraft, Wind- und Sonnenenergie ist übereinander gestapelt 
                während die rote Linie den Stromverbrauch darstellt. Jede Differenz 
                zwischen der erneuerbaren Energie und dem Verbrauch (als Residuallast bezeichnet) muss 
                durch fossile Brennstoffe oder Stromimporte ausgeglichen werden.
                """))
            
# ---- INFO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        with left_column:
            st.header(langwrite("What we do", "Was wir machen"), anchor=False)
            st.markdown(langwrite(
                """
                We at Ecowhen provide a free and publicly available forecast 
                of the German electricity mix to determine optimal times of usage.
                Our infographics and API are free for private purposes.
                Find out more <a href="about?lang=en" target="_self">About Us</a> and our <a href="terms?lang=en" target="_self">Terms of Use and License</a>.
                Soon, we will also offer the <a href="about?lang=en" target="_self">About Us</a>, 
                a simple and easy-to-install system that makes eco-friendly energy usage 
                even more convenient. So stay tuned for future updates!
                If you have any questions, please contact us through the [Contact Form](#get-in-touch) below.
                If you like our work, consider <a href="https://www.buymeacoffee.com/milan_wanek" target="_blank">buying us a coffee</a> :coffee:,
                we would really appreciate it! 
                """,
                """
                Wir von Ecowhen bieten eine kostenlose und öffentlich zugängliche Vorhersage 
                des deutschen Strommixes, um die optimalen Nutzungszeiten zu ermitteln.
                Unsere Infografik und API sind für private Zwecke kostenlos.
                Erfahren Sie mehr <a href="about?lang=de" target="_self">Über Uns</a> und unsere <a href="terms?lang=de" target="_self">Nutzungs- und Lizenzbedinungen</a>.
                Bald werden wir auch den <a href="about?lang=de" target="_self" >Ecowhen Home Assistant</a> anbieten, 
                ein einfaches und leicht zu installierendes System, das die umweltfreundliche Energienutzung 
                noch bequemer macht. Bleiben Sie also auf dem Laufenden für zukünftige Updates!
                Wenn Sie Fragen haben, kontaktieren Sie uns bitte über das [Kontaktformular](#kontaktieren-sie-uns) unten.
                Wenn Ihnen unsere Arbeit gefällt, können Sie uns gerne einen <a href="https://www.buymeacoffee.com/milan_wanek" target="_blank">Kaffee</a> :coffee: spendieren,
                wir würden uns sehr darüber freuen!
                """
            ), unsafe_allow_html=True)
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
        
# ---- CONTACT ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header(langwrite("Get In Touch!", "Kontaktieren Sie uns!"), anchor=False)
        # Docs on https://formsubmit.co
        contact_form = langwrite("""
            <form action="https://formsubmit.co/milanw12@gmail.com" method="POST">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here..." required ></textarea>
                <button type="submit">Send</button>
            </form>
        """,
        """
            <form action="https://formsubmit.co/milanw12@gmail.com" method="POST">
                <input type="text" name="name" placeholder="Dein Name" required>
                <input type="email" name="email" placeholder="Deine Email" required>
                <textarea name="message" placeholder="Deine Nachricht hier..." required ></textarea>
                <button type="submit">Senden</button>
            </form>
        """)
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()
        
# ---- Footer ----
with st.container():

    st.write("---")  
    st.markdown(langwrite("""<a href="about?lang=en" target="_self">About Us</a> - <a href="terms?lang=en" target="_self">Terms of Use and License</a>""",
                       """<a href="about?lang=de" target="_self">Über Uns</a> - <a href="terms?lang=de" target="_self">Nutzungs- und Lizenzbedinungen</a>"""
                       ), unsafe_allow_html=True)