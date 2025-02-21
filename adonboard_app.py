import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import time

# Δημιουργία του χάρτη με κεντρική τοποθεσία την Ελλάδα
def create_map():
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=6)
    
    # Προσθήκη μαρινών με markers
    marinas = {
        "Αθήνα": [37.9838, 23.7275],
        "Μύκονος": [37.4467, 25.3289],
        "Σαντορίνη": [36.3932, 25.4615],
        "Ρόδος": [36.4349, 28.2176],
        "Κέρκυρα": [39.6249, 19.9223],
        "Χανιά": [35.5122, 24.0156]
    }
    
    for name, coords in marinas.items():
        folium.Marker(coords, popup=name, icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
    
    return m, marinas

# Δρομολόγια διαθέσιμα για τους παίκτες
def get_routes():
    return {
        "Αθήνα -> Μύκονος": ["Αθήνα", "Μύκονος"],
        "Μύκονος -> Σαντορίνη": ["Μύκονος", "Σαντορίνη"],
        "Σαντορίνη -> Ρόδος": ["Σαντορίνη", "Ρόδος"],
        "Ρόδος -> Αθήνα": ["Ρόδος", "Αθήνα"],
        "Κέρκυρα -> Χανιά": ["Κέρκυρα", "Χανιά"]
    }

# Κίνηση του σκάφους στη διαδρομή
def move_boat(route, marinas):
    st.write("🚢 Το σκάφος ξεκινά το ταξίδι του!")
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=6)
    
    # Προσθήκη σημείων της διαδρομής
    coords = [marinas[point] for point in route]
    folium.PolyLine(coords, color="red", weight=3, opacity=0.7).add_to(m)
    
    # Προσθήκη markers
    for point in route:
        folium.Marker(marinas[point], popup=point, icon=folium.Icon(color="green", icon="flag" if point == route[-1] else "ship")).add_to(m)
    
    folium_static(m)
    st.write("✅ Τέλος ταξιδιού!")

# Streamlit UI
st.title("🚢 AdOnBoard - Ναυτιλιακό Επιτραπέζιο Παιχνίδι")

# Δημιουργία και εμφάνιση του αρχικού χάρτη
map_obj, marinas = create_map()
folium_static(map_obj)

# Επιλογή διαδρομής από τον χρήστη
st.subheader("Επιλέξτε Δρομολόγιο")
routes = get_routes()
selected_route_name = st.selectbox("Επιλέξτε μία διαδρομή:", list(routes.keys()))

# Κουμπί για την εκκίνηση του ταξιδιού
if st.button("Ρίξτε το Ζάρι & Ξεκινήστε το Ταξίδι!"):
    move_boat(routes[selected_route_name], marinas)
