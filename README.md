# Malaysia Air Quality & Weather Dashboard (2014–2024)

An interactive dashboard for visualizing and forecasting air quality and weather trends across Malaysia’s states from 2014 to 2024.

## 🌏 Project Links

- **Live Dashboard:** [View on Streamlit Cloud](https://malaysiaairqualitydashboard-fnrcnbgz6icnpgbyopzuub.streamlit.app/)
- **Source Code:** [View on GitHub](https://github.com/Mahmoudmu1/malaysia_airquality_dashboard)
- **Dataset:** [Kaggle - Malaysia Weather Data](https://www.kaggle.com/datasets/shahmirvarqha/weather-data-malaysia/data)
- **GeoJSON Map:** [Malaysia State Boundaries GeoJSON](https://github.com/salistg/administrative_malaysia_state_province_boundary)

---

## 📊 Overview

This dashboard helps users explore air quality and weather patterns in Malaysia using interactive charts, maps, and simple forecasting. Features include:

- **Filtering** by state, year, month, and variable (AQI, temperature, humidity, wind speed, precipitation)
- **Dynamic charts** for trends, distributions, and comparisons
- **Geographic maps** showing spatial patterns across Malaysian states
- **Forecasting** future trends using linear regression
- **Data export** for custom analysis

---

## 🗂️ Dataset

- **Source:** [Kaggle: Malaysia Weather Data (1996–Present)](https://www.kaggle.com/datasets/shahmirvarqha/weather-data-malaysia/data)
- **Variables Used:** 
    - Air Quality Index (AQI)
    - Temperature (°C)
    - Humidity (%)
    - Wind Speed (km/h)
    - Precipitation (mm)
    - State, Year, Month

---

## 🚀 How to Run Locally

1. Clone this repo and install requirements:
    ```bash
    git clone https://github.com/Mahmoudmu1/malaysia_airquality_dashboard.git
    cd malaysia_airquality_dashboard
    pip install -r requirements.txt
    ```
2. Download dataset and geojson (if not included).
3. Run:
    ```bash
    streamlit run app.py
    ```

---

## 📚 Dashboard Tabs

- **Overview:** Key metrics and quick insights
- **Trends:** Yearly/monthly trends, moving average, dual-axis charts
- **Distribution:** Bar/pie charts, progress bars for state comparison
- **Geographic:** Choropleth maps by state
- **Forecast:** Predict future trends (up to 24 months ahead)
- **Raw Data:** View and export filtered dataset

---

## 📝 Methodology

- Data cleaning, aggregation, and feature engineering using Python pandas
- Interactive web app built with Streamlit and Plotly
- Forecasting with linear regression (scikit-learn)
- Map visualization using Plotly and custom GeoJSON boundaries

---

## 📈 Sample Visuals

_Include screenshots or GIFs of your dashboard here!_

---

## 🔗 References

- [Kaggle: Malaysia Weather Data](https://www.kaggle.com/datasets/shahmirvarqha/weather-data-malaysia/data)
- [Malaysia States GeoJSON](https://github.com/salistg/administrative_malaysia_state_province_boundary)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)

---

## 👨‍💻 Author

**Mahmoud Musa**  


---

