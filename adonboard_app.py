import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# ----------------- ΡΥΘΜΙΣΕΙΣ ΕΦΑΡΜΟΓΗΣ -----------------
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Παιχνίδι", layout="wide")
st.title("🚢 AdOnBoard - Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🏴‍☠️")

# ----------------- ΔΕΔΟΜΕΝΑ ΣΚΑΦΩΝ & ΧΟΡΗΓΩΝ -----------------
sponsors = ["Nike", "Red Bull", "Vodafone", "Adidas", "North Face", "Coca-Cola"]
boats = ["BlueWave", "SailVenture", "Golden Horizon", "Sunset Cruiser", "Ocean Explorer"]
boat_capacity = {"BlueWave": 10, "SailVenture": 8, "Golden Horizon": 9, "Sunset Cruiser": 10, "Ocean Explorer": 8}

# ----------------- ΔΗΜΙΟΥΡΓΙΑ ΠΑΙΚΤΩΝ -----------------
st.sidebar.header("📌 Επιλογές Παικτών")
num_players = st.sidebar.slider("Πόσοι παίκτες θα παίξουν; (1-10):", 2, 10, 4)
selected_boat = st.sidebar.selectbox("🚤 Επιλέξτε Σκάφος:", boats)
selected_sponsor = st.sidebar.selectbox("💰 Επιλέξτε Χορηγό:", sponsors)

players = {f"Παίκτης {i+1}": {"θέση": 0, "χρήματα": 100000, "likes": 0, "sponsor": selected_sponsor} for i in range(num_players)}

# ----------------- HOTSPOTS & VIP EVENTS -----------------
hotspots = ["Mykonos Paradise Beach", "Santorini Red Beach", "Rhodes Faliraki", "Zakynthos Navagio", "Corfu Old Town"]
quiet_areas = ["Kythnos Kolona", "Andros Golden Sand", "Lefkada Porto Katsiki", "Alonissos Marine Park"]

# ----------------- LEADERBOARD -----------------
def show_leaderboard():
    leaderboard = pd.DataFrame.from_dict(players, orient='index')[['χρήματα', 'likes']]
    leaderboard = leaderboard.sort_values(by=['χρήματα', 'likes'], ascending=False)
    st.sidebar.subheader("🏆 Leaderboard")
    st.sidebar.dataframe(leaderboard)

# ----------------- ΔΗΜΙΟΥΡΓΙΑ ΔΙΑΔΡΟΜΩΝ ΣΕ ΧΑΡΤΗ -----------------
def draw_map():
    greece_map = folium.Map(location=[37.9838, 23.7275], zoom_start=6)
    
    # Προσθήκη τουριστικών μαρίνων
    marina_locations = {
        "Athens Marina": [37.9402, 23.6524],
        "Mykonos Marina": [37.4467, 25.3289],
        "Santorini Marina": [36.3932, 25.4615],
        "Rhodes Marina": [36.4341, 28.2176],
        "Corfu Marina": [39.624, 19.9215]
    }
    
    for name, coords in marina_locations.items():
        folium.Marker(coords, popup=name, icon=folium.Icon(color='blue', icon='cloud')).add_to(greece_map)
    
    folium_static(greece_map)

# ----------------- ΚΙΝΗΣΗ ΠΑΙΚΤΩΝ & ΔΙΑΔΡΟΜΕΣ -----------------
def roll_dice():
    return random.randint(1, 6)

def move_player(player):
    roll = roll_dice()
    st.write(f"🎲 {player} έριξε **{roll}**!")
    time.sleep(1)
    new_position = (players[player]["θέση"] + roll) % len(hotspots + quiet_areas)
    players[player]["θέση"] = new_position
    current_location = (hotspots + quiet_areas)[new_position]
    
    if current_location in hotspots:
        players[player]["χρήματα"] += 5000
        players[player]["likes"] += 2000
        st.success(f"🔥 Το {player} βρέθηκε σε hotspot! +5000€ και +2000 likes!")
    else:
        players[player]["χρήματα"] += 2000
        st.info(f"🌊 {player} έφτασε σε μια ήσυχη περιοχή. +2000€.")
    
    challenge = random.choice(["Διαφημιστική Καμπάνια!", "Συναυλία Beach Party!", "Χορηγία VIP Event!", "Extreme Sailing Challenge!"])
    st.write(f"📢 {challenge}")

# ----------------- ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ -----------------
if st.button("🎲 Ρίξε το Ζάρι!"):
    for player in players:
        move_player(player)
    draw_map()
    show_leaderboard()

draw_map()
show_leaderboard()
