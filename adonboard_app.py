import streamlit as st
import pandas as pd
import numpy as np
import time

# 🎯 Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="AdOnBoard - Ναυτιλιακό Επιτραπέζιο", layout="wide")

# 🏝️ Εικόνα Ταμπλό (χρησιμοποίησε την εικόνα που έχουμε φτιάξει)
board_image_url = "https://your-image-link.com"  # Βάλε εδώ το σωστό URL της εικόνας

st.image(board_image_url, use_column_width=True)

# 🔹 Διαδρομές (σαν τα τετράγωνα της Monopoly)
routes = ["Πολικός Αστέρας", "Φεγγάρι", "Ναυτίλος", "Φάρος", "Άνεμος", "Καταιγίδα", "Λιμάνι"]

# 🎮 Κατάσταση Παιχνιδιού
st.sidebar.title("⚓ Πλοία & Παίκτες")
players = {
    "Παίκτης 1": {"money": 1000000, "position": 0, "ships": 1},
    "Παίκτης 2": {"money": 900000, "position": 0, "ships": 1},
}

# 🔄 Button για Ζάρι
if st.sidebar.button("🎲 Ρίξε το Ζάρι!"):
    for player in players:
        roll = np.random.randint(1, 7)
        players[player]["position"] = (players[player]["position"] + roll) % len(routes)
        st.sidebar.write(f"🎯 **{player}** προχώρησε {roll} θέσεις -> **{routes[players[player]['position']]}**")

# 📍 Εμφάνιση του Πίνακα Παικτών
st.sidebar.markdown("### 📜 Κατάσταση Παικτών")
for player, data in players.items():
    st.sidebar.write(f"🛳️ **{player}** | 📍 Θέση: {routes[data['position']]} | 💰 Χρήματα: {data['money']}€")

# 🚀 Προσομοίωση κίνησης των πλοίων πάνω στο ταμπλό
st.subheader("🔄 Τα πλοία κινούνται...")
board_positions = np.zeros(len(routes))

for player, data in players.items():
    board_positions[data["position"]] += 1

# 🗺️ Χάρτης παιχνιδιού
for i, route in enumerate(routes):
    if board_positions[i] > 0:
        st.write(f"📍 **{route}** - {int(board_positions[i])} πλοία εδώ!")

st.markdown("---")
