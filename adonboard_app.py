import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import math
from datetime import date, timedelta

# ---------- Utility Functions ----------
def haversine_distance_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371.0 * c  # Earth radius in km

def distance_nm(lat1, lon1, lat2, lon2):
    """Υπολογίζει σε Ναυτικά Μίλια την απόσταση ανάμεσα σε δύο σημεία."""
    km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return km * 0.539957

# ---------- Αρχικοποίηση Session State ----------
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {
        "player": {
            "role": "Passenger",
            "ad_score": 0,
            "likes": 0,
            "shares": 0,
            "badges": [],
            "social_stats": {
                "facebook_friends": 0,
                "instagram_followers": 0,
                "adonboard_friends": 0,
                "posting_frequency": "Never"
            },
            "campaigns_joined": 0,
            "impressions": 0
        }
    }
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0

# ---------- Βασική Διάταξη ----------
st.set_page_config(page_title="Extended Maritime Route", layout="wide")
st.title("Extended Maritime Board Game with Longer Route & Intermediate Markers")

# ---------- Dashboard Προφίλ ----------
profile = st.session_state["profiles"]["player"]
st.markdown("### Profile Dashboard")
st.write(f"**Role:** {profile['role']}")
st.write(f"**Ad Score:** {profile['ad_score']}")
st.write(f"**Likes:** {profile['likes']}")
st.write(f"**Shares:** {profile['shares']}")
st.write(f"**Campaigns Joined:** {profile['campaigns_joined']}")
st.write(f"**Impressions:** {profile['impressions']}")
social = profile["social_stats"]
st.write(f"**Social Stats:** Facebook: {social['facebook_friends']}, Instagram: {social['instagram_followers']}, AdOnBoard: {social['adonboard_friends']}")
st.write(f"**Posting Frequency:** {social['posting_frequency']}")
if profile["badges"]:
    st.write("**Badges:** " + ", ".join(profile["badges"]))
else:
    st.write("**Badges:** None")

# ---------- Μεγάλο Δρομολόγιο ----------
# 15 Στάσεις (π.χ. σε μεγαλύτερη περιοχή), εσύ μπορείς να προσθέσεις/αλλάξεις
ROUTE_SQUARES = [
    {"name": "Rhodes Port", "coords": (36.4497, 28.2241), "event": "Start here. Beautiful Rhodes."},
    {"name": "Ialysos Coast", "coords": (36.4200, 28.1616), "event": "Ad Zone: You can run an Ad or Join Campaign."},
    {"name": "Kalithea Beach", "coords": (36.3825, 28.2472), "event": "Calm Waters, relax or run small Ad."},
    {"name": "Faliraki", "coords": (36.3435, 28.2110), "event": "Ad Zone: Potential Sponsor deals here."},
    {"name": "Lindos Bay", "coords": (36.0917, 28.0850), "event": "Lose a turn (bad weather)."},
    {"name": "Prasonisi", "coords": (35.8873, 27.7876), "event": "Bonus: Advance 1 square."},
    {"name": "Karpathos", "coords": (35.5077, 27.2139), "event": "Ad Zone: Run Ad or Join Campaign."},
    {"name": "Kasos Island", "coords": (35.4055, 26.9255), "event": "Storm area! Skip turn."},
    {"name": "Crete East", "coords": (35.2763, 26.1930), "event": "Nothing special here."},
    {"name": "Crete South", "coords": (34.9292, 24.8640), "event": "Ad Zone: Big Sponsor opportunity!"},
    {"name": "Gavdos Island", "coords": (34.8027, 24.0845), "event": "Mystery Island, unknown event."},
    {"name": "Calm Sea", "coords": (35.1000, 24.7000), "event": "Smooth sailing."},
    {"name": "Social Hub", "coords": (35.3000, 25.3000), "event": "Ad Zone: Join Ad. Possibly sponsor invites."},
    {"name": "Santorini", "coords": (36.3932, 25.4615), "event": "Bonus: Advance 1 square."},
    {"name": "Mykonos",  "coords": (37.4467, 25.3289), "event": "Finish - End of journey."}
]

st.write(f"**Current Position:** {ROUTE_SQUARES[st.session_state['current_index']]['name']}")
st.write(f"**Total NM Traveled:** {st.session_state['total_nm_traveled']:.2f} NM")

# ---------- Δημιουργία Χάρτη με Ενδιάμεσα Markers ----------
m = folium.Map(location=ROUTE_SQUARES[0]["coords"], zoom_start=6)

