import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import math

# ---------- Utility Functions ----------
EARTH_RADIUS_KM = 6371.0
KM_TO_NM = 0.539957  # 1 km ~ 0.54 nautical miles

def haversine_distance_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return EARTH_RADIUS_KM * c

def distance_nm(lat1, lon1, lat2, lon2):
    return haversine_distance_km(lat1, lon1, lat2, lon2) * KM_TO_NM

# ---------- Επιλογή Ρόλου ----------
st.set_page_config(page_title="Unified Maritime Board Game", layout="wide")
st.title("Unified Maritime Board Game")

role = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])
if role == "Passenger":
    st.info("As a Passenger, explore destinations and earn rewards!")
elif role == "Ship Owner":
    st.info("As a Ship Owner, manage your routes and maximize profits!")
elif role == "Sponsor":
    st.info("As a Sponsor, choose routes to advertise your brand!")

# ---------- Tab 1: Dynamic Route Simulation ----------
def dynamic_route_simulation():
    st.subheader("Dynamic Route Simulation")
    # Session state για διαδρομές και προορισμό
    if "routes" not in st.session_state:
        st.session_state["routes"] = {
            "Santorini - Mykonos": [(36.3932, 25.4615), (37.4467, 25.3289)],
            "Rhodes - Athens": [(36.4349, 28.2176), (37.9838, 23.7275)]
        }
    if "selected_route" not in st.session_state:
        st.session_state["selected_route"] = list(st.session_state["routes"].keys())[0]
    if "current_dist_nm" not in st.session_state:
        coords = st.session_state["routes"][st.session_state["selected_route"]]
        st.session_state["current_dist_nm"] = distance_nm(*coords[0], *coords[1])
    if "progress_nm" not in st.session_state:
        st.session_state["progress_nm"] = 0.0

    # Φόρμα για προσθήκη νέας διαδρομής
    st.subheader("Add a New Route")
    with st.form("route_form"):
        route_name = st.text_input("Route Name", placeholder="e.g. Corfu - Patras")
        start_lat = st.number_input("Start Latitude", value=36.0)
        start_lon = st.number_input("Start Longitude", value=25.0)
        end_lat = st.number_input("End Latitude", value=37.0)
        end_lon = st.number_input("End Longitude", value=25.5)
        submitted = st.form_submit_button("Add Route")
        if submitted:
            if route_name.strip() != "":
                st.session_state["routes"][route_name] = [(start_lat, start_lon), (end_lat, end_lon)]
                st.success(f"Route '{route_name}' added successfully!")
            else:
                st.warning("Please enter a valid route name.")
    
    selected_route = st.selectbox("Choose a Route:", list(st.session_state["routes"].keys()))
    if selected_route != st.session_state["selected_route"]:
        st.session_state["selected_route"] = selected_route
        coords = st.session_state["routes"][selected_route]
        st.session_state["current_dist_nm"] = distance_nm(*coords[0], *coords[1])
        st.session_state["progress_nm"] = 0.0
    coords = st.session_state["routes"][st.session_state["selected_route"]]
    total_dist_nm = st.session_state["current_dist_nm"]
    progress_nm = st.session_state["progress_nm"]
    remaining_nm = total_dist_nm - progress_nm
    if remaining_nm < 0:
        remaining_nm = 0
    st.write(f"**Total Route Distance:** ~{total_dist_nm:.2f} NM")
    st.write(f"**Ship has traveled:** ~{progress_nm:.2f} NM")
    st.write(f"**Remaining:** ~{remaining_nm:.2f} NM")

    # Δημιουργία χάρτη
    m = folium.Map(location=coords[0], zoom_start=6)
    folium.Marker(coords[0], tooltip="Start").add_to(m)
    folium.Marker(coords[1], tooltip="Destination").add_to(m)
    fraction = progress_nm / total_dist_nm if total_dist_nm > 0 else 0
    if fraction > 1:
        fraction = 1
    lat1, lon1 = coords[0]
    lat2, lon2 = coords[1]
    current_lat = lat1 + fraction * (lat2 - lat1)
    current_lon = lon1 + fraction * (lon2 - lon1)
    folium.Marker(
        [current_lat, current_lon],
        icon=folium.Icon(color="blue"),
        tooltip=f"Ship Position: {progress_nm:.2f} / {total_dist_nm:.2f} NM"
    ).add_to(m)
    
    if st.button("Roll the Dice (Dynamic Route)"):
        dice_value = random.randint(1, 6)
        st.success(f"You rolled: {dice_value}")
        move_nm = min(dice_value, remaining_nm)
        st.session_state["progress_nm"] += move_nm
        st.info(f"The ship moved {move_nm:.2f} NM forward.")
    st.subheader("Dynamic Route Map")
    st_folium(m, width=800, height=500)
    
    # Εάν ο ρόλος είναι Sponsor, εμφάνισε επιπλέον Advertising Dashboard
    if role == "Sponsor":
        st.markdown("### Advertising Dashboard")
        reach = random.randint(5000, 50000)
        st.metric("Potential Engagement", f"{reach} impressions")
        st.write("Select a Passenger for Sponsored Content:")
        passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
        selected_passenger = st.selectbox("Select a Passenger:", passengers)
        engagement = random.randint(1000, 10000)
        st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

