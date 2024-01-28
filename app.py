import pandas as pd
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from datetime import datetime
import pytz
from traffic_light import generate_traffic_light_html
from plots import plot_prediction, plot_renewable_share

# ---- Config ----
traffic_light_states = {
    80 : ('Green', 2),
    33 : ('Yellow', 1),
    0  : ('Red', 0)}

st.set_page_config(page_title="Ecowhen", page_icon="favicon_nobackground.ico", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


def get_traffic_light_state(forecast_df):
    share_df = forecast_df.loc[:,['time','re_share']].set_index('time')['re_share']
    share_df.index = pd.DatetimeIndex(share_df.index)
    berlin_now = pd.Timestamp.now().floor('h')
    re_share_now = share_df.loc[share_df.index == berlin_now].item()
    
    for level, (traffic_light_color, traffic_light_state) in traffic_light_states.items():
        if re_share_now > level:
            break # return fitting level
            
    # compute period until traffic light switches
    future_shares = share_df.loc[share_df.index > berlin_now]
    switch_times = future_shares.index[(future_shares>level).diff().fillna(False)]
    
    period = int((switch_times[0]- pd.Timestamp(berlin_now)) / pd.Timedelta('1h'))
    return re_share_now, traffic_light_state, traffic_light_color, period
    
# ---- LOAD ASSETS ----
local_css("style/style.css")
lottie_coding = load_lottieurl("https://lottie.host/5aee9f59-db21-45f4-8520-7f90f0698b12/Z6EW1TwZI7.json")

# ---- READ DATA ----
forecast_df = pd.read_json("https://reforecast.pythonanywhere.com/api/data")
forecast_df['re_share'] = 100*(forecast_df['wind'] + forecast_df['solar'] + forecast_df['hydropower'] + forecast_df['biomass']) / forecast_df['demand']

# ---- GLOBAL SETTINGS ----
hide_img_fs = ''' 
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True) #Remove fullscreen buttons from images

# ---- HEADER ----
with st.container():
    left_column, middle_column, right_column = st.columns((3,1,3))
    with left_column:
        st.subheader("Hello, welcome to the beta version", anchor=False)
        left_mini_column, right_mini_column = st.columns([1.5,8.5])
        with left_mini_column:
            st.image("favicon.svg", width=70)
        with right_mini_column:
            st.title("Ecowhen", anchor=False)
        st.write("We want to help you consume electricity in a more eco-friendly manner!")
        st.write("Consuming electricity during high renewable energy periods reduces your **carbon footprint**.")
        st.write("Check our forecast for the German electricity mix to make informed usage decisions.")
        st.write("[Learn More >](#what-we-do)")
    with middle_column:
        berlin_now = pd.Timestamp.now().floor('h')
        re_share_now, traffic_light_state, traffic_light_color, period = get_traffic_light_state(forecast_df)
        st.markdown(generate_traffic_light_html(traffic_light_state, period), unsafe_allow_html=True)
    with right_column:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.subheader("Electricity Traffic Light", anchor=False)
        st.write(f"""The traffic light shows, how eco-friendly the electricity mix is right now. 
                 With a renewable energy share of **{round(re_share_now)}%** the traffic light shows **{traffic_light_color}**.""")
        if(traffic_light_state==2):
            st.write("""Now is a good time to consume electricity, use the dishwasher and washing machine or charge
                     your electric vehicle. 
                     """)
        elif(traffic_light_state==1):
            st.write("""Now is an OK time to consume electricity. 
                     If you have planned to run big devices, maybe hold off on it, if you can!
                     """)
        else:
            st.write("""Now is not the best time to consume elctricity. Most of it comes from non-renewable sources like coal and gas 
                     that pollute the atmosphere.
                     """)
        st.write("""To find out, how this might change in the upcoming days,
                     check our [Forecasts](#forecasts) below!
                     """)
        
# ---- PLOTS ----
with st.container():
    st.write("---")
    st.subheader("Forecasts", anchor=False)
    tab1, tab2 = st.tabs(["Electricity Mix", "Electricity Traffic Light"])

    with tab1:
        left_column, right_column = st.columns((7,3))
        with left_column:
            forecast_fig = plot_prediction(forecast_df, berlin_now)
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
            st.write(
                """
                This graph shows the generation from each source of renewable energy 
                in the German electricity mix for each hour of the upcoming week. The power 
                from biomass, hydropower, wind, and solar is shown stacked on top of one 
                another, while the red line represents the overall demand. Any difference 
                between the renewable energy and demand (called residual load) needs to 
                be compensated for by fossil fuels or electricity imports.
                """)
    with tab2:
        left_column, right_column = st.columns((7,3))
        with left_column:
            traffic_light_fig = plot_renewable_share(forecast_df, berlin_now)
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
            st.write(
                """
                The electricity traffic light shows the share of renewable energy in the electricity mix in an intuitive format. 
                Every hour of the upcoming week gets assigned a color ranging from green to red depending on the share of renewable energy to overall demand.
                This makes determining times of optimal electricity usage super easy.
                """)
            
# ---- INFO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        with left_column:
            st.header("What we do", anchor=False)
            st.write(
                """
                We at Ecowhen provide a free and publicly available forecast 
                of the German electricity mix to determine optimal times of usage.
                Our infographics and API are free for non-commercial purposes. 
                Soon, we will also offer the [Ecowhen Home Assistant](https://www.smard.de/home), 
                a simple and easy-to-install system that makes eco-friendly energy usage 
                even more convenient. So stay tuned for future updates!
                If you have any questions, please contact us through the [Contact Form](#get-in-touch) below.
                If you like our work, consider [buying us a coffee](https://www.buymeacoffee.com/milan_wanek) :coffee:,
                we would really appreciate it! 
                """
            )
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
        

# ---- CONTACT ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Get In Touch!", anchor=False)
        # Docs on https://formsubmit.co
        contact_form = """
            <form action="https://formsubmit.co/milanw12@gmail.com" method="POST">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here..." required ></textarea>
                <button type="submit">Send</button>
            </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()