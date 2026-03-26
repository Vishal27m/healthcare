# ==========================================
# EPI-Optim - FINAL STARTUP DASHBOARD
# ==========================================

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="EPI-Optim", layout="wide")

# -------------------------------
# FINAL CLEAN CSS (VISIBILITY FIXED)
# -------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f7f9fc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d47a1;
    color: white;
}

/* Text visibility fix */
h1, h2, h3 {
    color: #1a1a1a !important;
}

p, div, span {
    color: #333333 !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Alerts */
.alert-red {
    background: #ffe5e5;
    padding: 12px;
    border-radius: 10px;
    color: #b71c1c !important;
    font-weight: bold;
}

.alert-green {
    background: #e8f5e9;
    padding: 12px;
    border-radius: 10px;
    color: #1b5e20 !important;
    font-weight: bold;
}

/* Tables */
[data-testid="stDataFrame"] {
    background-color: white;
}

/* Padding */
.block-container {
    padding-top: 2rem;
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
page = st.sidebar.radio("Navigation", ["Dashboard", "Insights"])

# -------------------------------
# DASHBOARD PAGE
# -------------------------------
if page == "Dashboard":

    st.title("📊 AI Healthcare Dashboard")

    # ---------------------------
    # METRICS
    # ---------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Zones", len(latest_data))
    col2.metric("High Risk Zones", int((latest_data['shortage'] > 0).sum()))
    col3.metric("Total Cases", int(latest_data['predicted_cases'].sum()))

    # ---------------------------
    # MAP
    # ---------------------------
    st.subheader("🗺️ Disease Spread Map")

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

    # ---------------------------
    # ALERTS
    # ---------------------------
    st.subheader("⚠️ Alerts")

    for _, row in latest_data.iterrows():
        if row['shortage'] > 0:
            st.markdown(f"<div class='alert-red'>🔴 {row['zone']} needs {row['shortage']} beds</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-green'>🟢 {row['zone']} stable</div>", unsafe_allow_html=True)

    # ---------------------------
    # RESOURCE ALLOCATION
    # ---------------------------
    st.subheader("🚑 Resource Allocation")

    st.dataframe(allocation_df, use_container_width=True)

    # ---------------------------
    # CHART
    # ---------------------------
    st.subheader("📈 Predicted Cases")

    st.bar_chart(latest_data.set_index('zone')['predicted_cases'])

# -------------------------------
# INSIGHTS PAGE (SHAP)
# -------------------------------
elif page == "Insights":

    st.title("🧠 AI Insights")

    try:
        shap_df = pd.read_csv("shap_values.csv")
        st.bar_chart(shap_df.abs().mean())
    except:
        st.warning("⚠️ Run SHAP in notebook to see explanations")