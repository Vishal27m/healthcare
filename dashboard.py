# ==========================================
# EPI-Optim - FINAL STARTUP DASHBOARD
# ==========================================

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from forecasting import generate_combined_forecast, get_forecast_summary, forecast_cases

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="EPI-Optim", layout="wide")

# -------------------------------
# ENHANCED CSS STYLING
# -------------------------------
st.markdown("""
<style>

/* Main background & layout */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #000000 !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%);
    color: white !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: white !important;
}

section[data-testid="stSidebar"] h2 {
    color: white !important;
}

section[data-testid="stSidebar"] p {
    color: white !important;
}

/* Navigation buttons - white text */
.stRadio > label {
    color: white !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

.stRadio > label span {
    color: white !important;
}

.stRadio > label div {
    color: white !important;
}

/* Main heading */
h1 {
    color: #000000 !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    margin-bottom: 0.5rem !important;
    text-shadow: none;
}

/* Subheadings - dark black */
h2, h3 {
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 0.8rem !important;
}

/* Descriptions and placeholder text - dark black */
p, div, span, label {
    color: #000000 !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}

/* Metric cards - enhanced */
[data-testid="metric-container"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.12);
    border-left: 5px solid #0d47a1;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0px 12px 32px rgba(0,0,0,0.16);
}

/* Metric labels and values - dark black */
[data-testid="metric-container"] label {
    color: #000000 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

[data-testid="metric-container"] > div > div {
    color: #000000 !important;
    font-weight: 800 !important;
    font-size: 2.2rem !important;
}

/* Alerts - improved styling */
.alert-red {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    padding: 15px 18px;
    border-radius: 12px;
    color: #b71c1c !important;
    font-weight: 700 !important;
    border-left: 4px solid #d32f2f;
    margin: 10px 0;
    box-shadow: 0px 4px 12px rgba(211, 47, 47, 0.15);
    font-size: 1.05rem !important;
}

.alert-green {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 15px 18px;
    border-radius: 12px;
    color: #1b5e20 !important;
    font-weight: 700 !important;
    border-left: 4px solid #388e3c;
    margin: 10px 0;
    box-shadow: 0px 4px 12px rgba(56, 142, 60, 0.15);
    font-size: 1.05rem !important;
}

/* Tables - enhanced */
[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 10px !important;
    overflow: hidden;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

[data-testid="stDataFrame"] td {
    color: #000000 !important;
    font-weight: 500 !important;
}

[data-testid="stDataFrame"] th {
    background-color: #f0f4f8 !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Charts container */
[data-testid="stPlotlyContainer"] {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin: 15px 0;
}

/* Container padding */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    color: #000000 !important;
}

/* Section separators */
hr {
    border: none;
    border-top: 2px solid #d0d0d0;
    margin: 2rem 0;
}

/* Button styling */
button {
    background-color: #0d47a1 !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
}

button:hover {
    background-color: #0a3577 !important;
}

/* Info boxes */
[data-testid="stInfo"] {
    background-color: #e3f2fd !important;
    border-left: 4px solid #0d47a1 !important;
    color: #000000 !important;
}

[data-testid="stInfo"] p {
    color: #000000 !important;
}

/* Warning boxes */
[data-testid="stWarning"] {
    background-color: #fff3e0 !important;
    border-left: 4px solid #f57c00 !important;
    color: #000000 !important;
}

[data-testid="stWarning"] p {
    color: #000000 !important;
}

/* Select box and input text */
input, select {
    color: #000000 !important;
}

input::placeholder {
    color: #666666 !important;
}

/* Markdown text */
[data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
latest_data = pd.read_csv("latest_data.csv")
allocation_df = pd.read_csv("allocation.csv")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🏥 EPI-Optim")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Dashboard", "Forecasting", "Insights"])
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
if len(latest_data) > 0:
    st.sidebar.metric("High Risk Zones", int((latest_data['shortage'] > 0).sum()))
    st.sidebar.metric("Total Zones", len(latest_data))

# -------------------------------
# DASHBOARD PAGE
# -------------------------------
if page == "Dashboard":

    st.title("📊 AI Healthcare Dashboard")
    st.markdown("Real-time disease monitoring and resource allocation system")
    st.markdown("---")

    # ---------------------------
    # METRICS
    # ---------------------------
    st.subheader("📈 Key Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        col1.metric("🏘️ Total Zones", len(latest_data))
    
    with col2:
        col2.metric("⚠️ High Risk Zones", int((latest_data['shortage'] > 0).sum()))
    
    with col3:
        col3.metric("🔴 Total Cases", int(latest_data['predicted_cases'].sum()))

    st.markdown("---")

    # ---------------------------
    # MAP SECTION
    # ---------------------------
    st.subheader("🗺️ Disease Spread Map")
    st.markdown("*Hover over markers to see zone details*")

    zone_coords = {
        "Zone_1": [13.0827, 80.2707],
        "Zone_3": [13.07, 80.28],
        "Zone_4": [13.09, 80.26],
        "Zone_8": [13.03, 80.27],
        "Zone_9": [13.10, 80.25]
    }

    m = folium.Map(
        location=[13.08, 80.27],
        zoom_start=12,
        tiles="cartodb positron"
    )

    for _, row in latest_data.iterrows():
        coords = zone_coords.get(row['zone'], [13.08, 80.27])

        color = "red" if row['shortage'] > 0 else "green"

        folium.CircleMarker(
            location=coords,
            radius=10,
            color=color,
            fill=True,
            fill_opacity=0.9,
            popup=f"{row['zone']} | Cases: {row['predicted_cases']} | Shortage: {row['shortage']}"
        ).add_to(m)

    st_folium(m, use_container_width=True, height=500)

    st.markdown("---")

    # ---------------------------
    # TWO COLUMN LAYOUT
    # ---------------------------
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        # ---------------------------
        # RESOURCE ALLOCATION
        # ---------------------------
        st.subheader("🚑 Resource Allocation")
        st.markdown("*Current resource distribution across zones*")
        st.dataframe(allocation_df, use_container_width=True, hide_index=True)

    with col_right:
        # ---------------------------
        # CHART
        # ---------------------------
        st.subheader("📊 Cases by Zone")
        st.bar_chart(latest_data.set_index('zone')['predicted_cases'])

    st.markdown("---")

    # ---------------------------
    # ALERTS SECTION
    # ---------------------------
    st.subheader("⚠️ Health Alerts")
    
    alert_cols = st.columns(2)
    col_idx = 0
    
    for _, row in latest_data.iterrows():
        with alert_cols[col_idx % 2]:
            if row['shortage'] > 0:
                st.markdown(f"<div class='alert-red'>🔴 {row['zone']} | {int(row['shortage'])} beds needed</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='alert-green'>🟢 {row['zone']} | Stable</div>", unsafe_allow_html=True)
        col_idx += 1

# -------------------------------
# FORECASTING PAGE
# -------------------------------
elif page == "Forecasting":

    st.title("🔮 Disease Cases Forecasting")
    st.markdown("Predict future disease cases and trends for proactive resource planning")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_zone = st.selectbox("📍 Select Zone", latest_data['zone'].unique())
    
    with col2:
        forecast_days = st.selectbox("📅 Forecast Period", [7, 14, 30], format_func=lambda x: f"{x} Days")
    
    with col3:
        st.metric("Selected Zone", selected_zone)

    st.markdown("---")

    # Generate forecast
    combined_data = generate_combined_forecast(latest_data, selected_zone, forecast_days)

    if combined_data is not None:
        # Create plotly chart with confidence intervals
        fig = go.Figure()

        # Historical data
        historical = combined_data[combined_data['type'] == 'Historical']
        fig.add_trace(go.Scatter(
            x=historical['date'],
            y=historical['predicted_cases'],
            mode='lines',
            name='Historical Data',
            line=dict(color='#0d47a1', width=3),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Cases:</b> %{y:.0f}<extra></extra>'
        ))

        # Forecast
        forecast = combined_data[combined_data['type'] == 'Forecast']
        fig.add_trace(go.Scatter(
            x=forecast['date'],
            y=forecast['predicted_cases'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#ff6b6b', width=3, dash='dash'),
            marker=dict(size=8),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Predicted Cases:</b> %{y:.0f}<extra></extra>'
        ))

        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast['date'].tolist() + forecast['date'].tolist()[::-1],
            y=forecast['upper_bound'].tolist() + forecast['lower_bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 107, 107, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=True,
            name='95% Confidence Interval',
            hoverinfo='skip'
        ))

        fig.update_layout(
            title=f"Case Forecast for {selected_zone} ({forecast_days} Days)",
            xaxis_title='Date',
            yaxis_title='Number of Cases',
            template='plotly_white',
            height=500,
            hovermode='x unified',
            plot_bgcolor='rgba(240, 244, 248, 0.5)',
            font=dict(size=12, color='#2c3e50', family='Arial')
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Forecast Summary
        summary = get_forecast_summary(forecast)

        if summary:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("📊 Avg Cases", summary['avg_cases'])
            with col2:
                st.metric("📈 Peak Cases", summary['max_cases'])
            with col3:
                st.metric("📉 Min Cases", summary['min_cases'])
            with col4:
                st.metric("🎯 Trend", summary['trend'])
            with col5:
                color = "🟢" if summary['growth_rate'] < 0 else "🔴"
                st.metric("📊 Growth Rate", f"{color} {summary['growth_rate']}%")

        st.markdown("---")

        # Detailed forecast table
        st.subheader("📋 Detailed Forecast")
        forecast_display = forecast[['date', 'predicted_cases', 'upper_bound', 'lower_bound']].copy()
        forecast_display.columns = ['Date', 'Predicted Cases', 'Upper Bound (95%)', 'Lower Bound (95%)']
        forecast_display['Date'] = forecast_display['Date'].dt.strftime('%Y-%m-%d')
        forecast_display = forecast_display.reset_index(drop=True)
        
        st.dataframe(forecast_display, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.info("💡 **How to read this forecast:**\n"
                "- **Predicted Cases:** Expected number of cases based on historical trends\n"
                "- **Confidence Interval:** Range where we're 95% confident the actual value will fall\n"
                "- **Growth Rate:** Percentage change from first to last day of forecast\n"
                "- Use this to plan resource allocation and preparations")

    else:
        st.warning("⚠️ Insufficient data to generate forecast for this zone")

# -------------------------------
# INSIGHTS PAGE (SHAP)
# -------------------------------
elif page == "Insights":

    st.title("🧠 AI Insights & Model Explanations")
    st.markdown("Understand how the AI model makes predictions")
    st.markdown("---")

    try:
        shap_df = pd.read_csv("shap_values.csv")
        
        st.subheader("📊 Feature Importance")
        st.markdown("*How different factors influence predictions*")
        
        chart_data = shap_df.abs().mean().sort_values(ascending=True)
        st.bar_chart(chart_data)
        
        st.markdown("---")
        st.info("💡 These SHAP values show which factors have the most impact on predictions. Higher values = greater influence.")
        
    except FileNotFoundError:
        st.warning("⚠️ No SHAP values found. Run the prediction analysis in the notebook to generate explanations.")