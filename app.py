import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import json

st.set_page_config(page_title="Malaysia Air Quality & Weather Dashboard", layout="wide")

# ---- Load Data ----
df = pd.read_csv("malaysia_airquality_weather_state_year_monthname.csv")
aqi_warning = pd.read_csv("air_quality_warning.csv")
indicators = pd.read_csv("air_quality_indicators.csv")

# ---- Prepare Lists for Sidebar Filters ----
states = sorted(df['state'].unique())
years = sorted(df['year'].unique())
months = sorted(df['month_name'].unique(), key=lambda m: pd.to_datetime(m, format='%B').month)

var_options = {
    'Air Quality Index (AQI)': 'pollutant_value',
    'Temperature (°C)': 'temperature',
    'Humidity (%)': 'humidity',
    'Wind Speed': 'wind_speed',
    'Precipitation': 'precipitation_total'
}

# ---- Session State for Filters ----
if 'selected_states' not in st.session_state:
    st.session_state.selected_states = states
if 'selected_years' not in st.session_state:
    st.session_state.selected_years = years
if 'selected_months' not in st.session_state:
    st.session_state.selected_months = months
if 'selected_var' not in st.session_state:
    st.session_state.selected_var = 'Air Quality Index (AQI)'
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "🏠 Overview"

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### Show Variable")
    selected_var = st.selectbox("Select Variable", list(var_options.keys()), key="selected_var")
    st.markdown("### Data Filters")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Select All States"):
            st.session_state.selected_states = states
        if st.button("Select All Years"):
            st.session_state.selected_years = years
        if st.button("Select All Months"):
            st.session_state.selected_months = months
    with col_b:
        if st.button("Clear All States"):
            st.session_state.selected_states = []
        if st.button("Clear All Years"):
            st.session_state.selected_years = []
        if st.button("Clear All Months"):
            st.session_state.selected_months = []
    selected_states = st.multiselect("Select State(s)", states, key="selected_states")
    selected_years = st.multiselect("Select Year(s)", years, key="selected_years")
    selected_months = st.multiselect("Select Month(s)", months, key="selected_months")

# ---- RADIO BUTTON TOP NAV ----
tab_options = [
    "🏠 Overview", "📈 Trends", "📊 Distribution", "🗺️ Geographic", "🔮 Forecast", "🗃️ Raw Data"
]

tab_selected = st.radio(
    "", tab_options, horizontal=True, label_visibility="collapsed",
    index=tab_options.index(st.session_state.active_tab)
)
st.session_state.active_tab = tab_selected

# ---- Filter Data ----
filtered = df[
    df['state'].isin(st.session_state.selected_states) &
    df['year'].isin(st.session_state.selected_years) &
    df['month_name'].isin(st.session_state.selected_months)
]
state_avg = pd.DataFrame()
if not filtered.empty:
    state_avg = filtered.groupby("state")[var_options[st.session_state.selected_var]].mean().reset_index()

#### ---- VARIABLE EXPLANATION & RANGES ---- ####
def show_variable_explanation(var):
    if var == 'Air Quality Index (AQI)':
        st.markdown("### 🟦 AQI Levels Explained")
        st.write("""
**Air Quality Index (AQI)** is a scale from 0 to 500 that shows how clean or polluted the air is, and what health effects might be a concern.
- **0-50 (Good):** Air quality is considered satisfactory.
- **51-100 (Moderate):** Air is acceptable but there may be a moderate health concern for very sensitive people.
- **101-150 (Unhealthy for Sensitive Groups):** Sensitive groups may experience health effects.
- **151-200 (Unhealthy):** Everyone may begin to experience health effects.
- **201-300 (Very Unhealthy):** Health warnings of emergency conditions.
- **301+ (Hazardous):** Everyone may experience more serious health effects.
        """)
        st.dataframe(aqi_warning, use_container_width=True)
    elif var == 'Temperature (°C)':
        st.markdown("### 🌡️ Temperature Indicators")
        st.write("""
**Temperature (°C)** measures how hot or cold the air is.
- **< 27°C:** Typical for cooler days/mornings in Malaysia.
- **27–33°C:** Typical daytime temperatures.
- **> 33°C:** Hot weather, can cause discomfort and heat-related stress.
        """)
        st.dataframe(indicators, use_container_width=True)
    elif var == 'Humidity (%)':
        st.markdown("### 💧 Humidity Indicators")
        st.write("""
**Humidity (%)** tells you how much water vapor is in the air.
- **60–70%:** Typical range in Malaysia (comfortable).
- **> 80%:** Feels sticky and can affect comfort, may increase risk of mold and heat stress.
        """)
        st.dataframe(indicators, use_container_width=True)
    elif var == 'Wind Speed':
        st.markdown("### 🏴 Wind Speed Indicators")
        st.write("""
**Wind Speed (km/h)** is how fast the air is moving.
- **< 5 km/h:** Calm, little wind.
- **5–20 km/h:** Light to moderate wind, common for Malaysia.
- **> 20 km/h:** Strong wind; may bring changes in weather.
        """)
        st.dataframe(indicators, use_container_width=True)
    elif var == 'Precipitation':
        st.markdown("### 🌧️ Precipitation Indicators")
        st.write("""
**Precipitation (mm)** is how much rain falls.
- **0 mm:** No rain.
- **1–10 mm:** Light to moderate rain.
- **> 10 mm:** Heavy rain or thunderstorm.
        """)
        st.dataframe(indicators, use_container_width=True)
    else:
        st.info("No additional info for this variable.")

