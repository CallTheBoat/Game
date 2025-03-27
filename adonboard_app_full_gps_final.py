
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
import json

def monopoly_auto_update_from_gps(squares):
    gps_file = "monopoly_state.json"
    if not os.path.exists(gps_file):
        st.warning("Δεν βρέθηκε GPS αρχείο. Χρήση προεπιλεγμένης θέσης.")
        return  # απλά δεν αλλάζει index
    try:
        with open(gps_file, "r") as f:
            gps_data = json.load(f)
        lat = gps_data["latitude"]
        lon = gps_data["longitude"]

        def distance_sq(sq):
            sq_lat, sq_lon = sq["coords"]
            return (lat - sq_lat) ** 2 + (lon - sq_lon) ** 2

        closest_index = min(range(len(squares)), key=lambda i: distance_sq(squares[i]))
        st.session_state["monopoly_index"] = closest_index
        st.success(f"✅ Αυτόματη μετακίνηση στο: {squares[closest_index]['name']}")
    except Exception as e:
        st.error(f"Σφάλμα GPS: {e}")

def create_monopoly_map(squares, current_index):
    mono_map = folium.Map(location=squares[0]["coords"], zoom_start=7)
    coords_list = []
    for i, sq in enumerate(squares):
        coords_list.append(sq["coords"])
        folium.CircleMarker(
            location=sq["coords"],
            radius=6,
            color="blue" if i == current_index else "gray",
            fill=True,
            fill_opacity=0.8,
            tooltip=sq["name"]
        ).add_to(mono_map)
    folium.PolyLine(coords_list, color="green", weight=3).add_to(mono_map)
    ship_icon = folium.CustomIcon("https://via.placeholder.com/30x30.png?text=⛵", icon_size=(30, 30))
    folium.Marker(squares[current_index]["coords"], icon=ship_icon, tooltip="📍 Τρέχουσα Θέση").add_to(mono_map)
    return mono_map

st.set_page_config(layout="wide")
st.title("🚢 AddOnBoard - Monopoly με Live Πλοήγηση")

if "monopoly_squares" not in st.session_state:
    st.session_state["monopoly_squares"] = [
        {"name": "Rhodes Start", "coords": (36.4349, 28.2176)},
        {"name": "Kallithea", "coords": (36.3825, 28.2472)},
        {"name": "Lindos", "coords": (36.0917, 28.0850)},
        {"name": "Prasonisi", "coords": (35.8873, 27.7876)},
        {"name": "Karpathos", "coords": (35.5079, 27.2134)},
        {"name": "Kos Finish", "coords": (36.8938, 27.2877)}
    ]
if "monopoly_index" not in st.session_state:
    st.session_state["monopoly_index"] = 0

squares = st.session_state["monopoly_squares"]
monopoly_auto_update_from_gps(squares)
map_obj = create_monopoly_map(squares, st.session_state["monopoly_index"])
st_folium(map_obj, width=800, height=500)

current = squares[st.session_state["monopoly_index"]]
st.markdown(f"### 📍 Τοποθεσία: **{current['name']}**")
st.info("Ο χάρτης ενημερώνεται αυτόματα με βάση live GPS δεδομένα (αν υπάρχει τοπικά το monopoly_state.json)")
