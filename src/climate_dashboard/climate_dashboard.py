import streamlit as st

st.set_page_config(page_title="Climate Dash Home")
st.sidebar.success("Select a demo above.")


st.title("Example Streamlit dashboard with climate related data")

st.subheader(
    "I will be periodically updating the examples in this repo as I find new data I think will be interesting or a new visualization technique I want to try out."
)
st.divider()
st.markdown(
    "To view the dashboards click on the links in the sidebar to the left. Source code for this repo if available at `https://github.com/wsharpe41/climate-dashboard`"
)
