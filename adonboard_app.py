import streamlit as st
import folium
from streamlit_folium import folium_static
import time
import numpy as np
import pygame

# 🎶 Προσθήκη Background Music
st.markdown(
    """
    <audio autoplay loop>
        <source src="https://www.fesliyanstudios.com/play-mp3/387" type="audio/mp3">
    </audio>
    """,
    unsafe_allow_html=True
)

# 💡 Custom Background Image με Sci-Fi Θέμα
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1524775095153-6d4c75524d36");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()

# 🎲 Επιλογή Διαδρομής με Real-Time Κίνηση
st.title("🌊 Επιλογή Διαδρομής")
routes = {
    "Luxury Tour 🌟": {"start": [36.3932, 25.4615], "end": [37.4467, 25.3289], "desc": "VIP τουριστικό ταξίδι"},
    "Beach Party Route 🎉": {"start": [37.0856, 25.1478], "end": [36.7261, 25.2810], "desc": "Beach party και παραλίες"},
    "Extreme Water Sports 🏄": {"start": [36.434, 28.217], "end": [36.892, 27.287], "desc": "Watersports και extreme events"},
    "Speed Challenge 🏎️": {"start": [37.9838, 23.7275], "end": [37.2634, 23.1592], "desc": "Γρήγορη διαδρομή για αγώνες ταχύτητας"}
}
selected_route = st.selectbox("📍 **Επέλεξε διαδρομή:**", list(routes.keys()))
route_data = routes[selected_route]

# 🌍 Δημιουργία δυναμικού χάρτη με 3D Σκάφος
map = folium.Map(location=[37.5, 24.5], zoom_start=6, tiles="Stamen Terrain")
folium.Marker(route_data["start"], tooltip="Αφετηρία", icon=folium.Icon(color="green", icon="cloud")).add_to(map)
folium.Marker(route_data["end"], tooltip="Προορισμός", icon=folium.Icon(color="red", icon="flag")).add_to(map)

# 🚢 Προσθήκη κινούμενου σκάφους (Real-Time Animation)
ship_icon = folium.Icon(color="blue", icon="ship")
ship_marker = folium.Marker(route_data["start"], icon=ship_icon)
map.add_child(ship_marker)

folium.PolyLine([route_data["start"], route_data["end"]], color="cyan", weight=6, opacity=0.7).add_to(map)
folium_static(map)

st.write(f"📝 **Περιγραφή:** {route_data['desc']}")

# 🔊 Προσθήκη Εφέ Ήχου με Pygame
pygame.mixer.init()
def play_sound():
    pygame.mixer.music.load("https://www.fesliyanstudios.com/play-mp3/640")
    pygame.mixer.music.play()

# 🚀 Animation για Κίνηση Σκάφους
if st.button("⚡ Ξεκίνα το ταξίδι"):
    st.write(f"🏁 **Το σκάφος ξεκινά:** {selected_route}!")

    # Εφέ ήχου όταν ξεκινά η διαδρομή
    play_sound()

    progress_bar = st.progress(0)
    lat_steps = np.linspace(route_data["start"][0], route_data["end"][0], 10)
    lon_steps = np.linspace(route_data["start"][1], route_data["end"][1], 10)

    for i in range(10):
        progress_bar.progress((i + 1) / 10)
        
        # Ανανεώνουμε τη θέση του σκάφους στον χάρτη
        map = folium.Map(location=[lat_steps[i], lon_steps[i]], zoom_start=6, tiles="Stamen Terrain")
        folium.Marker([lat_steps[i], lon_steps[i]], icon=ship_icon).add_to(map)
        folium.PolyLine([route_data["start"], route_data["end"]], color="cyan", weight=6, opacity=0.7).add_to(map)
        folium_static(map)
        
        time.sleep(0.5)

    st.success(f"🎉 **Έφτασες στον προορισμό σου!** {route_data['desc']}")

# 🏆 Floating Panel με Real-Time Status
st.markdown(
    f"""
    <div class="floating-panel">
        <h3>🎮 Κατάσταση Παιχνιδιού</h3>
        <p>🚢 **Διαδρομή:** {selected_route}</p>
        <p>📍 **Αφετηρία:** {route_data['start']}</p>
        <p>🏁 **Προορισμός:** {route_data['end']}</p>
        <p>💰 **Κέρδη:** 150,000€ + Bonus</p>
    </div>
    """,
    unsafe_allow_html=True
)
