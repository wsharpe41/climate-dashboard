# climate-dashboard
Streamlit climate dashboard

## Usage/Installation
To run locally if you have hatch installed on your machine you can run `hatch shell` in the directory with the `pyproject.toml` file in it. Otherwise first run `pip install hatch` and then start the shell. Once the environment is set up you can go to the `src/climate-dashboard` directory and run `streamlit run climate_dashboard.py` which will pull up the home page of the dashboard. For the Map Server page to work you need to have the `AQ_TOKEN` environment variable set, more info is on that page.

If you are a Docker enthusiast there is an image which can be run with `docker run -p 8501:8501 -e AQ_TOKEN=XXXX wsharpe41/climate-dashboard`. 
