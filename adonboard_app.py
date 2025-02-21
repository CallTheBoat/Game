import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# Χάρτης με τις μαρίνες και τα δρομολόγια
marinas = {
    "Αθήνα": [37.9838, 23.7275],
    "Μύκονος": [37.4467, 25.3289],
    "Σαντορίνη": [36.3932, 25.4615],
    "Ρόδος": [36.4350, 28.2176],
}

routes = {
    "Αθήνα - Μύκονος": ["Αθήνα", "Μύκονος"],
    "Μύκονος - Σαντορίνη": ["Μύκονος", "Σαντορίνη"],
    "Σαντορίνη - Ρόδος": ["Σαντορίνη", "Ρόδος"],
    "Ρόδος - Αθήνα": ["Ρόδος", "Αθήνα"],
}

players = {
    "Παίκτης 1": {"position": "Αθήνα", "sponsor": "Nike", "likes": 0, "earnings": 0},
    "Παίκτης 2": {"position": "Μύκονος", "sponsor": "Adidas", "likes": 0, "earnings": 0},
}

def roll_dice():
    return random.randint(1, 6)

def move_ship(player):
    route_keys = list(routes.keys())
    selected_route = random.choice(route_keys)
    player["position"] = routes[selected_route][-1]  # Μετακίνηση στο τέλος της διαδρομής
    return selected_route

def update_map():
    m = folium.Map(location=[37.5, 25.0], zoom_start=6)
    
    # Σημεία μαρινών
    for marina, coords in marinas.items():
        folium.Marker(location=coords, popup=marina, icon=folium.Icon(color='blue')).add_to(m)
    
    # Δρομολόγια
    for route, stops in routes.items():
        locations = [marinas[stop] for stop in stops]
        folium.PolyLine(locations, color="red", weight=2.5, opacity=0.8).add_to(m)
    
    return m

st.title("AdOnBoard: Επιτραπέζιο Παιχνίδι Ναυτιλίας")

if st.button("🎲 Ρίξε το Ζάρι!"):
    for player_name, player_data in players.items():
        selected_route = move_ship(player_data)
        st.write(f"{player_name} μετακινείται από {selected_route} και βρίσκεται τώρα στο {player_data['position']}")
        
        # Προσθήκη διαφημιστικών εσόδων
        if player_data["position"] in marinas:
            player_data["earnings"] += random.randint(1000, 5000)  # Τυχαίο ποσό διαφήμισης
            player_data["likes"] += random.randint(10, 100)  # Likes από social media
            st.write(f"Ο χορηγός {player_data['sponsor']} πλήρωσε {player_data['earnings']}€!")

# Εμφάνιση χάρτη
map_object = update_map()
st_folium(map_object, width=700, height=500)

# Προβολή στατιστικών
st.subheader("🔹 Στατιστικά Παικτών")
for player, data in players.items():
    st.write(f"**{player}** - Τοποθεσία: {data['position']}, Χορηγός: {data['sponsor']}, Likes: {data['likes']}, Κέρδη: {data['earnings']}€")
