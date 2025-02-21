import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time

# ----------------- ΡΥΘΜΙΣΕΙΣ ΕΦΑΡΜΟΓΗΣ -----------------
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Ναυτιλίας", layout="wide")

# ----------------- ΤΙΤΛΟΣ -----------------
st.markdown("<h1 style='text-align: center; color: navy;'>🚢 AdOnBoard - Επιτραπέζιο Ναυτιλίας 🎲</h1>", unsafe_allow_html=True)

# ----------------- ΟΡΙΣΜΟΣ ΠΑΙΚΤΩΝ -----------------
num_players = st.sidebar.slider("🔹 Πόσοι παίκτες θα παίξουν;", 1, 4, 2)

players = {f"Παίκτης {i+1}": {"θέση": 0, "χρήματα": 1000000} for i in range(num_players)}

# Ταμπλό (Λίστα τοποθεσιών)
board = ["Καταφύγιο", "Πολικός Αστέρας", "Φεγγάρι", "Ναύτιλος", "Φάρος", "Άνεμος"]

# ----------------- ΦΤΙΑΞΕ ΤΟ ΤΑΜΠΛΟ -----------------
def draw_board(players_positions):
    board_grid = np.zeros((1, len(board)))  # 1 γραμμή, Ν στήλες (για τις τοποθεσίες)

    for idx, player_pos in enumerate(players_positions):
        board_grid[0, player_pos] = idx + 1  # Βάζει τον αριθμό του παίκτη στη θέση του
    
    fig, ax = plt.subplots(figsize=(10, 2))
    sns.heatmap(board_grid, annot=board, fmt="", cmap="Blues", linewidths=0.5, cbar=False, xticklabels=False, yticklabels=False, ax=ax)
    plt.title("🌍 Θέσεις Παικτών στο Ταμπλό")
    st.pyplot(fig)

# ----------------- ΡΙΞΕ ΤΟ ΖΑΡΙ -----------------
def roll_dice():
    return random.randint(1, 6)

# ----------------- ΚΙΝΗΣΗ ΠΑΙΚΤΗ -----------------
def move_player(player):
    roll = roll_dice()
    st.write(f"🎲 Ο {player} έριξε **{roll}**!")
    time.sleep(1)
    
    new_position = (players[player]["θέση"] + roll) % len(board)  # Κυκλικό ταμπλό
    players[player]["θέση"] = new_position

    st.success(f"🚢 Ο {player} μετακινήθηκε στη θέση **{board[new_position]}**!")

# ----------------- ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ -----------------
if st.button("🎲 Ρίξε το Ζάρι!"):
    current_player = list(players.keys())[0]  # Ο πρώτος παίκτης παίζει
    move_player(current_player)
    
    # Εμφάνισε το ταμπλό με τις νέες θέσεις
    players_positions = [p["θέση"] for p in players.values()]
    draw_board(players_positions)
