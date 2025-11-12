# app_streamlit.py
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
    """
    Risale le cartelle a partire da `start` finché trova docs/air-quality/assets/img.
    Se non lo trova, usa la stessa struttura relativa alla working dir corrente.
    """
    start = start.resolve()
    for p in [start] + list(start.parents):
        candidate = p / "docs" / "air-quality" / "assets" / "img"
        if candidate.exists():
            return candidate
    # fallback
    return Path.cwd() / "docs" / "air-quality" / "assets" / "img"

HERE = Path(__file__).resolve().parent
IMG_DIR = find_img_dir(HERE)

# ---------------- HELPERS ----------------
def img_to_datauri(path: Path, max_width: int = 420) -> str:
    """
    Carica un'immagine, la ridimensiona (se necessario) e restituisce una data URI base64.
    Se il file non esiste, crea un placeholder grigio.
    """
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
    """Costruisce l'HTML del popup con i due PNG."""
    f = IMG_DIR / f"pm25_forecast_{key}.png"
    h = IMG_DIR / f"pm25_hindcast_1day_{key}.png"
    f_uri = img_to_datauri(f)
    h_uri = img_to_datauri(h)
    return f"""
    <div style="font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;width:460px;">
      <h4 style="margin:0 0 6px 0;">{sensor_name}</h4>
      <div style="font-size:12px;color:#555;margin-bottom:6px;">PM2.5 Forecast (next 7 days)</div>
      <img src="{f_uri}" style="width:100%;border-radius:8px;border:1px solid #eee"/>
      <div style="font-size:12px;color:#555;margin:10px 0 6px 0;">Hindcast (Predicted vs Actual, 1-day)</div>
      <img src="{h_uri}" style="width:100%;border-radius:8px;border:1px solid #eee"/>
    </div>
    """

# ---------------- SENSORS (coord. aggiornabili) ----------------
SENSORS = [
    {"name": "Rådhuset", "key": "radhuset", "lat": 55.6065, "lon": 13.0038},
    {"name": "Dalaplan", "key": "dalaplan", "lat": 55.5868, "lon": 13.0145},
]

# ---------------- LAYOUT ----------------
col_map, col_panel = st.columns([2, 1], gap="large")

with col_map:
    # Tiles chiari stile "seconda mappa"
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

with col_panel:
    st.subheader("Quick view")
    choice = st.radio("Select a sensor", [s["name"] for s in SENSORS], horizontal=False)
    chosen = next(s for s in SENSORS if s["name"] == choice)

    f_path = IMG_DIR / f"pm25_forecast_{chosen['key']}.png"
    h_path = IMG_DIR / f"pm25_hindcast_1day_{chosen['key']}.png"

    st.markdown("**📈 Forecast (next 7 days)**")
    st.image(str(f_path), use_column_width=True, caption=f"PM2.5 Forecast – {chosen['name']}")

    st.markdown("**🔄 Hindcast (predicted vs actual)**")
    st.image(str(h_path), use_column_width=True, caption=f"Hindcast (1-day) – {chosen['name']}")

st.markdown(
    """
    ---
    *This dashboard is part of the ID2223 Lab 1 (Scalable ML & DL).  
    Visualizations show predicted PM2.5 levels and hindcast performance for Malmö sensors.*
    """
)
