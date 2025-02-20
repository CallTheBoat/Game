import streamlit as st
import random

def start_game():
    st.title("🚀 AdOnBoard: Το Επιτραπέζιο Παιχνίδι Ναυτιλίας 🎲")
    
    players = st.number_input("Πόσοι παίκτες θα παίξουν; (1-4):", min_value=1, max_value=4, step=1)
    start = st.button("Ξεκίνα το παιχνίδι!")

    if start:
        play_game(players)

def play_game(players):
    routes = ["Πολικός Αστέρας", "Φεγγάρι", "Ναυτίλος", "Φάρος", "Άνεμος"]
    event_cards = [
        "Κακοκαιρία! Χάνεις έναν γύρο.",
        "Χορηγία από τη Vodafone! Κερδίζεις 200.000€.",
        "Βλάβη στο GPS! Πληρώνεις 50.000€.",
        "Καλός καιρός! Προχωράς 2 θέσεις μπροστά.",
        "Ναύλωση VIP! Κερδίζεις 300.000€."
    ]
    
    player_data = {}
    for i in range(1, players + 1):
        player_data[f"Παίκτης {i}"] = {"money": 1000000, "position": 0}

    game_over = False
    while not game_over:
        for player in player_data:
            st.write(f"\n### {player}, ρίξε το ζάρι... 🎲")
            roll = random.randint(1, 6)
            player_data[player]["position"] = (player_data[player]["position"] + roll) % len(routes)
            st.write(f"{player} μετακινήθηκε στη διαδρομή: {routes[player_data[player]['position']]}!")

            event = random.choice(event_cards)
            st.write(f"🃏 Κάρτα συμβάντος: {event}")

            if "Κερδίζεις" in event:
                amount = int(event.split()[2].replace("€.", ""))
                player_data[player]["money"] += amount
            elif "Πληρώνεις" in event:
                amount = int(event.split()[2].replace("€.", ""))
                player_data[player]["money"] -= amount

            st.write(f"{player} τώρα έχει **{player_data[player]['money']}€**.")
        
        if st.button("Επόμενος γύρος ή τέλος παιχνιδιού;"):
            game_over = True

    st.write("\n## 🎉 Τέλος παιχνιδιού! Δείτε τα αποτελέσματα:")
    for player in player_data:
        st.write(f"{player}: {player_data[player]['money']}€")

if __name__ == "__main__":
    start_game()