# ---------- Tab 2: Board Game Simulation ----------
def board_game_simulation():
    st.subheader("Board Game Simulation")
    # Ορισμός board squares (κουτάκια)
    BOX_SIZE = 0.02  # μέγεθος για σχεδίαση ορθογωνίων
    board_squares = [
        {"name": "Santorini", "coords": (36.3932, 25.4615), "event": ""},
        {"name": "Choppy Seas", "coords": (36.50, 25.50), "event": "Choppy seas! Stay here for one turn."},
        {"name": "Mystery Island", "coords": (36.70, 25.60), "event": ""},
        {"name": "Storm Area", "coords": (36.90, 25.70), "event": "Storm - delay! Lose 1 turn."},
        {"name": "Mykonos", "coords": (37.4467, 25.3289), "event": ""}
    ]
    if "boat_index_board" not in st.session_state:
        st.session_state["boat_index_board"] = 0
    if "skip_turn_board" not in st.session_state:
        st.session_state["skip_turn_board"] = False
    
    # Δημιουργία χάρτη για Board Game
    center_coords = board_squares[0]["coords"]
    m = folium.Map(location=center_coords, zoom_start=7)
    for i, square in enumerate(board_squares):
        lat, lon = square["coords"]
        bounds = [(lat - BOX_SIZE, lon - BOX_SIZE), (lat + BOX_SIZE, lon + BOX_SIZE)]
        folium.Rectangle(
            bounds=bounds,
            color='green',
            fill=True,
            fill_opacity=0.2,
            tooltip=f"{i}. {square['name']}"
        ).add_to(m)
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(html=f"""<div style="font-size: 12pt; color: darkgreen">{square['name']}</div>""")
        ).add_to(m)
    current_square = board_squares[st.session_state["boat_index_board"]]
    folium.Marker(
        current_square["coords"],
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip=f"Boat is here: {current_square['name']}"
    ).add_to(m)
    
    st_folium(m, width=800, height=500)
    if st.button("Roll the Dice (Board Game)"):
        if st.session_state["skip_turn_board"]:
            st.warning("You must skip this turn due to a previous event!")
            st.session_state["skip_turn_board"] = False
        else:
            dice = random.randint(1, 6)
            st.success(f"You rolled: {dice}")
            new_index = st.session_state["boat_index_board"] + dice
            if new_index >= len(board_squares):
                new_index = len(board_squares) - 1
            st.session_state["boat_index_board"] = new_index
            current_square = board_squares[new_index]
            if current_square["event"]:
                st.info(f"Event on {current_square['name']}: {current_square['event']}")
                if ("skip" in current_square["event"].lower() or
                    "delay" in current_square["event"].lower() or
                    "lose" in current_square["event"].lower()):
                    st.session_state["skip_turn_board"] = True
    current_sq = board_squares[st.session_state["boat_index_board"]]
    st.write(f"**Boat is now at**: {current_sq['name']}")
    if current_sq["event"]:
        st.write(f"**Square Event**: {current_sq['event']}")
    else:
        st.write("No special event here.")
    
    # Εάν ο ρόλος είναι Sponsor, εμφάνισε επιπλέον Advertising Dashboard
    if role == "Sponsor":
        st.markdown("### Advertising Dashboard")
        reach = random.randint(5000, 50000)
        st.metric("Potential Engagement", f"{reach} impressions")
        st.write("Select a Passenger for Sponsored Content:")
        passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
        selected_passenger = st.selectbox("Select a Passenger:", passengers, key="board_passenger")
        engagement = random.randint(1000, 10000)
        st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

# ---------- Main App: Tabs ----------
tabs = st.tabs(["Dynamic Route Simulation", "Board Game Simulation"])
with tabs[0]:
    dynamic_route_simulation()
with tabs[1]:
    board_game_simulation()
