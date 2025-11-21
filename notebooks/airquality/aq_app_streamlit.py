import base64
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Air Quality – Malmö", page_icon="🗺️", layout="wide")
st.title("🗺️ Air Quality Forecast – Malmö")
st.markdown(
    "Click a sensor on the map to view **PM2.5 forecast** and the 1-day **hindcast (predicted vs actual)**."
)

# ---------------- PATH DISCOVERY (robusto) ----------------
def find_img_dir(start: Path) -> Path:
    start = start.resolve()
    for p in [start] + list(start.parents):
        candidate = p / "docs" / "air-quality" / "assets" / "img"
        if candidate.exists():
            return candidate
    return Path.cwd() / "docs" / "air-quality" / "assets" / "img"

def find_model_img_dir(start: Path) -> Path:
    start = start.resolve()
    for p in [start] + list(start.parents):
        candidate = p / "notebooks" / "airquality" / "air_quality_model" / "images"
        if candidate.exists():
            return candidate
    return Path.cwd() / "notebooks" / "airquality" / "air_quality_model" / "images"

HERE = Path(__file__).resolve().parent
IMG_DIR = find_img_dir(HERE)
MODEL_IMG_DIR = find_model_img_dir(HERE)

# ---------------- HELPERS ----------------
def img_to_datauri(path: Path, max_width: int = 420) -> str:
    if not path.exists():
        placeholder = Image.new("RGB", (max_width, int(max_width * 0.6)), (240, 240, 240))
        buf = BytesIO()
        placeholder.save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

    img = Image.open(path).convert("RGB")
    if img.width > max_width:
        new_h = int(img.height * (max_width / img.width))
        img = img.resize((max_width, new_h))
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

def popup_html(sensor_name: str, key: str) -> str:
    f = IMG_DIR / f"pm25_forecast_{key}.png"
    f_uri = img_to_datauri(f)
    return f"""
    <div style="font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;width:460px;">
    <h4 style="margin:0 0 6px 0;">{sensor_name}</h4>
    <div style="font-size:12px;color:#555;margin-bottom:6px;">PM2.5 Forecast (next 7 days)</div>
    <img src="{f_uri}" style="width:100%;border-radius:8px;border:1px solid #eee"/>
    </div>
    """

# ---------------- SENSORS ----------------
SENSORS = [
    {"name": "Rådhuset", "key": "radhuset", "lat": 55.6065, "lon": 13.0038},
    {"name": "Dalaplan", "key": "dalaplan", "lat": 55.5868, "lon": 13.0145},
]

# ---------------- MAPPA ----------------
m = folium.Map(location=[55.603, 13.003], zoom_start=13, tiles="CartoDB Positron")

for s in SENSORS:
    popup = folium.Popup(popup_html(s["name"], s["key"]), max_width=500, parse_html=False)
    folium.CircleMarker(
        location=[s["lat"], s["lon"]],
        radius=9,
        weight=2,
        color="#111",
        fill=True,
        fill_color="#2b8a3e",
        fill_opacity=0.9,
        tooltip=s["name"],
        popup=popup,
    ).add_to(m)

st_folium(m, width=None, height=600)

# ---------------- PANNELLO ----------------
st.subheader("Quick view")
choice = st.radio("Select a sensor", [s["name"] for s in SENSORS], horizontal=False)
chosen = next(s for s in SENSORS if s["name"] == choice)

# Paths immagini
f_path = IMG_DIR / f"pm25_forecast_{chosen['key']}.png"
h_path = IMG_DIR / f"pm25_hindcast_1day_{chosen['key']}.png"
model_hindcast_path = MODEL_IMG_DIR / f"pm25_{chosen['key']}_hindcast.png"
feature_importance_path = MODEL_IMG_DIR / f"{chosen['key']}_feature_importance.png"

# Prima riga
row1_col1, row1_col2 = st.columns(2, gap="large")

with row1_col1:
    st.markdown("**📈 Forecast (next 7 days)**")
    st.image(str(f_path), caption=f"PM2.5 Forecast – {chosen['name']}")

with row1_col2:
    st.markdown("**📉 Historical hindcast (last months)**")
    st.image(
        str(model_hindcast_path),
        caption=f"Historical PM2.5 Hindcast (last months) – {chosen['name']}",
    )

# Seconda riga



st.markdown(
    """
    ---
    *This dashboard is part of the ID2223 Lab 1 (Scalable ML & DL).  
    Visualizations show predicted PM2.5 levels, short-term hindcast, historical hindcast and model feature importance for Malmö sensors.*
    """
)
