import streamlit as st
import random

# Αρχικοποίηση session state
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False
if "players" not in st.session_state:
    st.session_state["players"] = 1
if "player_data" not in st.session_state:
    st.session_state["player_data"] = {}

def start_game():
    st.title("🚀 AdOnBoard: Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🎲")

    st.session_state["players"] = st.number_input("Πόσοι παίκτες θα παίξουν; (1-4):", min_value=1, max_value=4, step=1)

    if st.button("Ξεκίνα το παιχνίδι!"):
        st.session_state["game_started"] = True
        st.session_state["player_data"] = {f"Παίκτης {i+1}": {"money": 1000000, "position": 0} for i in range(st.session_state["players"])}

def extract_amount(event_text):
    """ Εξάγει το ποσό από την κάρτα συμβάντος με ασφαλή τρόπο. """
    words = event_text.split()
    for word in words:
        try:
            return int(word.replace("€", "").replace(".", "").replace(",", ""))
        except ValueError:
            continue
