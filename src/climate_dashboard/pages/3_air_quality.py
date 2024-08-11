import streamlit as st
import leafmap.foliumap as leafmap
import os

st.set_page_config(page_title="Global Air Quality", layout="wide")
st.title("Global Air Quality Web Map Server")
st.subheader(
    "This page requires an API Token for the AQICN API in the AQ_TOKEN environment variable"
)
st.subheader("To get an api token you can visit `https://aqicn.org/api/`")
st.divider()

m = leafmap.Map(center=(36.3, 0), zoom=2, google_map="SATELLITE")
aqis = st.multiselect(
    "Which Air Quality Indices Would You Like To View?",
    ["usepa-aqi", "usepa-pm25", "usepa-pm10"],
)

aq_token = os.environ["AQ_TOKEN"]

for aqi in aqis:
    url = f"https://tiles.aqicn.org/tiles/{aqi}/{{z}}/{{x}}/{{y}}.png?token={aq_token}"

    m.add_tile_layer(url, name=aqi, attribution="EPA")

m.to_streamlit(height=600)
