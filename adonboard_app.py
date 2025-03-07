import streamlit as st
import folium
from streamlit_folium import folium_static
import time
import base64

# 💡 Προσθήκη Custom Background Image
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1501594907352-04cda38ebc29");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()

# 🌊 UI Styling - CSS για Floating Panel
st.markdown(
    """
    <style>
    .floating-panel {
        background: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 15px;
        color: white;
        position: fixed;
        top: 20px;
        right: 20px;
        width: 300px;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff8c00, #ff4500);
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        transition: 0.3s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎲 Επιλογή Διαδρομής & Προσθήκη Animation
st.title("⛵ Επιλογή Διαδρομής")
routes = {
    "Luxury Tour": {"start": [36.3932, 25.4615], "end": [37.4467, 25.3289], "desc": "VIP τουριστικό ταξίδι"},
    "Beach Party Route": {"start": [37.0856, 25.1478], "end": [36.7261, 25.2810], "desc": "Beach party και παραλίες"},
    "Extreme Water Sports": {"start": [36.434, 28.217], "end": [36.892, 27.287], "desc": "Events με extreme sports"},
    "Speed Challenge": {"start": [37.9838, 23.7275], "end": [37.2634, 23.1592], "desc": "Αγώνας ταχύτητας"}
}

selected_route = st.selectbox("📌 Επίλεξε διαδρομή:", list(routes.keys()))
route_data = routes[selected_route]

# 🌍 Δημιουργία δυναμικού χάρτη
map = folium.Map(location=[37.5, 24.5], zoom_start=6)
folium.Marker(route_data["start"], tooltip="Αφετηρία", icon=folium.Icon(color="green")).add_to(map)
folium.Marker(route_data["end"], tooltip="Προορισμός", icon=folium.Icon(color="red")).add_to(map)
folium.PolyLine([route_data["start"], route_data["end"]], color="blue", weight=5).add_to(map)
folium_static(map)

st.write(f"📝 Περιγραφή: {route_data['desc']}")

# 🚀 Animation Κίνησης Σκάφους
if st.button("🚀 Ξεκίνα το ταξίδι"):
    st.write(f"🏁 Το σκάφος ξεκινά: {selected_route}!")

    # Προσθήκη Progress Bar Animation
    progress_bar = st.progress(0)
    for i in range(10):
        progress_bar.progress((i + 1) / 10)
        time.sleep(0.5)

    st.success(f"🎉 Έφτασες στον προορισμό σου! {route_data['desc']}")

# 🏆 Floating Panel με Στοιχεία Παιχνιδιού
st.markdown(
    f"""
    <div class="floating-panel">
        <h4>🎮 Κατάσταση Παιχνιδιού</h4>
        <p>🚢 Διαδρομή: {selected_route}</p>
        <p>📍 Αφετηρία: {route_data['start']}</p>
        <p>🏁 Προορισμός: {route_data['end']}</p>
        <p>💰 Κέρδη: 100,000€ + Bonus</p>
    </div>
    """,
    unsafe_allow_html=True
)
