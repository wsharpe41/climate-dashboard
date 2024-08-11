FROM python:3.11-slim
RUN python -m pip install hatch
WORKDIR /app
COPY pyproject.toml /app
RUN hatch dep show requirements > /app/requirements.txt && \
    python -m pip install -r /app/requirements.txt
COPY . /app
EXPOSE 8051
WORKDIR /app/src/climate_dashboard
CMD ["streamlit","run","climate_dashboard.py"]

