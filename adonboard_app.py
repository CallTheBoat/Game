import streamlit as st
import numpy as np
import time

# 🎯 Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="AdOnBoard - Ναυτιλιακό Επιτραπέζιο", layout="wide")

# 🏝️ Εικόνα Ταμπλό (ανέβασε τη σωστή εικόνα σου ή χρησιμοποίησε placeholder)
board_image_url = "https://your-image-link.com"  # Βάλε εδώ το URL της εικόνας

# 📜 Διαδρομές του παιχνιδιού (σαν κελιά Monopoly)
routes = ["🏝 Πολικός Αστέρας", "🌙 Φεγγάρι", "⚓ Ναυτίλος", "🚢 Φάρος", "🌊 Άνεμος", "⛈ Καταιγίδα", "🏠 Λιμάνι"]

# 🎮 Κατάσταση Παιχνιδιού
st.sidebar.title("⚓ Πλοία & Παίκτες")
players = {
    "Παίκτης 1": {"money": 1000000, "position": 0, "icon": "⛵"},
    "Παίκτης 2": {"money": 900000, "position": 0, "icon": "🚤"},
}

# 🔹 Φόρμα παιχνιδιού
st.title("🎲 AdOnBoard - Το Επιτραπέζιο Ναυτιλίας")

# 📍 Εμφάνιση του ταμπλό
st.image(board_image_url, use_column_width=True)

# 🔄 Button για Ζάρι
if st.sidebar.button("🎲 Ρίξε το Ζάρι!"):
    for player in players:
        roll = np.random.randint(1, 7)
        old_position = players[player]["position"]
        players[player]["position"] = (players[player]["position"] + roll) % len(routes)

        # 🎥 Animation για τη μετακίνηση του πλοίου
        for step in range(old_position, players[player]["position"] + 1):
            st.write(f"⏳ {player} κινείται στο **{routes[step % len(routes)]}** {players[player]['icon']}")
            time.sleep(0.5)
            st.experimental_rerun()

# 📊 Κατάσταση Παικτών
st.sidebar.markdown("### 📜 Κατάσταση Παικτών")
for player, data in players.items():
    st.sidebar.write(f"{data['icon']} **{player}** | 📍 Θέση: {routes[data['position']]} | 💰 {data['money']}€")

# 🛳️ Αναπαράσταση του ταμπλό με emoji
st.subheader("📍 Θέσεις Παικτών στο Ταμπλό")
board_state = ["⬜"] * len(routes)

for player, data in players.items():
    board_state[data["position"]] = data["icon"]

st.write(" | ".join(board_state))
