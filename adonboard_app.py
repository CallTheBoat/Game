import streamlit as st
import math
import folium
from streamlit_folium import st_folium
import random
import time

# Υπολογισμός απόστασης σε ναυτικά μίλια
def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# Αρχικοποίηση session state
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "photo": None
    }

if "monopoly_squares" not in st.session_state:
    st.session_state["monopoly_squares"] = [
        {"name": "Rhodes Start", "coords": (36.4349, 28.2176), "event": "Starting point."},
        {"name": "Square 1", "coords": (36.4000, 28.10), "event": "Engine failure! Lose a turn."},
        {"name": "Square 2", "coords": (36.3000, 28.00), "event": "Beach party! Stay here 1 turn to enjoy."},
        {"name": "Square 3", "coords": (36.2000, 27.90), "event": "Strong currents - move forward 1 extra step."},
        {"name": "Square 4", "coords": (36.1000, 27.80), "event": "Strong winds - slower speed next turn."},
        {"name": "Kos Finish", "coords": (36.8938, 27.2877), "event": "Arrived at Kos!"}
    ]

if "monopoly_index" not in st.session_state:
    st.session_state["monopoly_index"] = 0

if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

if "visited_coords" not in st.session_state:
    st.session_state["visited_coords"] = [st.session_state["monopoly_squares"][0]["coords"]]

# Tabs
tabs = st.tabs(["Profile Setup", "Monopoly Route"])

# TAB 1: Profile Setup
with tabs[0]:
    st.title("Profile Setup")
    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        photo_file = st.file_uploader("Upload a Profile Photo", type=["jpg", "jpeg", "png"])
        if photo_file:
            st.session_state["profile"]["photo"] = photo_file.read()
        if st.form_submit_button("Save"):
            st.success("Profile saved!")

    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Your Profile Photo", width=150)

# TAB 2: Monopoly Game
with tabs[1]:
    st.subheader("Monopoly-Style Route (Rhodes -> Kos) with Dice & Events")
    squares = st.session_state["monopoly_squares"]
    center = squares[0]["coords"]
    mono_map = folium.Map(location=center, zoom_start=6)

    # Προσθήκη markers
    for sq in squares:
        color = "gray"
        if "Finish" in sq["name"]:
            color = "green"
        elif "Start" in sq["name"]:
            color = "blue"
        folium.CircleMarker(
            location=sq["coords"],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            tooltip=f"{sq['name']} | {sq['event']}"
        ).add_to(mono_map)

    # Διαδρομή που διανύθηκε
    folium.PolyLine(st.session_state["visited_coords"], color="orange", weight=4).add_to(mono_map)

    # Δείκτης πλοίου
    current_square = squares[st.session_state["monopoly_index"]]
    folium.Marker(
        location=current_square["coords"],
        tooltip="Your Ship",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mono_map)

    st_folium(mono_map, width=700, height=450)
    st.write(f"**Current Index**: {st.session_state['monopoly_index']} / {len(squares) - 1}")
    st.write(f"**Current Square**: {current_square['name']}")
    st.info(f"Event: {current_square['event']}")

    if st.button("Roll the Dice"):
        dice = random.randint(1, 6)
        st.success(f"You rolled a {dice}!")

        steps_remaining = dice
        while steps_remaining > 0 and st.session_state["monopoly_index"] < len(squares) - 1:
            old_index = st.session_state["monopoly_index"]
            st.session_state["monopoly_index"] += 1
            new_index = st.session_state["monopoly_index"]
            startC = squares[old_index]["coords"]
            endC = squares[new_index]["coords"]
            dist_nm = distance_nm(startC[0], startC[1], endC[0], endC[1])
            st.session_state["total_nm"] += dist_nm
            st.session_state["visited_coords"].append(endC)

            st.info(f"Step {dice - steps_remaining + 1}: Moved to {squares[new_index]['name']}")
            steps_remaining -= 1
            time.sleep(0.5)

        final_square = squares[st.session_state["monopoly_index"]]
        st.info(f"Arrived at {final_square['name']}")
        st.info(f"Event: {final_square['event']}")

        if "Lose a turn" in final_square["event"]:
            st.warning("You lose a turn next time (not fully implemented).")
        elif "Beach party" in final_square["event"]:
            st.success("Party time! Stay 1 turn? (not fully implemented).")
        elif "Strong currents" in final_square["event"]:
            st.info("Move forward 1 extra square! (not fully implemented).")
        elif "Strong winds" in final_square["event"]:
            st.info("Slower speed next turn (not fully implemented).")

    if st.session_state["monopoly_index"] == len(squares) - 1:
        st.balloons()
        st.success("Arrived at Kos Finish!")
        if st.button("Restart Route"):
            st.session_state["monopoly_index"] = 0
            st.session_state["visited_coords"] = [squares[0]["coords"]]
            st.session_state["total_nm"] = 0.0
            st.success("Route restarted.")