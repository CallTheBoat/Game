import streamlit as st
import random
import folium
from streamlit_folium import st_folium

def board_game_simulation():
    st.subheader("Enhanced Board Game Simulation")
    
    # Ορισμός μεγέθους κουτιών και χρωματικής παλέτας
    BOX_SIZE = 0.03  # Λίγο μεγαλύτερο για πιο εντυπωσιακή απεικόνιση
    box_colors = ['#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f', '#ffb703']
    
    # Ορισμός board squares: 6 κουτάκια με τρία νησιά (στην 0, 2 και 4) και ενδιάμεσα event squares
    board_squares = [
        {"name": "Santorini", "coords": (36.3932, 25.4615), "event": ""},
        {"name": "Calm Waters", "coords": (36.65, 26.2), "event": "Nothing happens."},
        {"name": "Mykonos", "coords": (37.4467, 25.3289), "event": "Option: Become Ship Owner"},
        {"name": "Stormy Seas", "coords": (37.0, 26.5), "event": "Lose a turn."},
        {"name": "Rhodes", "coords": (36.4349, 28.2176), "event": "Option: Become Sponsor"},
        {"name": "Harbor", "coords": (36.80, 27.0), "event": "Bonus: Advance 1 square"}
    ]
    
    # Αρχικοποίηση session state για το παιχνίδι αν δεν υπάρχουν ήδη
    if "boat_index_board" not in st.session_state:
        st.session_state["boat_index_board"] = 0
    if "skip_turn_board" not in st.session_state:
        st.session_state["skip_turn_board"] = False
    if "current_role" not in st.session_state:
        st.session_state["current_role"] = "Passenger"
    
    st.write(f"**Current Role:** {st.session_state['current_role']}")
    
    # Δημιουργία χάρτη με κεντρική τοποθέτηση στο πρώτο κουτάκι
    center_coords = board_squares[0]["coords"]
    m = folium.Map(location=center_coords, zoom_start=7, tiles="cartodbpositron")
    
    # Σχεδίαση κάθε κουτιού ως ορθογώνιο με όμορφα χρώματα και custom popup HTML
    for i, square in enumerate(board_squares):
        lat, lon = square["coords"]
        bounds = [(lat - BOX_SIZE, lon - BOX_SIZE), (lat + BOX_SIZE, lon + BOX_SIZE)]
        color = box_colors[i % len(box_colors)]
        popup_html = f"""
        <div style="font-family: Arial; font-size: 14px; text-align: center">
            <strong>{square['name']}</strong><br>
            <em>{square['event'] if square['event'] else "No event"}</em>
        </div>
        """
        folium.Rectangle(
            bounds=bounds,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.4,
            weight=2,
            tooltip=f"{i}. {square['name']}",
            popup=folium.Popup(popup_html, max_width=200)
        ).add_to(m)
        # Εμφάνιση ονόματος στο κέντρο του κουτιού με DivIcon
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f"""<div style="font-size: 13pt; color: #1d3557; font-weight: bold">{square['name']}</div>"""
            )
        ).add_to(m)
    
    # Marker για τη θέση του πλοίου
    current_square = board_squares[st.session_state["boat_index_board"]]
    folium.Marker(
        current_square["coords"],
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip=f"Boat is here: {current_square['name']}"
    ).add_to(m)
    
    st_folium(m, width=800, height=500)
    
    # Ρίψη ζαριού και μετακίνηση
    if st.button("Roll the Dice (Board Game)"):
        if st.session_state["skip_turn_board"]:
            st.warning("You must skip this turn due to a previous event!")
            st.session_state["skip_turn_board"] = False
        else:
            dice = random.randint(1, 6)
            st.success(f"You rolled: {dice}")
            new_index = st.session_state["boat_index_board"] + dice
            if new_index >= len(board_squares):
                new_index = len(board_squares) - 1  # παραμένουμε στο τελευταίο κουτάκι
            st.session_state["boat_index_board"] = new_index
            current_square = board_squares[new_index]
            st.info(f"Boat landed on: {current_square['name']}")
            
            if current_square["event"]:
                st.info(f"Event: {current_square['event']}")
                # Αν το event είναι "Lose a turn", ορίζουμε skip turn
                if "lose" in current_square["event"].lower():
                    st.session_state["skip_turn_board"] = True
                # Αν υπάρχει bonus "Advance", προχωράμε επιπλέον 1 κουτάκι
                if "advance" in current_square["event"].lower():
                    st.session_state["boat_index_board"] = min(new_index + 1, len(board_squares) - 1)
                    st.success("Bonus: Advance 1 square!")
                # Εάν το event δίνει επιλογή αλλαγής ρόλου:
                if "become ship owner" in current_square["event"].lower():
                    if st.button("Become Ship Owner", key="ship_owner"):
                        st.session_state["current_role"] = "Ship Owner"
                        st.success("You are now a Ship Owner!")
                if "become sponsor" in current_square["event"].lower():
                    if st.button("Become Sponsor", key="sponsor"):
                        st.session_state["current_role"] = "Sponsor"
                        st.success("You are now a Sponsor!")
                        
        current_sq = board_squares[st.session_state["boat_index_board"]]
        st.write(f"**Boat is now at:** {current_sq['name']}")
        if current_sq["event"]:
            st.write(f"**Square Event:** {current_sq['event']}")
        else:
            st.write("No special event here.")

# ---------- Main App ----------
st.set_page_config(page_title="Maritime Board Game Dashboard", layout="wide")
st.title("Maritime Board Game Dashboard")

# Εκκίνηση του enhanced board game
board_game_simulation()
