import streamlit as st
import random
import folium
from streamlit_folium import folium_static
import pandas as pd

# Δημιουργία χάρτη με μαρίνες και διαδρομές
marinas = {
    "Μύκονος": (37.4467, 25.3289),
    "Σαντορίνη": (36.3932, 25.4615),
    "Ρόδος": (36.4349, 28.2176),
    "Αθήνα": (37.9838, 23.7275)
}

routes = {
    "Μύκονος - Σαντορίνη": ["Μύκονος", "Σαντορίνη"],
    "Ρόδος - Αθήνα": ["Ρόδος", "Αθήνα"]
}

def create_map(selected_route=None):
    game_map = folium.Map(location=[37.5, 25.0], zoom_start=6)
    
    # Προσθήκη μαρινών
    for marina, coords in marinas.items():
        folium.Marker(location=coords, popup=marina, icon=folium.Icon(color='blue')).add_to(game_map)
    
    # Προσθήκη διαδρομής
    if selected_route:
        route_coords = [marinas[loc] for loc in routes[selected_route]]
        folium.PolyLine(route_coords, color='red', weight=5).add_to(game_map)
    
    return game_map

# Προφίλ παίκτη
player = {
    "name": "Παίκτης 1",
    "money": 1000000,
    "likes": 0,
    "sponsor": "AdOnBoard",
    "position": "Μύκονος"
}

# Διαφημιστική αξία περιοχών
ad_value = {
    "Μύκονος": 50000,
    "Σαντορίνη": 75000,
    "Ρόδος": 60000,
    "Αθήνα": 40000
}

# Streamlit UI
st.title("🏝️ AdOnBoard - Επιτραπέζιο Ναυτιλίας")
st.sidebar.header("Πλοία & Παίκτες")
st.sidebar.write(f"🎭 {player['name']} - Χορηγός: {player['sponsor']}")
st.sidebar.write(f"💰 Χρήματα: {player['money']} €")
st.sidebar.write(f"👍 Likes: {player['likes']}")

# Επιλογή διαδρομής
selected_route = st.selectbox("Επιλέξτε διαδρομή", list(routes.keys()))

# Ρίψη ζαριού
if st.button("🎲 Ρίξε το ζάρι!"):
    steps = random.randint(1, 2)
    index = routes[selected_route].index(player["position"])
    new_index = min(index + steps, len(routes[selected_route]) - 1)
    player["position"] = routes[selected_route][new_index]
    earnings = ad_value[player["position"]]
    player["money"] += earnings
    player["likes"] += random.randint(100, 500)
    st.success(f"Το πλοίο έφτασε στη {player['position']} και κέρδισε {earnings}€ από χορηγούς!")

# Εμφάνιση χάρτη
folium_static(create_map(selected_route))