# ---- TABS LOGIC ----
if st.session_state.active_tab == "🏠 Overview":
    st.title("🇲🇾 Malaysia Air Quality & Weather Dashboard (2014–2024)")
    st.markdown("**InfoVis Project:** Interactive analytics for Malaysia's air quality & weather data.")

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("States", len(filtered['state'].unique()))
    col2.metric("Years", len(filtered['year'].unique()))
    col3.metric("Months", len(filtered['month_name'].unique()))
    if not filtered.empty:
        avg_val = filtered[var_options[st.session_state.selected_var]].mean()
        col4.metric(f"Average {st.session_state.selected_var}", f"{avg_val:.1f}")
    else:
        col4.metric(f"Average {st.session_state.selected_var}", "N/A")

    st.subheader("Insights & Interpretation")
    if not filtered.empty:
        max_state = state_avg.sort_values(var_options[st.session_state.selected_var], ascending=False).iloc[0]['state']
        st.info(f"**{st.session_state.selected_var}:** The average for your selection is **{avg_val:.1f}**. The state with the highest average is **{max_state}**.")
    else:
        st.warning("No data available for current filter selection.")
    if st.session_state.selected_var == 'Air Quality Index (AQI)' and not filtered.empty:
        extreme = filtered[filtered['pollutant_value'] > 100]
        if not extreme.empty:
            st.warning(f"🚨 {len(extreme)} records have AQI above 100 (Unhealthy) for your current filter!")
        else:
            st.success("No extreme air pollution (AQI > 100) in the current selection.")

