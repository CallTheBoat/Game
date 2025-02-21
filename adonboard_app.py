import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import random

# Δημιουργία του ταμπλό
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Παιχνίδι", layout="wide")
st.title("🚢 AdOnBoard - Το Επιτραπέζιο Παιχνίδι Ναυτιλίας")

# Λίστα με προορισμούς
destinations = ["Καταφύγιο", "Πολικός Αστέρας", "Φανάρι", "Ναυτίλος", "Φάρος", "Άνεμος"]

# Διαδρομές του παιχνιδιού
board_size = len(destinations)
player_positions = {1: 0, 2: 0}
player_money = {1: 1000000, 2: 900000}

# Λειτουργία για το ζάρι
def roll_dice():
    return random.randint(1, 6)

# Δημιουργία ταμπλό
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xticks([])
ax.set_yticks([])

# Θέσεις προορισμών
positions = [(1, 1), (3, 1), (5, 1), (7, 1), (9, 1), (9, 3)]
for i, (x, y) in enumerate(positions):
    ax.text(x, y, destinations[i], ha='center', fontsize=12, bbox=dict(facecolor='blue', alpha=0.5))

# Κουμπί ρίψης ζαριού
if st.button("🎲 Ρίξε το Ζάρι!"):
    dice = roll_dice()
    st.write(f"Το ζάρι έφερε: {dice}")
    
    # Κίνηση του παίκτη
    player_positions[1] = (player_positions[1] + dice) % board_size
    st.write(f"Παίκτης 1 μετακινήθηκε στο {destinations[player_positions[1]]} 🚢")
    
    # Προβολή ταμπλό
    for i, (x, y) in enumerate(positions):
        if i == player_positions[1]:
            ax.text(x, y, "🚢", ha='center', fontsize=15, bbox=dict(facecolor='yellow', alpha=0.5))
    st.pyplot(fig)
    
    # Γεγονός πλοίου
    event = random.choice(["Διαφημιστική Καμπάνια!", "Νέος Διαγωνισμός!", "Χορηγία Vodafone!", "Καταιγίδα στη Θάλασσα!"])
    st.write(f"📢 {event}")
