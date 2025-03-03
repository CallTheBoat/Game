import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# --------------------------------------
# 1) Ορισμός "ταμπλό" (Squares) σε μορφή Monopoly
# --------------------------------------
# Κάθε "κουτάκι" έχει:
# - name (π.χ. νησί ή συμβάν)
# - coords (lat, lon)
# - event (κείμενο γεγονότος, αν υπάρχει)
board_squares = [
    {
        "name": "Santorini",
        "coords": (36.3932, 25.4615),
        "event": ""
    },
    {
        "name": "Choppy Seas",
        "coords": (36.50, 25.50),
        "event": "Choppy seas! Skip next turn!"
    },
    {
        "name": "Random Island #1",
        "coords": (36.70, 25.60),
        "event": ""
    },
    {
        "name": "Storm Area",
        "coords": (36.90, 25.70),
        "event": "Storm - lose 1 turn!"
    },
    {
        "name": "Mykonos",
        "coords": (37.4467, 25.3289),
        "event": ""
    },
]

# --------------------------------------
# 2) Αρχικές Ρυθμίσεις Streamlit
# --------------------------------------
st.set_page_config(page_title="Island Monopoly", layout="wide")
st.title("Island Monopoly Board Game")

st.markdown("""
Παράδειγμα επιτραπέζιου τύπου "Monopoly" πάνω σε χάρτη:
- Κάθε κουτάκι είναι νησί ή γεγονός.
- Με κάθε ρίψη ζαριού το πλοίο προχωράει αντίστοιχα.
- Αν "πέσεις" σε κουτάκι με event, εμφανίζεται μήνυμα.
""")

# --------------------------------------
# 3) Session State για το πλοίο
# --------------------------------------
# boat_index: σε ποιο κουτάκι βρισκόμαστε;
if "boat_index" not in st.session_state:
    st.session_state["boat_index"] = 0

# skip_turn: αν είναι True, δεν μπορείς να παίξεις αυτόν τον γύρο (π.χ. λόγω storm)
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False

# --------------------------------------
# 4) Προβολή του Ταμπλό (Χάρτης)
# --------------------------------------
# Τοποθετούμε markers για ΟΛΑ τα squares
# και ξεχωριστό marker για το πλοίο.
start_coords = board_squares[0]["coords"]
m = folium.Map(location=start_coords, zoom_start=7)

# Προσθήκη markers για όλα τα νησιά/κουτάκια:
for i, square in enumerate(board_squares):
    folium.Marker(
        square["coords"],
        tooltip=f"{i}. {square['name']}",
        popup=square["event"] if square["event"] else f"{square['name']} (No event)"
    ).add_to(m)

# Marker για τη ΘΕΣΗ του πλοίου
boat_square = board_squares[st.session_state["boat_index"]]
boat_coords = boat_square["coords"]
folium.Marker(
    boat_coords,
    icon=folium.Icon(color="blue", icon="ship", prefix='fa'),
    tooltip="Boat Position",
    popup=f"Current: {boat_square['name']}"
).add_to(m)

# Εμφάνιση Χάρτη
st_folium(m, width=800, height=500)

# --------------------------------------
# 5) Κουμπί Roll the Dice
# --------------------------------------
st.markdown("---")
if st.button("Roll the Dice"):
    if st.session_state["skip_turn"]:
        # Αν πρέπει να παρακάμψουμε αυτόν τον γύρο
        st.warning("You must skip this turn due to a previous event!")
        st.session_state["skip_turn"] = False  # Ακυρώνουμε το skip για επόμενο γύρο
    else:
        dice = random.randint(1, 6)
        st.success(f"You rolled: {dice}")
        # Μετακίνηση του πλοίου
        new_index = st.session_state["boat_index"] + dice
        # Αν ξεπεράσουμε το τελευταίο κουτάκι, παραμένουμε στο τέλος
        if new_index >= len(board_squares):
            new_index = len(board_squares) - 1

        st.session_state["boat_index"] = new_index
        current_square = board_squares[new_index]

        # Ελέγχουμε αν υπάρχει event
        if current_square["event"]:
            st.info(f"Event: {current_square['event']}")
            # Αν το event είναι "skip turn" ή "lose turn", μπορείς να βάλεις λογική εδώ:
            if "skip" in current_square["event"].lower() or "lose" in current_square["event"].lower():
                st.session_state["skip_turn"] = True

# --------------------------------------
# 6) Εμφάνιση Πληροφορίας
# --------------------------------------
current_sq = board_squares[st.session_state["boat_index"]]
st.write(f"**Boat is now at**: {current_sq['name']}")
if current_sq["event"]:
    st.write(f"**Square Event**: {current_sq['event']}")
else:
    st.write("No special event here.")
