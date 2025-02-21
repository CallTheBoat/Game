import streamlit as st
import random
import folium
from streamlit_folium import folium_static

# Ορισμός τοποθεσιών μαρινών
marinas = {
    "Αθήνα": [37.9838, 23.7275],
    "Μύκονος": [37.4467, 25.3289],
    "Σαντορίνη": [36.3932, 25.4615],
    "Ρόδος": [36.4344, 28.2170],
    "Κέρκυρα": [39.6243, 19.9217]
}

# Χαρτογράφηση χορηγών
sponsors = ["Coca-Cola", "Nike", "Adidas", "Red Bull", "Samsung"]

# Ρύθμιση αρχικής κατάστασης
if "player_position" not in st.session_state:
    st.session_state.player_position = "Αθήνα"
    st.session_state.balance = 10000
    st.session_state.sponsor = random.choice(sponsors)
    st.session_state.route = []
    
# Εμφάνιση πληροφοριών παίκτη
st.title("🚢 AdOnBoard - Το Επιτραπέζιο Ναυτιλίας")
st.sidebar.subheader("Πληροφορίες Παίκτη")
st.sidebar.write(f"📍 Θέση: {st.session_state.player_position}")
st.sidebar.write(f"💰 Χρήματα: {st.session_state.balance}€")
st.sidebar.write(f"🎽 Χορηγός: {st.session_state.sponsor}")

# Χάρτης
m = folium.Map(location=[37.5, 24.0], zoom_start=6)
for name, coords in marinas.items():
    folium.Marker(coords, tooltip=name, icon=folium.Icon(color="blue", icon="cloud")).add_to(m)
    
# Σχεδίαση διαδρομής αν υπάρχει
if st.session_state.route:
    folium.PolyLine(st.session_state.route, color="blue", weight=5, opacity=0.7).add_to(m)

folium_static(m)

# Ρίψη ζαριού
if st.button("🎲 Ρίξε το Ζάρι!"):
    new_position = random.choice(list(marinas.keys()))
    st.session_state.route.append(marinas[new_position])
    st.session_state.player_position = new_position
    st.session_state.balance += random.randint(500, 2000)
    st.rerun()
