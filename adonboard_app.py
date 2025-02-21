import streamlit as st
import numpy as np
import time

# 🎯 Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="AdOnBoard - Ναυτιλιακό Επιτραπέζιο", layout="wide")

# 📜 Διαδρομές του παιχνιδιού
routes = ["🏝 Πολικός Αστέρας", "🌙 Φεγγάρι", "⚓ Ναυτίλος", "🚢 Φάρος", "🌊 Άνεμος", "⛈ Καταιγίδα", "🏠 Λιμάνι"]

# 🔹 Διατήρηση κατάστασης μέσω session_state
if "players" not in st.session_state:
    st.session_state.players = {
        "Παίκτης 1": {"money": 1000000, "position": 0, "icon": "⛵"},
        "Παίκτης 2": {"money": 900000, "position": 0, "icon": "🚤"},
    }

# 🎮 Πάνελ παιχνιδιού
st.sidebar.title("⚓ Πλοία & Παίκτες")
st.title("🎲 AdOnBoard - Το Επιτραπέζιο Ναυτιλίας")

# 🔄 Button για Ζάρι
if st.sidebar.button("🎲 Ρίξε το Ζάρι!"):
    for player in st.session_state.players:
        roll = np.random.randint(1, 7)
        old_position = st.session_state.players[player]["position"]
        st.session_state.players[player]["position"] = (old_position + roll) % len(routes)

# 📊 Κατάσταση Παικτών
st.sidebar.markdown("### 📜 Κατάσταση Παικτών")
for player, data in st.session_state.players.items():
    st.sidebar.write(f"{data['icon']} **{player}** | 📍 Θέση: {routes[data['position']]} | 💰 {data['money']}€")

# 🛳️ Αναπαράσταση του ταμπλό με emoji
st.subheader("📍 Θέσεις Παικτών στο Ταμπλό")
board_state = ["⬜"] * len(routes)

for player, data in st.session_state.players.items():
    board_state[data["position"]] = data["icon"]

st.write(" | ".join(board_state))
