import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# ---------- Enhanced Interactive Board Game Simulation ----------
def enhanced_board_game():
    st.subheader("Interactive Maritime Board Game")

    # Ορισμός μεγέθους κουτιών (squares) και χρωματικής παλέτας
    BOX_SIZE = 0.03  # Για πιο εντυπωσιακή απεικόνιση
    box_colors = ['#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f', '#ffb703']
    
    # Ορισμός board squares: 10 κουτάκια με διάφορα events και επιλογές ρόλων
    board_squares = [
        {"name": "Santorini", "coords": (36.3932, 25.4615), "event": "Start"},
        {"name": "Calm Waters", "coords": (36.50, 25.55), "event": "Nothing happens."},
        {"name": "Mykonos", "coords": (37.4467, 25.3289), "event": "Option: Become Ship Owner"},
        {"name": "Choppy Seas", "coords": (36.70, 25.60), "event": "Waves! Lose a turn."},
        {"name": "Rhodes", "coords": (36.4349, 28.2176), "event": "Option: Become Sponsor"},
        {"name": "Stormy Waters", "coords": (36.80, 27.10), "event": "Severe storm! Skip turn."},
        {"name": "Mystery Island", "coords": (36.90, 27.50), "event": "Find treasure! Advance 1 square."},
        {"name": "Calm Harbor", "coords": (37.00, 27.80), "event": "Rest and recover."},
        {"name": "Crete", "coords": (35.2401, 24.8093), "event": "Option: Become Ship Owner"},
        {"name": "Port", "coords": (35.50, 25.00), "event": "Finish – No event."}
    ]
    
    # Αρχικοποίηση session state αν δεν υπάρχουν ήδη
    if "boat_index_board" not in st.session_state:
        st.session_state["boat_index_board"] = 0
    if "skip_turn_board" not in st.session_state:
        st.session_state["skip_turn_board"] = False
    if "current_role" not in st.session_state:
        st.session_state["current_role"] = "Passenger"

    st.markdown(f"**Current Role:** {st.session_state['current_role']}")
    st.markdown(f"**Current Square:** {board_squares[st.session_state['boat_index_board']]['name']}")
    
    # Δημιουργία χάρτη: Κέντρο στο πρώτο κουτάκι
    center_coords = board_squares[0]["coords"]
    m = folium.Map(location=center_coords, zoom_start=6, tiles="cartodbpositron")
    
    # Σχεδίαση κάθε κουτιού ως ορθογώνιο με όμορφα χρώματα και custom popup
    for i, square in enumerate(board_squares):
        lat, lon = square["coords"]
        bounds = [(lat - BOX_SIZE, lon - BOX_SIZE), (lat + BOX_SIZE, lon + BOX_SIZE)]
        color = box_colors[i % len(box_colors)]
        popup_html = f"""
        <div style="font-family: Arial; font-size: 14px; text-align: center">
            <strong>{square['name']}</strong><br>
            <em>{square['event']}</em>
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
        # Προσθήκη ονόματος στο κέντρο του κουτιού
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
    
    # Ρίψη ζαριού & μετακίνηση του πλοίου
    if st.button("Roll the Dice (Board Game)"):
        if st.session_state["skip_turn_board"]:
            st.warning("You must skip this turn due to a previous event!")
            st.session_state["skip_turn_board"] = False
        else:
            dice = random.randint(1, 6)
            st.success(f"You rolled: {dice}")
            new_index = st.session_state["boat_index_board"] + dice
            if new_index >= len(board_squares):
                new_index = len(board_squares) - 1  # Μένουμε στο τελευταίο κουτάκι
            st.session_state["boat_index_board"] = new_index
            current_square = board_squares[new_index]
            st.info(f"Boat landed on: {current_square['name']}")
            
            # Ελέγχουμε events και δίνουμε επιλογές αλλαγής ρόλου αν υπάρχουν
            event_text = current_square["event"].lower()
            if "lose" in event_text or "skip" in event_text or "storm" in event_text:
                st.info("Event: You lose your turn!")
                st.session_state["skip_turn_board"] = True
            if "advance" in event_text:
                st.success("Bonus: Advance 1 square!")
                st.session_state["boat_index_board"] = min(new_index + 1, len(board_squares) - 1)
            # Δυνατότητα αλλαγής ρόλου στα συγκεκριμένα κουτάκια
            if "become ship owner" in event_text:
                if st.button("Become Ship Owner", key=f"owner_{new_index}"):
                    st.session_state["current_role"] = "Ship Owner"
                    st.success("Role changed: You are now a Ship Owner!")
            if "become sponsor" in event_text:
                if st.button("Become Sponsor", key=f"sponsor_{new_index}"):
                    st.session_state["current_role"] = "Sponsor"
                    st.success("Role changed: You are now a Sponsor!")
                    
        current_sq = board_squares[st.session_state["boat_index_board"]]
        st.write(f"**Boat is now at:** {current_sq['name']}")
        st.write(f"**Event:** {current_sq['event']}")
    
    # Εάν ο τρέχων ρόλος είναι Sponsor, εμφάνισε Advertising Dashboard
    if st.session_state["current_role"] == "Sponsor":
        st.markdown("### Advertising Dashboard")
        reach = random.randint(5000, 50000)
        st.metric("Potential Engagement", f"{reach} impressions")
        st.write("Select a Passenger for Sponsored Content:")
        passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
        selected_passenger = st.selectbox("Select a Passenger:", passengers, key="dashboard_passenger")
        engagement = random.randint(1000, 10000)
        st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

# ---------- Main App ----------
st.set_page_config(page_title="Interactive Maritime Board Game", layout="wide")
st.title("Interactive Maritime Board Game Dashboard")

# Στην αρχή όλοι ξεκινούν ως Passenger. Μετά τα events μπορούν να αλλάξουν ρόλο.
st.session_state["current_role"] = st.selectbox("Select Your Starting Role:", 
                                                  ["Passenger", "Ship Owner", "Sponsor"],
                                                  index=0, key="starting_role")
st.markdown("**Note:** You start with the selected role, but you may change roles at specific board squares.")

enhanced_board_game()
