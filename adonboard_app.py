import streamlit as st
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ορισμός του ταμπλό
board_positions = [
    "Καταφύγιο", "Πολικός Αστέρας", "Φάρος", "Ναυτίλος", "Ανεμος", "Φυγή", "Νησί", "Λιμάνι"
]

# Σχεδιασμός του ταμπλό
board_grid = np.zeros((3, 3))

# Εικόνες και εικονίδια
icons = {
    "Καταφύγιο": "🏠", "Πολικός Αστέρας": "🌟", "Φάρος": "🚢", "Ναυτίλος": "⚓", "Ανεμος": "💨", "Φυγή": "⛵", "Νησί": "🏝️", "Λιμάνι": "⚓"
}

# Θέση παικτών
player_positions = {1: 0, 2: 0}

# Χρήματα παικτών
player_money = {1: 1000000, 2: 900000}

# Ρίψη ζαριού με animation
def roll_dice():
    for _ in range(10):
        st.session_state["dice"] = random.randint(1, 6)
        time.sleep(0.1)
    return st.session_state["dice"]

# Κίνηση παικτών
def move_player(player):
    roll = roll_dice()
    player_positions[player] = (player_positions[player] + roll) % len(board_positions)
    st.session_state["message"] = f"Παίκτης {player} κινήθηκε στο {board_positions[player_positions[player]]} {icons[board_positions[player_positions[player]]]}"

# Σχεδίαση ταμπλό
def draw_board():
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(board_grid, annot=np.array(board_positions).reshape(3, 3), fmt="", cmap="Blues", linewidths=2, linecolor='black', cbar=False, ax=ax)
    st.pyplot(fig)

# UI Streamlit
st.title("AdOnBoard - Επιτραπέζιο Ναυτιλίας 🏴‍☠️")
st.subheader("🔹 Θέσεις Παικτών στο Ταμπλό")
draw_board()

for player in player_positions:
    st.write(f"**Παίκτης {player}**: Θέση -> {board_positions[player_positions[player]]} {icons[board_positions[player_positions[player]]]} | Χρήματα: {player_money[player]}")

st.subheader("🎲 Ρίξε το Ζάρι!")
if "dice" not in st.session_state:
    st.session_state["dice"] = 1

st.image(f"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Dice-{st.session_state['dice']}-b.svg/120px-Dice-{st.session_state['dice']}-b.svg.png")

if st.button("Ρίξε το Ζάρι! (Παίκτης 1)"):
    move_player(1)

if "message" in st.session_state:
    st.success(st.session_state["message"])

if st.button("Ρίξε το Ζάρι! (Παίκτης 2)"):
    move_player(2)

st.subheader("📍 Κατάσταση Παικτών")
for player in player_positions:
    st.write(f"**Παίκτης {player}**: Θέση -> {board_positions[player_positions[player]]} {icons[board_positions[player_positions[player]]]} | Χρήματα: {player_money[player]}")