# Σχεδιάζουμε όλα τα τετράγωνα πάνω στο χάρτη ως ορθογώνια (προαιρετικά)
BOX_SIZE = 0.03
colors = ['#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f',
          '#ffb703', '#8ecae6', '#219ebc', '#023047', '#ffb703',
          '#006d77', '#9c6644', '#b56576', '#ee6c4d', '#3d5a80']

for i, sq in enumerate(ROUTE_SQUARES):
    lat, lon = sq["coords"]
    bounds = [(lat - BOX_SIZE, lon - BOX_SIZE), (lat + BOX_SIZE, lon + BOX_SIZE)]
    color = colors[i % len(colors)]
    popup_html = f"""
    <div style="font-family: Arial; font-size: 14px; text-align: center">
        <strong>{sq['name']}</strong><br>
        <em>{sq['event']}</em>
    </div>
    """
    folium.Rectangle(
        bounds=bounds,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.3,
        weight=2,
        tooltip=f"{i}. {sq['name']}",
        popup=folium.Popup(popup_html, max_width=200)
    ).add_to(m)
    folium.Marker(
        [lat, lon],
        tooltip=sq["name"],
        popup=sq["event"]
    ).add_to(m)

# Marker τρέχουσας θέσης πλοίου
current_coords = ROUTE_SQUARES[st.session_state["current_index"]]["coords"]
folium.Marker(
    current_coords,
    icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
    tooltip=f"Boat is here: {ROUTE_SQUARES[st.session_state['current_index']]['name']}"
).add_to(m)

st_folium(m, width=800, height=500)

