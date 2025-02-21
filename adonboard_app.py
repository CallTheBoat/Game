import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import random

def draw_map_with_route(start, end, waypoints=[]):
    """Σχεδιάζει τον χάρτη και δείχνει τη διαδρομή του σκάφους."""
    
    m = folium.Map(location=start, zoom_start=7)
    
    # Προσθήκη σημείου εκκίνησης
    folium.Marker(start, tooltip="Αφετηρία", icon=folium.Icon(color='green')).add_to(m)
    
    # Προσθήκη σημείων ενδιάμεσης στάσης
    for point in waypoints:
        folium.Marker(point, tooltip="Στάση", icon=folium.Icon(color='blue')).add_to(m)
    
    # Προσθήκη σημείου τελικού προορισμού
    folium.Marker(end, tooltip="Προορισμός", icon=folium.Icon(color='red')).add_to(m)
    
    # Προσθήκη διαδρομής
    folium.PolyLine([start] + waypoints + [end], color="blue", weight=5, opacity=0.7).add_to(m)
    
    return m

def move_ship(start, end, steps=10):
    """Αναπαριστά την κίνηση του σκάφους από το σημείο εκκίνησης στο σημείο άφιξης."""
    lat_step = (end[0] - start[0]) / steps
    lon_step = (end[1] - start[1]) / steps
    
    positions = [(start[0] + i * lat_step, start[1] + i * lon_step) for i in range(steps + 1)]
    return positions

# Streamlit UI
st.title("Ναυτικό Ταξίδι - Διαδραστικός Χάρτης")

# Τυχαία επιλογή διαδρομής
ports = {
    "Αθήνα": (37.9838, 23.7275),
    "Μύκονος": (37.4467, 25.3289),
    "Σαντορίνη": (36.3932, 25.4615),
    "Ρόδος": (36.4349, 28.2176)
}

start_port, end_port = random.sample(list(ports.values()), 2)
waypoints = random.sample(list(ports.values()), k=random.randint(0, 2))

st.write(f"Διαδρομή από {list(ports.keys())[list(ports.values()).index(start_port)]} προς {list(ports.keys())[list(ports.values()).index(end_port)]}")

# Σχεδίαση αρχικού χάρτη
map_obj = draw_map_with_route(start_port, end_port, waypoints)
map_placeholder = st_folium(map_obj, width=700, height=500)

# Κουμπί για να ξεκινήσει η κίνηση
if st.button("Ξεκίνα το ταξίδι!"):
    positions = move_ship(start_port, end_port)
    
    for pos in positions:
        map_obj = draw_map_with_route(start_port, end_port, waypoints)
        folium.Marker(pos, tooltip="Σκάφος", icon=folium.Icon(color='orange')).add_to(map_obj)
        
        map_placeholder = st_folium(map_obj, width=700, height=500)
        time.sleep(0.5)
