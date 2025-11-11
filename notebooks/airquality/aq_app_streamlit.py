import streamlit as st
from PIL import Image
from pathlib import Path

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Air Quality Forecast Dashboard",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ Air Quality Forecast Dashboard")
st.markdown("""
Welcome to the **Air Quality Prediction Service**.  
This dashboard visualizes the **PM2.5 air pollution forecasts** and compares them with past observed values.  
""")

root_dir = Path(__file__).parents[2]  # due livelli sopra (es. notebooks/airquality -> progetto root)
forecast_path = root_dir / "docs" / "air-quality" / "assets" / "img" / "pm25_forecast.png"
hindcast_path = root_dir / "docs" / "air-quality" / "assets" / "img" / "pm25_hindcast_1day.png"

# --- DISPLAY FORECAST ---
st.subheader("📈 PM2.5 Forecast for the Next 7 Days")
st.markdown("Predicted air quality levels based on recent weather and pollution data.")

if forecast_path.exists():
    forecast_img = Image.open(forecast_path)
    st.image(forecast_img, use_column_width=True, caption="PM2.5 Forecast")
else:
    st.warning("⚠️ Forecast image not found. Please ensure pm25_forecast.png is in the correct folder.")

# --- DISPLAY HINDCAST ---
st.subheader("🔄 Model Hindcast (1-day Comparison)")
st.markdown("Comparison between **predicted** and **actual** PM2.5 values for previous days.")

if hindcast_path.exists():
    hindcast_img = Image.open(hindcast_path)
    st.image(hindcast_img, use_column_width=True, caption="PM2.5 Hindcast (Predicted vs Actual)")
else:
    st.warning("⚠️ Hindcast image not found. Please ensure pm25_hindcast_1day.png is in the correct folder.")

# --- FOOTER ---
st.markdown("""
---
🌍 *This visualization is part of the ID2223 Lab 1: Scalable Machine Learning & Deep Learning project.*  
Developed by [Emanuele Minotti & Stefano Romano].
""")
