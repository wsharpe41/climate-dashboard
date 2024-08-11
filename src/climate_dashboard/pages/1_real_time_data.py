import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from datetime import timedelta, datetime
from dataclasses import dataclass
from typing import Literal
import leafmap.foliumap as leafmap


@dataclass
class AQMeasurement:
    id: str
    latitude: float
    longitude: float
    sensorType: Literal["low-cost sensor", "reference grade"]
    date: datetime
    value: float
    location: str


st.set_page_config(
    page_title="Real-Time OpenAq Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Real-Time OpenAq Dashboard")
st.subheader(
    """
    This is an example of a "live" dashboard, which queries OpenAq's API and updates every 30 seconds with the most recent data. 
    """
)
st.subheader("For more info on the API you can go to `https://docs.openaq.org/`")
st.divider()
# creating a single-element container
placeholder = st.empty()


# near real-time / live feed simulation
# Initialize dataframe with 100 measurements
def get_pm_measurements(time_step: timedelta) -> list[AQMeasurement]:
    url = "https://api.openaq.org/v2/measurements"
    payload = {
        "has_geo": True,
        "parameter_id": 2,
        "limit": 500,
        "unit": "µg/m³",
        "country": "US",
        "value_from": 1,
        "value_to": 1000,
    }
    end = datetime.now()
    start = end - time_step
    payload["date_from"] = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    payload["date_to"] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        results = r.json()["results"]
        new_measurements = []
        for res in results:
            if res["value"] > 1000:
                continue
            meas = AQMeasurement(
                id=res["locationId"],
                latitude=res["coordinates"]["latitude"],
                longitude=res["coordinates"]["longitude"],
                sensorType=res["sensorType"],
                date=res["date"]["utc"],
                value=res["value"],
                location=res["location"],
            )
            new_measurements.append(meas)
        return new_measurements
    else:
        print("request failed with status", r.status_code)
        return


# Initalize with the 100 most recent US PM measurements
def get_site_trends(id: float) -> list:
    url = "https://api.openaq.org/v2/measurements?date_from=2024-05-30T00%3A00%3A00Z&limit=100&page=1&offset=0&sort=desc&radius=1000&order_by=datetime"

    payload = {
        "location_id": id,
        "parameter_id": 2,
        "limit": 500,
        "unit": "µg/m³",
        "date_to": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        results = r.json()["results"]
        new_meas = [res["value"] for res in results]
        dates = [res["date"]["utc"] for res in results]
        location = results[0]["location"]
        return new_meas, dates, location
    else:
        print("request failed with status", r.status_code)
    return None, None, None


initial = get_pm_measurements(timedelta(minutes=240))
df = pd.DataFrame([meas.__dict__ for meas in initial])
while True:
    old_avg = df["value"].mean()
    old_max = df["value"].max()
    update = get_pm_measurements(timedelta(seconds=59))
    new_meas = pd.DataFrame([meas.__dict__ for meas in update])
    df = pd.concat([df, new_meas], ignore_index=True)
    df = df.sort_values(by="date", ascending=False).drop_duplicates("id", keep="first")
    df = df.head(500)
    max_id = df.loc[df["value"].idxmax()]["id"]
    new_trend, dates, location = get_site_trends(id=max_id)

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="US Average",
            value=round(df["value"].mean(), 3),
        )
        kpi2.metric(
            label="Max Value",
            value=round(df["value"].max(), 3),
        )
        m = leafmap.Map(center=[40, -100], zoom=4)
        m.add_circle_markers_from_xy(
            df,
            x="longitude",
            y="latitude",
            radius=5,
            color="red",
            fill_color="red",
            opacity=0.6,
            popup=["location", "value"],
        )
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown(f"### Moving Average of Max Value Location ({location})")
            fig = px.line(x=dates, y=new_trend)
            st.write(fig)

        with fig_col2:
            st.markdown("### 500 Most Recent PM2.5 Measurements")
            fig2 = px.histogram(data_frame=df, x="value", color="sensorType", nbins=20)
            st.write(fig2)

        m.to_streamlit(height=400)

        # st.markdown("### Detailed Data View")
        # st.dataframe(df)

        time.sleep(30)
