import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import math
from datetime import date, timedelta

# ---------- Utility Functions ----------
def haversine_distance_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lat2 - lon2)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371.0 * c  # Earth radius in km

def distance_nm(lat1, lon1, lat2, lon2):
    """Υπολογίζει σε Ναυτικά Μίλια την απόσταση ανάμεσα σε δύο σημεία."""
    # Διορθώνουμε το λάθος στο d_lon
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

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

# Συνολικά Ναυτικά Μίλια που έχουμε διανύσει
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0

# Buffer για να υπολογίζουμε πόντους από απόσταση (κάθε 10 NM = 1 πόντος)
if "distance_buffer" not in st.session_state:
    st.session_state["distance_buffer"] = 0.0

# Συνολικοί πόντοι
if "total_points" not in st.session_state:
    st.session_state["total_points"] = 0

# Scoreboard σαν λίστα από ενέργειες
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []

# ---------- Βασική Διάταξη ----------
st.set_page_config(page_title="Extended Maritime Route", layout="wide")
st.title("Extended Maritime Board Game with Points & Scoreboard")

# ---------- Dashboard Προφίλ ----------
profile = st.session_state["profiles"]["player"]
st.markdown("### Profile Dashboard")
st.write(f"**Role:** {profile['role']}")
st.write(f"**Ad Score:** {profile['ad_score']}")
st.write(f"**Likes:** {profile['likes']}")
st.write(f"**Shares:** {profile['shares']}")
st.write(f"**Campaigns Joined:** {profile['campaigns_joined']}")
st.write(f"**Impressions:** {profile['impressions']}")
st.write(f"**Total Points:** {st.session_state['total_points']}")
social = profile["social_stats"]
st.write(f"**Social Stats:** Facebook: {social['facebook_friends']}, Instagram: {social['instagram_followers']}, AdOnBoard: {social['adonboard_friends']}")
st.write(f"**Posting Frequency:** {social['posting_frequency']}")
if profile["badges"]:
    st.write("**Badges:** " + ", ".join(profile["badges"]))
else:
    st.write("**Badges:** None")

# ---------- Μεγάλο Δρομολόγιο (15 Στάσεις) ----------
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

# ---------- Δημιουργία Χάρτη ----------
m = folium.Map(location=ROUTE_SQUARES[0]["coords"], zoom_start=6)

BOX_SIZE = 0.03
colors = [
    '#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f',
    '#ffb703', '#8ecae6', '#219ebc', '#023047', '#ffb703',
    '#006d77', '#9c6644', '#b56576', '#ee6c4d', '#3d5a80'
]

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

# Marker πλοίου
current_coords = ROUTE_SQUARES[st.session_state["current_index"]]["coords"]
folium.Marker(
    current_coords,
    icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
    tooltip=f"Boat is here: {ROUTE_SQUARES[st.session_state['current_index']]['name']}"
).add_to(m)

st_folium(m, width=800, height=500)

# ---------- Συνάρτηση: Προσθήκη γραμμής στο scoreboard ----------
def add_scoreboard_entry(action, distance_nm=0.0, likes=0, shares=0, ad_run=False, total_points_gained=0):
    row = {
        "Action": action,
        "Distance(NM)": round(distance_nm, 2),
        "Likes": likes,
        "Shares": shares,
        "AdRun?": ("Yes" if ad_run else "No"),
        "Points Gained": total_points_gained,
        "Total Points So Far": st.session_state["total_points"]
    }
    st.session_state["scoreboard"].append(row)

# ---------- Υπολογισμός πόντων από απόσταση ----------
def add_distance_points(dist_nm):
    """
    Προσθέτει την απόσταση στο distance_buffer.
    Για κάθε 10 NM στο buffer, κερδίζει 1 πόντο.
    """
    st.session_state["distance_buffer"] += dist_nm
    points_gained = 0
    while st.session_state["distance_buffer"] >= 10:
        st.session_state["distance_buffer"] -= 10
        points_gained += 1
    return points_gained

