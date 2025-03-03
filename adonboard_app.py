import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# ------------------------------
# 1) Ορισμός "ταμπλό" (board squares)
# ------------------------------
# Κάθε κουτάκι έχει:
# - name: το όνομα (π.χ. όνομα νησιού ή γεγονός)
# - coords: το κέντρο του κουτιού (lat, lon)
# - event: (προαιρετικά) μήνυμα όταν σταματάς σε αυτό
# Θα σχεδιάσουμε κάθε κουτάκι ως ορθογώνιο με ακτίνα 0.02 βαθμών
BOX_SIZE = 0.02

board_squares = [
    {
        "name": "Santorini",
        "coords": (36.3932, 25.4615),
        "event": ""
    },
    {
        "name": "Choppy Seas",
        "coords": (36.50, 25.50),
        "event": "Choppy seas! Stay here for one turn."
    },
    {
        "name": "Mystery Island",
        "coords": (36.70, 25.60),
        "event": ""
    },
    {
        "name": "Storm Area",
        "coords": (36.90, 25.70),
        "event": "Storm - delay! Lose 1 turn."
    },
    {
        "name": "Mykonos",
        "coords": (37.4467, 25.3289),
        "event": ""
    },
]

# ------------------------------
# 2) Ρυθμίσεις Streamlit
# ------------------------------
st.set_page_config(page_title="Island Board Game", layout="wide")
st.title("Island Board Game")

st.markdown("""
Αυτό το app προσομοιώνει ένα επιτραπέζιο παιχνίδι πάνω σε χάρτη:
- Κάθε κουτάκι (square) εμφανίζεται ως ορθογώνιο πάνω στον χάρτη.
- Με κάθε ρίψη ζαριού το πλοίο κινείται κατά τόσα κουτάκια.
- Αν το κουτάκι έχει event, εμφανίζεται σχετικό μήνυμα.
""")

# ------------------------------
# 3) Session State για το παιχνίδι
# ------------------------------
if "boat_index" not in st.session_state:
    st.session_state["boat_index"] = 0  # αρχική θέση στο πρώτο κουτάκι

if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False

# ------------------------------
# 4) Σχεδιασμός Χάρτη με τα κουτάκια
# ------------------------------
# Επιλέγουμε ως κέντρο το πρώτο κουτάκι για αρχική τοποθέτηση του χάρτη.
center_coords = board_squares[0]["coords"]
m = folium.Map(location=center_coords, zoom_start=7)

# Σχεδιάζουμε κάθε κουτάκι ως ορθογώνιο (rectangle)
for i, square in enumerate(board_squares):
    lat, lon = square["coords"]
    bounds = [(lat - BOX_SIZE, lon - BOX_SIZE), (lat + BOX_SIZE, lon + BOX_SIZE)]
    # Σχεδιάζουμε το ορθογώνιο με ελαφριά διαφάνεια
    folium.Rectangle(
        bounds=bounds,
        color='green',
        fill=True,
        fill_opacity=0.2,
        tooltip=f"{i}. {square['name']}"
    ).add_to(m)
    # Επίσης, προσθέτουμε ένα marker στο κέντρο για να φαίνεται το όνομα
    folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(html=f"""<div style="font-size: 12pt; color: darkgreen">{square['name']}</div>""")
    ).add_to(m)

# Marker για τη θέση του πλοίου (έγχρωμο εικονίδιο)
current_square = board_squares[st.session_state["boat_index"]]
folium.Marker(
    current_square["coords"],
    icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
    tooltip=f"Boat is here: {current_square['name']}"
).add_to(m)

# Εμφάνιση του χάρτη
st_folium(m, width=800, height=500)

# ------------------------------
# 5) Ρίψη ζαριού και μετακίνηση πλοίου
# ------------------------------
st.markdown("---")
if st.button("Roll the Dice"):
    if st.session_state["skip_turn"]:
        st.warning("You must skip this turn due to a previous event!")
        st.session_state["skip_turn"] = False
    else:
        dice = random.randint(1, 6)
        st.success(f"You rolled: {dice}")
        new_index = st.session_state["boat_index"] + dice
        if new_index >= len(board_squares):
            new_index = len(board_squares) - 1  # μένουμε στο τελευταίο κουτάκι
        st.session_state["boat_index"] = new_index

        current_square = board_squares[new_index]
        if current_square["event"]:
            st.info(f"Event on {current_square['name']}: {current_square['event']}")
            # Αν το event περιέχει λέξεις "skip" ή "delay" τότε παραλείπεται ο γύρος
            if "skip" in current_square["event"].lower() or "delay" in current_square["event"].lower() or "lose" in current_square["event"].lower():
                st.session_state["skip_turn"] = True

# Εμφάνιση τρέχουσας θέσης
current_sq = board_squares[st.session_state["boat_index"]]
st.write(f"**Boat is now at**: {current_sq['name']}")
if current_sq["event"]:
    st.write(f"**Square Event**: {current_sq['event']}")
else:
    st.write("No special event here.")
