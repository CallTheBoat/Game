import streamlit as st
import random
import time

# ✅ Ρύθμιση εμφάνισης
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Παιχνίδι", page_icon="⛵", layout="wide")

# ✅ Διαδρομές & Εικόνες
routes = {
    "Πολικός Αστέρας": "🌟",
    "Φεγγάρι": "🌙",
    "Ναυτίλος": "⚓",
    "Φάρος": "🏮",
    "Άνεμος": "🌬️"
}
event_cards = [
    "🌊 Κακοκαιρία! Χάνεις έναν γύρο.",
    "🎉 Χορηγία από τη Vodafone! Κερδίζεις 200000€.",
    "📡 Βλάβη στο GPS! Πληρώνεις 50000€.",
    "☀️ Καλός καιρός! Προχωράς 2 θέσεις μπροστά.",
    "🛥️ Ναύλωση VIP! Κερδίζεις 300000€."
]

# ✅ Κατάσταση παιχνιδιού
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False
if "players" not in st.session_state:
    st.session_state["players"] = 1
if "player_data" not in st.session_state:
    st.session_state["player_data"] = {}

# ✅ Συνάρτηση εμφάνισης πίνακα παιχνιδιού
def display_board():
    st.subheader("🎯 Πίνακας Παιχνιδιού")
    board = ["🔲"] * len(routes)

    for player, data in st.session_state["player_data"].items():
        pos = data["position"]
        board[pos] = f"🎭 {player[0]}"  # Εμφάνιση του αρχικού γράμματος κάθε παίκτη

    st.write(" ➡️ ".join(board))

# ✅ Συνάρτηση για να ξεκινήσει το παιχνίδι
def start_game():
    st.title("⛵ AdOnBoard: Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🎲")
    
    st.image("st.image("https://cdn.pixabay.com/photo/2017/1/23/22/5/sea-2006139_1280.jpg", use_container_width=True)

    st.session_state["players"] = st.number_input("Πόσοι παίκτες θα παίξουν; (1-4):", min_value=1, max_value=4, step=1)

    if st.button("🏁 Ξεκίνα το παιχνίδι!"):
        st.session_state["game_started"] = True
        st.session_state["player_data"] = {
            f"Παίκτης {i+1}": {"money": 1000000, "position": 0} for i in range(st.session_state["players"])
        }

# ✅ Συνάρτηση για το gameplay
def play_game():
    display_board()
    st.header("🎲 Ρίξτε το Ζάρι!")
    
    for player in st.session_state["player_data"]:
        st.subheader(f"{player} 🎮")
        if st.button(f"🎲 Ρίξε ζάρι ({player})"):
            roll = random.randint(1, 6)
            st.session_state["player_data"][player]["position"] = (st.session_state["player_data"][player]["position"] + roll) % len(routes)
            position_name = list(routes.keys())[st.session_state["player_data"][player]["position"]]
            st.success(f"{player} μετακινήθηκε στη διαδρομή: {routes[position_name]} **{position_name}**!")

            event = random.choice(event_cards)
            st.warning(f"🃏 Κάρτα συμβάντος: {event}")

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

            st.info(f"{player} τώρα έχει **{st.session_state['player_data'][player]['money']}€**.")

            time.sleep(1)

    display_board()

    if st.button("🏁 Τέλος παιχνιδιού"):
        st.session_state["game_started"] = False

# ✅ Έναρξη παιχνιδιού
if st.session_state["game_started"]:
    play_game()
else:
    start_game()