# ---------- Κουμπί Ζαριού & Κίνηση σε Ενδιάμεσα Στάδια ----------
if st.button("Roll the Dice"):
    if st.session_state["skip_turn"]:
        st.warning("You must skip this turn due to a previous event!")
        st.session_state["skip_turn"] = False
    else:
        dice = random.randint(1, 6)
        st.success(f"You rolled a {dice}.")
        
        old_index = st.session_state["current_index"]
        new_index = old_index + dice
        if new_index >= len(ROUTE_SQUARES):
            new_index = len(ROUTE_SQUARES) - 1
        
        # Προσθέτουμε markers για κάθε "βήμα" ενδιάμεσα
        # π.χ. αν είμασταν στο 3 και το dice είναι 4, περνάμε 4 κουτάκια (4, 5, 6, 7)
        # και σε καθένα προσθέτουμε στο total_nm_traveled την απόσταση
        traveled_path = []  # για debug αν χρειαστεί
        for step in range(old_index, new_index):
            start_coords = ROUTE_SQUARES[step]["coords"]
            end_coords = ROUTE_SQUARES[step+1]["coords"]
            dist_step = distance_nm(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
            st.session_state["total_nm_traveled"] += dist_step
            traveled_path.append((step, step+1, dist_step))
        
        st.session_state["current_index"] = new_index
        
        # Ελέγχουμε το event στο νέο κουτάκι
        current_sq = ROUTE_SQUARES[new_index]
        st.info(f"Boat landed on {current_sq['name']}!")
        event_text = current_sq["event"].lower()
        
        # Αρνητικά events
        if "lose a turn" in event_text or "skip turn" in event_text or "storm" in event_text:
            st.warning("Negative event: you lose your next turn!")
            st.session_state["skip_turn"] = True
        # Bonus advance
        if "bonus: advance" in event_text:
            st.success("Bonus: Advance 1 extra square!")
            next_idx = min(new_index + 1, len(ROUTE_SQUARES) - 1)
            # πρόσθεσε και την απόσταση αυτή
            startC = ROUTE_SQUARES[new_index]["coords"]
            endC = ROUTE_SQUARES[next_idx]["coords"]
            dist_bon = distance_nm(startC[0], startC[1], endC[0], endC[1])
            st.session_state["total_nm_traveled"] += dist_bon
            st.session_state["current_index"] = next_idx
            st.info(f"Boat ended up at {ROUTE_SQUARES[next_idx]['name']} after bonus move!")
        
        # Ad Zones
        if "ad zone" in event_text:
            # Επιλογές "Run Ad" και "Join Ad Campaign"
            run_ad = st.button("Run Ad")
            join_camp = st.button("Join Ad Campaign")
            
            if run_ad:
                added_score = 10
                added_likes = random.randint(5, 15)
                added_shares = random.randint(2, 8)
                st.session_state["profiles"]["player"]["ad_score"] += added_score
                st.session_state["profiles"]["player"]["likes"] += added_likes
                st.session_state["profiles"]["player"]["shares"] += added_shares
                st.success(f"Ad run! +{added_score} ad score, +{added_likes} likes, +{added_shares} shares.")
            
            if join_camp:
                st.markdown("#### Join Ad Campaign")
                with st.form(key=f"form_campaign_{new_index}"):
                    fb = st.number_input("Number of Facebook Friends", min_value=0, step=1)
                    ig = st.number_input("Number of Instagram Followers", min_value=0, step=1)
                    adon = st.number_input("Number of AdOnBoard Friends", min_value=0, step=1)
                    post_freq = st.selectbox("Posting Frequency", ["Daily", "Weekly", "Monthly", "Rarely"])
                    duration = st.number_input("Campaign Duration (days)", min_value=1, value=3)
                    submit_info = st.form_submit_button("Submit Campaign Info")
                    if submit_info:
                        st.session_state["profiles"]["player"]["social_stats"]["facebook_friends"] = fb
                        st.session_state["profiles"]["player"]["social_stats"]["instagram_followers"] = ig
                        st.session_state["profiles"]["player"]["social_stats"]["adonboard_friends"] = adon
                        st.session_state["profiles"]["player"]["social_stats"]["posting_frequency"] = post_freq
                        st.session_state["profiles"]["player"]["campaigns_joined"] += 1
                        bscore = 20
                        st.session_state["profiles"]["player"]["ad_score"] += bscore
                        rand_impressions = random.randint(1000, 5000)
                        st.session_state["profiles"]["player"]["impressions"] += rand_impressions
                        st.success(f"You joined a campaign! +{bscore} ad score, +{rand_impressions} impressions.")
                        startD = date.today()
                        endD = startD + timedelta(days=duration)
                        st.info(f"Campaign from {startD} to {endD}.")
                        st.image("https://via.placeholder.com/600x300.png?text=Boat+Ad", caption="Boat Ad Display")
        
        # Αν ο ρόλος δεν έχει οριστεί, εμφανίζουμε επιλογές
        if "become ship owner" in event_text:
            become_owner = st.button("Become Ship Owner")
            if become_owner:
                st.session_state["profiles"]["player"]["role"] = "Ship Owner"
                st.success("You are now Ship Owner!")
        
        if "become sponsor" in event_text:
            become_sponsor = st.button("Become Sponsor")
            if become_sponsor:
                st.session_state["profiles"]["player"]["role"] = "Sponsor"
                st.success("You are now Sponsor!")
        
        # Αν βρισκόμαστε στο τελευταίο κουτάκι = τερματισμός
        if st.session_state["current_index"] == len(ROUTE_SQUARES) - 1:
            st.subheader("Journey Completed - Final Scoreboard")
            st.write(f"**Total Ad Campaigns**: {st.session_state['profiles']['player']['campaigns_joined']}")
            st.write(f"**Total Impressions**: {st.session_state['profiles']['player']['impressions']}")
            st.write(f"**Total NM Traveled**: {st.session_state['total_nm_traveled']:.2f} NM")
            if st.button("Restart Game"):
                st.session_state["current_index"] = 0
                st.session_state["skip_turn"] = False
                st.session_state["total_nm_traveled"] = 0.0
                st.session_state["profiles"]["player"]["ad_score"] = 0
                st.session_state["profiles"]["player"]["likes"] = 0
                st.session_state["profiles"]["player"]["shares"] = 0
                st.session_state["profiles"]["player"]["campaigns_joined"] = 0
                st.session_state["profiles"]["player"]["impressions"] = 0
                st.session_state["profiles"]["player"]["role"] = "Passenger"
                st.success("Game Restarted!")

# ---------- Ενημέρωση Dashboard ----------
st.markdown("### Updated Profile Dashboard")
profile = st.session_state["profiles"]["player"]
st.write(f"**Role:** {profile['role']}")
st.write(f"**Ad Score:** {profile['ad_score']}")
st.write(f"**Likes:** {profile['likes']}")
st.write(f"**Shares:** {profile['shares']}")
st.write(f"**Campaigns Joined:** {profile['campaigns_joined']}")
st.write(f"**Impressions:** {profile['impressions']}")
st.write(f"**Total NM Traveled:** {st.session_state['total_nm_traveled']:.2f} NM (so far)")
social = profile["social_stats"]
st.write(f"**Social Stats:** Facebook: {social['facebook_friends']}, Instagram: {social['instagram_followers']}, AdOnBoard: {social['adonboard_friends']}")
st.write(f"**Posting Frequency:** {social['posting_frequency']}")
if profile["badges"]:
    st.write("**Badges:** " + ", ".join(profile["badges"]))
else:
    st.write("**Badges:** None")
