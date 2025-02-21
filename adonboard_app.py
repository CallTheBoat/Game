import streamlit as st
import random

# ✅ Αρχικοποίηση της εφαρμογής
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Παιχνίδι", page_icon="🎲")

# ✅ Κατάσταση παιχνιδιού (session state)
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False
if "players" not in st.session_state:
    st.session_state["players"] = 1
if "player_data" not in st.session_state:
    st.session_state["player_data"] = {}

# ✅ Διαδρομές και κάρτες συμβάντων
routes = ["Πολικός Αστέρας", "Φεγγάρι", "Ναυτίλος", "Φάρος", "Άνεμος"]
event_cards = [
    "Κακοκαιρία! Χάνεις έναν γύρο.",
    "Χορηγία από τη Vodafone! Κερδίζεις 200000€.",
    "Βλάβη στο GPS! Πληρώνεις 50000€.",
    "Καλός καιρός! Προχωράς 2 θέσεις μπροστά.",
    "Ναύλωση VIP! Κερδίζεις 300000€."
]

# ✅ Συνάρτηση για να ξεκινήσει το παιχνίδι
def start_game():
    st.title("🚀 AdOnBoard: Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🎲")

    st.session_state["players"] = st.number_input("Πόσοι παίκτες θα παίξουν; (1-4):", min_value=1, max_value=4, step=1)

    if st.button("Ξεκίνα το παιχνίδι!"):
        st.session_state["game_started"] = True
        st.session_state["player_data"] = {f"Παίκτης {i+1}": {"money": 1000000, "position": 0} for i in range(st.session_state["players"])}

# ✅ Συνάρτηση για να παίξει ο κάθε παίκτης
def play_game():
    for player in st.session_state["player_data"]:
        st.write(f"### {player}, ρίξε το ζάρι... 🎲")

        if st.button(f"🎲 Ρίξε ζάρι ({player})"):
            roll = random.randint(1, 6)
            st.session_state["player_data"][player]["position"] = (st.session_state["player_data"][player]["position"] + roll) % len(routes)
            st.write(f"{player} μετακινήθηκε στη διαδρομή: **{routes[st.session_state['player_data'][player]['position']]}**!")

            event = random.choice(event_cards)
            st.write(f"🃏 Κάρτα συμβάντος: {event}")

            # ✅ Εξαγωγή ποσού από την κάρτα συμβάντος
            words = event.split()
            amount = 0
            for word in words:
                if "€" in word:
                    amount = int(word.replace("€", "").replace(".", "").replace(",", ""))
                    break
            
            if "Κερδίζεις" in event:
                st.session_state["player_data"][player]["money"] += amount
            elif "Πληρώνεις" in event:
                st.session_state["player_data"][player]["money"] -= amount

            st.write(f"{player} τώρα έχει **{st.session_state['player_data'][player]['money']}€**.")

    if st.button("🏁 Τέλος παιχνιδιού"):
        st.session_state["game_started"] = False

# ✅ Εκκίνηση παιχνιδιού ή συνέχεια
if st.session_state["game_started"]:
    play_game()
else:
    start_game()
