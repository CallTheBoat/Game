import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

# Δημιουργία του ταμπλό με τις μαρίνες και τις διαδρομές
marinas = {
    "Μύκονος": [37.4467, 25.3289],
    "Σαντορίνη": [36.3932, 25.4615],
    "Ρόδος": [36.434, 28.217],
    "Αθήνα": [37.9838, 23.7275]
}

routes = {
    "Μύκονος - Σαντορίνη": [[37.4467, 25.3289], [36.3932, 25.4615]],
    "Ρόδος - Αθήνα": [[36.434, 28.217], [37.9838, 23.7275]]
}

# Λίστα παικτών και σκαφών
players = {}
boats = {"Speedboat": 8, "Yacht": 10}

# Χορηγοί
sponsors = ["Coca-Cola", "Red Bull", "Nike", "Adidas"]

# Εμφάνιση επιλογών
st.title("AdOnBoard: Επιτραπέζιο Παιχνίδι Ναυτιλίας")
num_players = st.number_input("Πόσοι παίκτες θα παίξουν;", 1, 4, 1)

for i in range(num_players):
    player_name = st.text_input(f"Όνομα Παίκτη {i+1}", f"Παίκτης {i+1}")
    boat_choice = st.selectbox(f"Σκάφος για {player_name}", list(boats.keys()))
    sponsor = np.random.choice(sponsors)
    players[player_name] = {"boat": boat_choice, "sponsor": sponsor, "likes": 0, "position": "Μύκονος"}

# Ρίψη ζαριού
if st.button("🎲 Ρίξε το Ζάρι!"):
    for player in players:
        move = np.random.choice(list(routes.keys()))
        players[player]["position"] = move.split(" - ")[1]
        players[player]["likes"] += np.random.randint(1, 20)
    st.rerun()

# Εμφάνιση χάρτη
st.subheader("🌍 Χάρτης Διαδρομών")
map_ = folium.Map(location=[37.5, 25.0], zoom_start=6)

for name, coords in marinas.items():
    folium.Marker(coords, tooltip=name, icon=folium.Icon(color="blue")).add_to(map_)

for route, coords in routes.items():
    folium.PolyLine(coords, color="red", weight=3, tooltip=route).add_to(map_)

folium_static(map_)

# Προφίλ παικτών
st.subheader("📋 Πληροφορίες Παικτών")
for player, details in players.items():
    st.write(f"**{player}** - Σκάφος: {details['boat']}, Χορηγός: {details['sponsor']}, Τοποθεσία: {details['position']}, Likes: {details['likes']}")
