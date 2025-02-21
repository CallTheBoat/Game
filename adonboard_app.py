import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# ----------------- ΡΥΘΜΙΣΕΙΣ ΕΦΑΡΜΟΓΗΣ -----------------
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Ναυτιλίας", layout="wide")

# ----------------- ΤΙΤΛΟΣ -----------------
st.markdown("""
    <h1 style='text-align: center; color: navy;'>🚢 AdOnBoard - Επιτραπέζιο Ναυτιλίας 🎲</h1>
    <h3 style='text-align: center;'>Χάρτης Ναυτιλίας - Προορισμοί και Διαδρομές</h3>
    """, unsafe_allow_html=True)

# ----------------- ΟΡΙΣΜΟΣ ΠΑΙΚΤΩΝ -----------------
num_players = st.sidebar.slider("🔹 Πόσοι παίκτες θα παίξουν;", 1, 4, 2)
players = {f"Παίκτης {i+1}": {"θέση": 0, "χρήματα": 1000000} for i in range(num_players)}

# Ταμπλό (κυκλικές τοποθεσίες)
board = ["Πειραιάς", "Σύρος", "Μύκονος", "Νάξος", "Σαντορίνη", "Ηράκλειο", "Ρόδος", "Κως", "Λέσβος", "Θεσσαλονίκη", "Βόλος", "Πάτρα"]

# Συντεταγμένες κυκλικής διαδρομής
angle = np.linspace(0, 2*np.pi, len(board), endpoint=False)
positions = np.array([np.cos(angle), np.sin(angle)]).T * 10  # Κυκλική πορεία

# ----------------- ΦΤΙΑΞΕ ΤΟ ΤΑΜΠΛΟ -----------------
def draw_board(players_positions):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    
    # Ζωγραφίζουμε τον κυκλικό πίνακα
    for i, location in enumerate(board):
        ax.add_patch(plt.Circle((positions[i, 0], positions[i, 1]), 1, fill=True, color="lightblue", edgecolor="black"))
        ax.text(positions[i, 0], positions[i, 1], location, ha="center", va="center", fontsize=10, fontweight="bold")
    
    # Ζωγραφίζουμε τα πλοία
    for i, player_pos in enumerate(players_positions):
        ax.text(positions[player_pos, 0], positions[player_pos, 1] + 0.8, f"🚢 {i+1}", ha="center", va="center", fontsize=14, color="red")
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    st.pyplot(fig)

# ----------------- ΡΙΞΕ ΤΟ ΖΑΡΙ -----------------
def roll_dice():
    return random.randint(1, 6)

# ----------------- ΚΙΝΗΣΗ ΠΑΙΚΤΗ -----------------
def move_player(player):
    roll = roll_dice()
    st.write(f"🎲 Ο {player} έριξε **{roll}**!")
    time.sleep(1)
    
    new_position = (players[player]["θέση"] + roll) % len(board)
    players[player]["θέση"] = new_position
    
    st.success(f"🚢 Ο {player} μετακινήθηκε στη θέση **{board[new_position]}**!")

# ----------------- ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ -----------------
if st.button("🎲 Ρίξε το Ζάρι!"):
    current_player = list(players.keys())[0]
    move_player(current_player)
    players_positions = [p["θέση"] for p in players.values()]
    draw_board(players_positions)
