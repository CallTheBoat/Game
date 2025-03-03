import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# ---------- Enhanced Board Game Simulation ----------
def enhanced_board_game():
    st.subheader("Enhanced Board Game Simulation")
    
    # Ορισμός μεγέθους κουτιών και χρωματικής παλέτας
    BOX_SIZE = 0.03  # ελαφρώς μεγαλύτερο για πιο εντυπωσιακή απεικόνιση
    box_colors = ['#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f']
    
    # Ορισμός board squares: κάθε κουτάκι έχει όνομα, κέντρο (coords) και event
    board_squares = [
        {"name": "Santorini", "coords": (36.3932, 25.4615), "event": ""},
        {"name": "Calm Waters", "coords": (36.50, 25.50), "event": "Smooth sailing."},
        {"name": "Choppy Seas", "coords": (36.60, 25.55), "event": "Waves ahead! Lose a turn."},
        {"name": "Mystery Island", "coords": (36.70, 25.60), "event": "Discover treasure! Advance 1 square."},
        {"name": "Storm Area", "coords": (36.80, 25.65), "event": "Severe storm! Skip next turn."},
        {"name": "Mykonos", "coords": (37.4467, 25.3289), "event": ""}
    ]
    
    # Αρχικοποίηση session state για το παιχνίδι, εάν δεν υπάρχουν ήδη
    if "boat_index_board" not in st.session_state:
        st.session_state["boat_index_board"] = 0
    if "skip_turn_board" not in st.session_state:
        st.session_state["skip_turn_board"] = False

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
    
    # Λογική ρίψης ζαριού και μετακίνησης
    if st.button("Roll the Dice (Enhanced Board)"):
        if st.session_state["skip_turn_board"]:
            st.warning("You must skip this turn due to a previous event!")
            st.session_state["skip_turn_board"] = False
        else:
            dice = random.randint(1, 6)
            st.success(f"You rolled: {dice}")
            new_index = st.session_state["boat_index_board"] + dice
            if new_index >= len(board_squares):
                new_index = len(board_squares) - 1  # μένουμε στο τελευταίο κουτάκι
            st.session_state["boat_index_board"] = new_index
            current_square = board_squares[new_index]
            st.info(f"Boat landed on: {current_square['name']}")
            if current_square["event"]:
                st.info(f"Event: {current_square['event']}")
                # Λογική για γεγονότα: αν περιέχει "lose" ή "skip", παραλείπει γύρο
                if "lose" in current_square["event"].lower() or "skip" in current_square["event"].lower():
                    st.session_state["skip_turn_board"] = True
                # Εάν υπάρχει bonus (π.χ. "advance"), μετακινούμε επιπλέον 1 κουτάκι
                if "advance" in current_square["event"].lower():
                    st.session_state["boat_index_board"] = min(new_index + 1, len(board_squares) - 1)
                    st.success("Bonus: Advance 1 square!")
        current_sq = board_squares[st.session_state["boat_index_board"]]
        st.write(f"**Boat is now at**: {current_sq['name']}")
        if current_sq["event"]:
            st.write(f"**Square Event**: {current_sq['event']}")
        else:
            st.write("No special event here.")
    
    # Επιλογή ρόλου Sponsor: Εμφάνιση Advertising Dashboard
    if st.session_state.get("role") == "Sponsor":
        st.markdown("### Advertising Dashboard")
        reach = random.randint(5000, 50000)
        st.metric("Potential Engagement", f"{reach} impressions")
        st.write("Select a Passenger for Sponsored Content:")
        passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
        selected_passenger = st.selectbox("Select a Passenger:", passengers, key="nice_board_passenger")
        engagement = random.randint(1000, 10000)
        st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

# ---------- Main App ----------
st.set_page_config(page_title="Enhanced Maritime Board Game", layout="wide")
st.title("Enhanced Maritime Board Game")

# Επιλογή ρόλου
st.session_state["role"] = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])
if st.session_state["role"] == "Passenger":
    st.info("As a Passenger, enjoy the journey!")
elif st.session_state["role"] == "Ship Owner":
    st.info("As a Ship Owner, manage your routes and profits!")
elif st.session_state["role"] == "Sponsor":
    st.info("As a Sponsor, boost your brand with our advertising dashboard!")

# Εμφάνιση της Enhanced Board Game Simulation
enhanced_board_game()
