import streamlit as st
import random

# Ρυθμίσεις Στυλ
st.markdown(
    """
    <style>
        body {background-color: #0E1C36; color: white;}
        .big-font {font-size: 24px !important; font-weight: bold; color: #FFDD57;}
        .game-board {display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;}
        .tile {width: 80px; height: 80px; background-color: #1F4068; color: white; display: flex; align-items: center; justify-content: center; font-size: 18px; border-radius: 10px; border: 2px solid #FFDD57;}
        .player-icon {color: #FF5733; font-size: 22px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-font">🎲 AdOnBoard: Το Επιτραπέζιο Ναυτιλίας</p>', unsafe_allow_html=True)

# Ταμπλό Παιχνιδιού
routes = ["⚓ Καταφύγιο", "🌊 Πολικός Αστέρας", "🚢 Φεγγάρι", "⚓ Ναυτίλος", "🛳️ Φάρος", "🌬️ Άνεμος"]
players = st.session_state.get("players", {})
num_players = st.number_input("Πόσοι παίκτες θα παίξουν; (1-4)", min_value=1, max_value=4, value=1, step=1)

if st.button("🔄 Έναρξη Παιχνιδιού"):
    players.clear()
    for i in range(1, num_players + 1):
        players[f"Παίκτης {i}"] = {"position": 0, "money": 1000000}
    st.session_state.players = players

if players:
    st.markdown("### 📍 Θέσεις Παικτών στο Ταμπλό")
    
    # Εμφάνιση Ταμπλό
    board_html = "<div class='game-board'>"
    for i, place in enumerate(routes):
        occupied = [p for p in players if players[p]["position"] == i]
        board_html += f"<div class='tile'>{place}<br>{' '.join(occupied)}</div>"
    board_html += "</div>"
    st.markdown(board_html, unsafe_allow_html=True)
    
    # Ρίψη Ζαριού
    for player in players:
        if st.button(f"🎲 Ρίξε το Ζάρι ({player})"):
            roll = random.randint(1, 6)
            players[player]["position"] = (players[player]["position"] + roll) % len(routes)
            st.session_state.players = players
            st.experimental_rerun()
    
    # Κατάσταση Παικτών
    st.markdown("### 📜 Κατάσταση Παικτών")
    for player, data in players.items():
        st.markdown(f"**{player}** - Θέση: {routes[data['position']]} | 💰 Χρήματα: {data['money']}€")