# ---------- Πάτημα Ζαριού ----------
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
        
        # Βήμα-βήμα μετακίνηση, για να μετράμε αποστάσεις τμηματικά
        for step in range(old_index, new_index):
            start_coords = ROUTE_SQUARES[step]["coords"]
            end_coords = ROUTE_SQUARES[step+1]["coords"]
            dist_step = distance_nm(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
            st.session_state["total_nm_traveled"] += dist_step
            # Υπολογισμός πόντων από την απόσταση
            dist_points = add_distance_points(dist_step)
            st.session_state["total_points"] += dist_points
            if dist_points > 0:
                add_scoreboard_entry(
                    action=f"Moved from {step} to {step+1}",
                    distance_nm=dist_step,
                    total_points_gained=dist_points
                )
        
        st.session_state["current_index"] = new_index
        current_sq = ROUTE_SQUARES[new_index]
        st.info(f"Boat landed on {current_sq['name']}!")
        
        # Event λογική
        event_text = current_sq["event"].lower()
        if "lose a turn" in event_text or "skip turn" in event_text or "storm" in event_text:
            st.warning("Negative event: you lose your next turn!")
            st.session_state["skip_turn"] = True
        
        if "bonus: advance" in event_text:
            st.success("Bonus: Advance 1 extra square!")
            next_idx = min(new_index + 1, len(ROUTE_SQUARES) - 1)
            startC = ROUTE_SQUARES[new_index]["coords"]
            endC = ROUTE_SQUARES[next_idx]["coords"]
            dist_bon = distance_nm(startC[0], startC[1], endC[0], endC[1])
            st.session_state["total_nm_traveled"] += dist_bon
            dist_points_bon = add_distance_points(dist_bon)
            st.session_state["total_points"] += dist_points_bon
            if dist_points_bon > 0:
                add_scoreboard_entry(
                    action="Bonus Advance",
                    distance_nm=dist_bon,
                    total_points_gained=dist_points_bon
                )
            st.session_state["current_index"] = next_idx
            st.info(f"Boat ended up at {ROUTE_SQUARES[next_idx]['name']} after bonus move!")
        
        # Ad Zone
        if "ad zone" in event_text:
            run_ad_click = st.button("Run Ad")
            join_camp_click = st.button("Join Ad Campaign")
            
            if run_ad_click:
                # Κάθε φορά που τρέχει μια διαφήμιση (Run Ad) = 10 πόντοι
                ad_points = 10
                st.session_state["total_points"] += ad_points
                st.session_state["profiles"]["player"]["ad_score"] += 10
                
                # Likes & Shares
                l = random.randint(5, 15)   # τυχαία likes
                sh = random.randint(2, 8)  # τυχαία shares
                st.session_state["profiles"]["player"]["likes"] += l
                st.session_state["profiles"]["player"]["shares"] += sh
                
                # Κάθε like/share = 10 πόντοι
                points_from_likes = l * 10
                points_from_shares = sh * 10
                st.session_state["total_points"] += points_from_likes
                st.session_state["total_points"] += points_from_shares
                
                # Scoreboard entry
                add_scoreboard_entry(
                    action="Run Ad",
                    distance_nm=0,
                    likes=l,
                    shares=sh,
                    ad_run=True,
                    total_points_gained=(ad_points + points_from_likes + points_from_shares)
                )
                
                st.success(f"Ran an Ad! +{ad_points} pts for Ad, +{l} likes (={l*10} pts), +{sh} shares (={sh*10} pts).")
            
            if join_camp_click:
                # Φόρμα για συμμετοχή σε Campaign
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
                        base_camp_points = 20  # πόντοι για τη συμμετοχή
                        st.session_state["total_points"] += base_camp_points
                        
                        # Και κάποια impressions
                        rand_impressions = random.randint(1000, 5000)
                        st.session_state["profiles"]["player"]["impressions"] += rand_impressions
                        
                        # Scoreboard entry για campaign
                        add_scoreboard_entry(
                            action="Join Ad Campaign",
                            distance_nm=0,
                            likes=0,
                            shares=0,
                            ad_run=False,
                            total_points_gained=base_camp_points
                        )
                        
                        st.success(f"Joined campaign: +{base_camp_points} pts, +{rand_impressions} impressions.")
                        startD = date.today()
                        endD = startD + timedelta(days=duration)
                        st.info(f"Campaign from {startD} to {endD}.")
                        st.image("https://via.placeholder.com/600x300.png?text=Boat+Ad", caption="Boat Ad Display")
        
        # Έλεγχος αλλαγής ρόλου
        if "become ship owner" in event_text:
            if st.button("Become Ship Owner"):
                st.session_state["profiles"]["player"]["role"] = "Ship Owner"
                st.success("You are now Ship Owner!")
        if "become sponsor" in event_text:
            if st.button("Become Sponsor"):
                st.session_state["profiles"]["player"]["role"] = "Sponsor"
                st.success("You are now Sponsor!")
        
        # Εάν βρισκόμαστε στο τέλος
        if st.session_state["current_index"] == len(ROUTE_SQUARES) - 1:
            st.subheader("Journey Completed - Final Scoreboard")
            st.write(f"**Total Ad Campaigns**: {st.session_state['profiles']['player']['campaigns_joined']}")
            st.write(f"**Total Impressions**: {st.session_state['profiles']['player']['impressions']}")
            st.write(f"**Total NM Traveled**: {st.session_state['total_nm_traveled']:.2f} NM")
            st.write(f"**Total Points**: {st.session_state['total_points']}")
            if st.button("Restart Game"):
                st.session_state["current_index"] = 0
                st.session_state["skip_turn"] = False
                st.session_state["total_nm_traveled"] = 0.0
                st.session_state["distance_buffer"] = 0.0
                st.session_state["total_points"] = 0
                st.session_state["scoreboard"] = []
                
                st.session_state["profiles"]["player"]["ad_score"] = 0
                st.session_state["profiles"]["player"]["likes"] = 0
                st.session_state["profiles"]["player"]["shares"] = 0
                st.session_state["profiles"]["player"]["campaigns_joined"] = 0
                st.session_state["profiles"]["player"]["impressions"] = 0
                st.session_state["profiles"]["player"]["role"] = "Passenger"
                
                st.success("Game Restarted!")

# ---------- Εμφάνιση Scoreboard ----------
st.markdown("## Scoreboard")
if len(st.session_state["scoreboard"]) > 0:
    st.dataframe(st.session_state["scoreboard"])
else:
    st.write("No actions recorded yet.")
