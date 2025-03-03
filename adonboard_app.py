import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# ---------- Ορισμός Προφίλ στο Session State ----------
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {
        "player": {"role": "Passenger", "ad_score": 0, "likes": 0, "shares": 0, "badges": []}
    }

# ---------- Αρχικοποίηση Board Game Session State ----------
if "boat_index" not in st.session_state:
    st.session_state["boat_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False

# ---------- Επιλογή Ξεκινήματος Ρόλου ----------
starting_role = st.selectbox("Select Your Starting Role:", 
                             ["Passenger", "Ship Owner", "Sponsor"], 
                             key="starting_role")
st.session_state["profiles"]["player"]["role"] = starting_role

st.title("Interactive Maritime Board Game with Profile Dashboard")

# ---------- Προφίλ Dashboard ----------
st.markdown("### Profile Dashboard")
profile = st.session_state["profiles"]["player"]
st.write(f"**Role:** {profile['role']}")
st.write(f"**Ad Score:** {profile['ad_score']}")
st.write(f"**Likes:** {profile['likes']}")
st.write(f"**Shares:** {profile['shares']}")
if profile["badges"]:
    st.write("**Badges:** " + ", ".join(profile["badges"]))
else:
    st.write("**Badges:** None")

# ---------- Ορισμός Board Squares (10 κουτάκια) ----------
BOX_SIZE = 0.03  # Μέγεθος για σχεδίαση των κουτιών
box_colors = ['#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f',
              '#ffb703', '#8ecae6', '#219ebc', '#023047', '#ffb703']

# Ορισμός 10 κουτιών με διάφορα events και επιλογές (τα "Ad Zone" έχουν σχετικές οδηγίες)
board_squares = [
    {"name": "Start", "coords": (36.3932, 25.4615), "event": "Begin your journey."},
    {"name": "Calm Waters", "coords": (36.50, 25.55), "event": "Smooth sailing."},
    {"name": "Ad Zone A", "coords": (36.60, 25.60), "event": "Ad Zone: Run Ad to boost profile & option: Become Ship Owner."},
    {"name": "Choppy Seas", "coords": (36.70, 25.65), "event": "Waves ahead! Lose a turn."},
    {"name": "Ad Zone B", "coords": (36.80, 25.70), "event": "Ad Zone: Run Ad to boost profile & option: Become Sponsor."},
    {"name": "Stormy Waters", "coords": (36.90, 25.75), "event": "Severe storm! Skip turn."},
    {"name": "Treasure Island", "coords": (37.00, 25.80), "event": "Bonus: Advance 1 square."},
    {"name": "Social Hub", "coords": (37.10, 25.85), "event": "Ad Zone: Run Ad to gain likes and shares."},
    {"name": "Mystery Port", "coords": (37.20, 25.90), "event": "Nothing special here."},
    {"name": "Finish", "coords": (37.30, 25.95), "event": "Journey's End."}
]

st.markdown(f"**Current Board Position:** {board_squares[st.session_state['boat_index']]['name']}")

# ---------- Δημιουργία Χάρτη ----------
center_coords = board_squares[0]["coords"]
m = folium.Map(location=center_coords, zoom_start=6, tiles="cartodbpositron")

# Σχεδίαση των κουτιών ως ορθογώνια με custom popups
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
    # Εμφάνιση του ονόματος στο κέντρο του κουτιού
    folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(
            html=f"""<div style="font-size: 13pt; color: #1d3557; font-weight: bold">{square['name']}</div>"""
        )
    ).add_to(m)

# Marker για τη θέση του πλοίου
current_square = board_squares[st.session_state["boat_index"]]
folium.Marker(
    current_square["coords"],
    icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
    tooltip=f"Boat is here: {current_square['name']}"
).add_to(m)

st_folium(m, width=800, height=500)

# ---------- Λογική Ρόλων & ρίψη ζαριού ----------
if st.button("Roll the Dice"):
    if st.session_state["skip_turn"]:
        st.warning("You must skip this turn due to a previous event!")
        st.session_state["skip_turn"] = False
    else:
        dice = random.randint(1, 6)
        st.success(f"You rolled: {dice}")
        new_index = st.session_state["boat_index"] + dice
        if new_index >= len(board_squares):
            new_index = len(board_squares) - 1
        st.session_state["boat_index"] = new_index
        current_square = board_squares[new_index]
        st.info(f"Boat landed on: {current_square['name']}")
        
        # Επεξεργασία Event του κουτιού
        event_text = current_square["event"].lower()
        if "lose a turn" in event_text or "skip turn" in event_text or "storm" in event_text:
            st.info("Event: You lose your turn!")
            st.session_state["skip_turn"] = True
        if "bonus: advance" in event_text:
            st.success("Bonus: Advance 1 square!")
            st.session_state["boat_index"] = min(new_index + 1, len(board_squares) - 1)
        # Εάν είναι Ad Zone, δώσε επιλογή για "Run Ad" που ενημερώνει το προφίλ
        if "ad zone" in event_text:
            if st.button("Run Ad", key=f"run_ad_{new_index}"):
                added_score = 10
                added_likes = random.randint(5, 15)
                added_shares = random.randint(2, 8)
                st.session_state["profiles"]["player"]["ad_score"] += added_score
                st.session_state["profiles"]["player"]["likes"] += added_likes
                st.session_state["profiles"]["player"]["shares"] += added_shares
                st.success(f"Ad run! +{added_score} ad score, +{added_likes} likes, +{added_shares} shares.")
                # Εάν το event προσφέρει επιλογή αλλαγής ρόλου:
                if "become ship owner" in event_text:
                    if st.button("Become Ship Owner", key=f"owner_{new_index}"):
                        st.session_state["profiles"]["player"]["role"] = "Ship Owner"
                        st.success("Role changed: You are now a Ship Owner!")
                if "become sponsor" in event_text:
                    if st.button("Become Sponsor", key=f"sponsor_{new_index}"):
                        st.session_state["profiles"]["player"]["role"] = "Sponsor"
                        st.success("Role changed: You are now a Sponsor!")
        
    current_sq = board_squares[st.session_state["boat_index"]]
    st.write(f"**Boat is now at:** {current_sq['name']}")
    st.write(f"**Square Event:** {current_sq['event']}")
    
    # Ενημέρωση του Dashboard προφίλ
    st.markdown("### Updated Profile Dashboard")
    profile = st.session_state["profiles"]["player"]
    st.write(f"**Role:** {profile['role']}")
    st.write(f"**Ad Score:** {profile['ad_score']}")
    st.write(f"**Likes:** {profile['likes']}")
    st.write(f"**Shares:** {profile['shares']}")
    if profile["badges"]:
        st.write("**Badges:** " + ", ".join(profile["badges"]))
    else:
        st.write("**Badges:** None")
