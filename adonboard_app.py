import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Διαμόρφωση ταμπλό
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Ναυτιλίας", layout="wide")

# Χάρτης της Ελλάδας ως βάση του ταμπλό
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Ταμπλό: Διαδρομές στη Ναυτιλία")

# Σημεία σταθμών
stations = {
    "Θεσσαλονίκη": (1, 9),
    "Καβάλα": (3, 8),
    "Λήμνος": (5, 7),
    "Μυτιλήνη": (7, 6),
    "Χίος": (8, 5),
    "Σύρος": (6, 3),
    "Πειραιάς": (4, 2),
    "Χανιά": (2, 1)
}

# Σχεδίαση διαδρομών
for key, value in stations.items():
    ax.scatter(value[0], value[1], color='blue', s=100)
    ax.text(value[0] + 0.2, value[1], key, fontsize=12, color='black')

# Παίκτες και θέσεις
players = {"Παίκτης 1": [1, 9], "Παίκτης 2": [1, 9]}
player_icons = {"Παίκτης 1": "🚢", "Παίκτης 2": "⛵"}

# Προσθήκη κουμπιού για ρίψη ζαριού
st.sidebar.title("Πλοία & Παίκτες")
if st.sidebar.button("🎲 Ρίξε το Ζάρι!"):
    for player in players.keys():
        move = random.randint(1, 3)
        players[player][0] = min(players[player][0] + move, 10)
        players[player][1] = max(players[player][1] - move, 1)
        st.sidebar.write(f"{player} κινήθηκε κατά {move} θέσεις!")
        
    # Ενημέρωση ταμπλό
    for player, position in players.items():
        ax.scatter(position[0], position[1], color='red', s=150, label=player_icons[player])
    st.pyplot(fig)
    time.sleep(1)

# Παρουσίαση ταμπλό
st.title("AdOnBoard - Το Επιτραπέζιο Ναυτιλίας")
st.write("### 📌 Θέσεις Παικτών στο Ταμπλό")
st.pyplot(fig)

# Διαφήμιση και ειδικές κάρτες
if random.random() > 0.7:
    st.success("🎉 Διαφημιστική καμπάνια της AdOnBoard! Κέρδισες μπόνους!")