elif st.session_state.active_tab == "📈 Trends":
    st.header(f"Monthly & Yearly {st.session_state.selected_var} Trends")

    if not filtered.empty:
        # --- 1. Yearly Trend ---
        st.subheader(f"Yearly {st.session_state.selected_var} Trend (All States Average)")
        yearly_trend = (
            filtered.groupby("year")[var_options[st.session_state.selected_var]].mean().reset_index()
        )
        fig_year = px.line(
            yearly_trend, x="year", y=var_options[st.session_state.selected_var],
            markers=True, title=f"Yearly Average {st.session_state.selected_var} (All States)"
        )
        st.plotly_chart(fig_year, use_container_width=True)

        # --- 2. Monthly Trend with Moving Average ---
        st.subheader(f"Monthly {st.session_state.selected_var} Trend (Moving Average)")
        trend_df = (
            filtered.groupby(['year', 'month_name'])[var_options[st.session_state.selected_var]].mean().reset_index()
        )
        trend_df['month_num'] = trend_df['month_name'].apply(lambda m: pd.to_datetime(m, format='%B').month)
        trend_df = trend_df.sort_values(['year', 'month_num'])
        trend_df['moving_avg'] = trend_df[var_options[st.session_state.selected_var]].rolling(3, min_periods=1).mean()
        fig_ma = px.line(
            trend_df,
            x="month_name",
            y=[var_options[st.session_state.selected_var], "moving_avg"],
            color_discrete_map={
                var_options[st.session_state.selected_var]: 'blue',
                "moving_avg": 'orange'
            },
            line_dash_sequence=['solid', 'dash'],
            title=f"Monthly {st.session_state.selected_var} with 3-Month Moving Average"
        )
        st.plotly_chart(fig_ma, use_container_width=True)

        # --- 3. Boxplot by State ---
        st.subheader(f"{st.session_state.selected_var} Distribution by State (Boxplot)")
        box_fig = px.box(
            filtered, x="state", y=var_options[st.session_state.selected_var],
            title=f"Distribution of {st.session_state.selected_var} Across States"
        )
        st.plotly_chart(box_fig, use_container_width=True)

        # --- 4. Dual-Axis Chart: Compare Two Variables ---
        st.subheader("Dual-Axis Chart: Compare Two Variables")
        dual_axis_var = st.selectbox(
            "Select Second Variable for Dual Axis",
            [k for k in var_options.keys() if k != st.session_state.selected_var],
            key="dual_axis_var"
        )
        # Compute monthly averages for both variables
        dual_df = (
            filtered.groupby(['year', 'month_name'])
            [[var_options[st.session_state.selected_var], var_options[dual_axis_var]]]
            .mean().reset_index()
        )
        dual_df['month_num'] = dual_df['month_name'].apply(lambda m: pd.to_datetime(m, format='%B').month)
        dual_df = dual_df.sort_values(['year', 'month_num'])

        fig_dual = go.Figure()
        # First variable (left axis)
        fig_dual.add_trace(go.Scatter(
            x=dual_df['month_name'] + " " + dual_df['year'].astype(str),
            y=dual_df[var_options[st.session_state.selected_var]],
            name=st.session_state.selected_var,
            mode='lines+markers',
            line=dict(color='royalblue')
        ))
        # Second variable (right axis)
        fig_dual.add_trace(go.Scatter(
            x=dual_df['month_name'] + " " + dual_df['year'].astype(str),
            y=dual_df[var_options[dual_axis_var]],
            name=dual_axis_var,
            mode='lines+markers',
            line=dict(color='orange'),
            yaxis='y2'
        ))
        fig_dual.update_layout(
            title=f"{st.session_state.selected_var} vs {dual_axis_var} (Monthly Average)",
            xaxis=dict(title="Month-Year"),
            yaxis=dict(title=st.session_state.selected_var, color='royalblue'),
            yaxis2=dict(title=dual_axis_var, overlaying='y', side='right', color='orange'),
            legend=dict(orientation="h", x=0, y=-0.2),
            margin=dict(t=40)
        )
        st.plotly_chart(fig_dual, use_container_width=True)

        # --- 5. Your Original Trends Chart (by State and Year, Faceted) ---
        st.subheader(f"Monthly {st.session_state.selected_var} Trend by State & Year (Original)")
        trend_df_original = filtered.groupby(['year', 'month_name', 'state'])[var_options[st.session_state.selected_var]].mean().reset_index()
        fig_trend = px.line(
            trend_df_original, x="month_name", y=var_options[st.session_state.selected_var], color="state",
            facet_col="year", category_orders={"month_name": months},
            markers=True, title=f"Monthly {st.session_state.selected_var} by State and Year"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    else:
        st.info("No data available to plot trends.")

elif st.session_state.active_tab == "📊 Distribution":
    st.header("Distribution & Comparison")
    if not filtered.empty:
        bar_fig = px.bar(state_avg, x="state", y=var_options[st.session_state.selected_var], title=f"Average {st.session_state.selected_var} by State")
        st.plotly_chart(bar_fig, use_container_width=True)
        pie_fig = px.pie(
            state_avg, names="state", values=var_options[st.session_state.selected_var],
            title=f"State Share of Average {st.session_state.selected_var}"
        )
        st.plotly_chart(pie_fig, use_container_width=True)
        st.markdown("#### Top States by Pollution (Progress Bar Table)")
        pollution_by_state = (
            filtered.groupby("state")["pollutant_value"]
            .mean()
            .reset_index()
            .sort_values(by="pollutant_value", ascending=False)
            .rename(columns={"pollutant_value": "Average AQI"})
        )
        top_n = 10
        pollution_by_state = pollution_by_state.head(top_n)
        st.dataframe(
            pollution_by_state,
            column_config={
                "state": st.column_config.TextColumn("State"),
                "Average AQI": st.column_config.ProgressColumn(
                    "Average AQI",
                    format="%.1f",
                    min_value=0,
                    max_value=float(pollution_by_state["Average AQI"].max())
                ),
            },
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Not enough data for distribution charts.")

elif st.session_state.active_tab == "🗺️ Geographic":
    st.header("Interactive Map: Average by State")
    try:
        if not state_avg.empty:
            with open("malaysia_states.geojson", "r") as f:
                gjson = json.load(f)
            state_name_map = {
                "Pulau Pinang": "Penang",
                "Wilayah Persekutuan Kuala Lumpur": "Kuala Lumpur",
                "W.P. Kuala Lumpur": "Kuala Lumpur",
                "Malacca": "Malacca"
            }
            state_avg['state'] = state_avg['state'].replace(state_name_map)
            map_fig = px.choropleth(
                state_avg,
                geojson=gjson,
                featureidkey="properties.name",
                locations='state',
                color=var_options[st.session_state.selected_var],
                color_continuous_scale='OrRd',
                title=f"Average {st.session_state.selected_var} by State (Map)"
            )
            map_fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(map_fig, use_container_width=True)
        else:
            st.info("No data for map.")
    except Exception as e:
        st.info(f"Map unavailable. Error: {e}")
    show_variable_explanation(st.session_state.selected_var)

elif st.session_state.active_tab == "🔮 Forecast":
    st.header(f"Forecast: Next N Months of {st.session_state.selected_var}")
    forecast_months = st.slider("Forecast Horizon (months ahead):", 12, 24, 12)
    if len(st.session_state.selected_states) == 1:
        state = st.session_state.selected_states[0]
        state_df = df[df["state"] == state].sort_values(["year", "month_name"])
        var_col = var_options[st.session_state.selected_var]
        # Create a 'year_month' column for clear timeline
        state_df['month_num'] = state_df['month_name'].apply(lambda m: pd.to_datetime(m, format='%B').month)
        state_df['year_month'] = pd.to_datetime(state_df['year'].astype(str) + '-' + state_df['month_num'].astype(str) + '-01')
        state_df = state_df.dropna(subset=[var_col])
        state_df = state_df.sort_values('year_month')
        if len(state_df) >= 12:
            X = np.arange(len(state_df)).reshape(-1,1)
            y = state_df[var_col].values
            model = LinearRegression().fit(X, y)
            future_X = np.arange(len(state_df), len(state_df) + forecast_months).reshape(-1,1)
            preds = model.predict(future_X)
            # Build future dates
            last_date = state_df['year_month'].iloc[-1]
            future_dates = pd.date_range(last_date + pd.offsets.MonthBegin(), periods=forecast_months, freq='MS')
            # Plot actual + forecasted
            fig = go.Figure()
            # Actual historical
            fig.add_trace(go.Scatter(
                x=state_df['year_month'], y=state_df[var_col],
                mode='lines+markers', name=f"Actual {st.session_state.selected_var}", line=dict(color='royalblue')
            ))
            # Forecast
            fig.add_trace(go.Scatter(
                x=future_dates, y=preds,
                mode='lines+markers', name=f"Forecast {st.session_state.selected_var}",
                line=dict(color='orange', dash='dash')
            ))
            fig.update_layout(
                title=f"{st.session_state.selected_var} Historical & {forecast_months}-Month Forecast ({state})",
                xaxis_title="Year-Month",
                yaxis_title=st.session_state.selected_var,
                legend=dict(orientation="h", x=0, y=-0.2),
                margin=dict(t=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"Forecasted average {st.session_state.selected_var} for {state} in next {forecast_months} months: {preds.mean():.1f}")
        else:
            st.warning("Not enough data for this state to generate a reliable forecast.")
    else:
        st.info("Select a single state in the sidebar to see a forecast.")


elif st.session_state.active_tab == "🗃️ Raw Data":
    st.header("Filtered Data Table")
    st.dataframe(filtered, use_container_width=True)
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Filtered Data as CSV", data=csv, file_name="filtered_malaysia_airquality_weather.csv", mime="text/csv")

# ---- Footer ----
st.markdown("---")
st.caption("2024 SKIH3033 InfoVis Project | Data: Malaysia Air Quality & Weather (2014–2024) - By Mahmoud Musa Uthman (Maahmoudsm1@gmail.com)")
