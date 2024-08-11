import pandas as pd
import streamlit as st
import plotly.express as px

# Adjust the width of the Streamlit page
st.set_page_config(page_title="Climate Change Indicators", layout="wide")
st.title("Country Temperature Change From Baseline")
# Import your data
df = pd.read_csv("./../../data/climate_change_indicators.csv")


def plot_temp_change(year: int):
    yr = "F" + str(year)
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=yr,
        range_color=(-3, 3),
        color_continuous_scale=px.colors.sequential.Bluered,
        title=f"Relative Temperature Change from 1960 to {year} by Country",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),  # Left, right, top, bottom
        title_font_size=20,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_trends(selected_year: int):
    # Extract columns for years from 1961 to the selected year
    year_columns = [f"F{year}" for year in range(1961, selected_year + 1)]
    trend_df = df[year_columns].copy()

    # Calculate the mean temperature change for each year
    yearly_mean = trend_df.mean().reset_index()
    yearly_mean.columns = ["Year", "Mean Temperature Change"]
    yearly_mean["Year"] = yearly_mean["Year"].str.replace("F", "").astype(int)

    # Create the line plot
    fig = px.line(
        yearly_mean,
        x="Year",
        y="Mean Temperature Change",
        title=f"Mean Temperature Change from 1960 to {selected_year}",
        labels={"Mean Temperature Change": "Mean Temp Change"},
    )

    # Update layout to reduce padding and margin
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),  # Adjust margins as needed
        title_font_size=20,
        height=200,
    )

    st.plotly_chart(fig, use_container_width=True)


# Create a layout with one column
with st.container():
    selected_year = st.slider(
        label="Selected Year", min_value=1961, max_value=2022, value=2022, step=1
    )
col1, col2 = st.columns([2, 1])

with col1:
    plot_temp_change(selected_year)
with col2:
    st.dataframe(df, column_order=["Country", "Unit", f"F{selected_year}"])

with st.container():
    # Plot the global trends for each continent
    plot_trends(selected_year)
