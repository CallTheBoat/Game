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
    return 6371.0 * c

def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
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
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0
if "distance_buffer" not in st.session_state:
    st.session_state["distance_buffer"] = 0.0
if "total_points" not in st.session_state:
    st.session_state["total_points"] = 0
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []

# ---------- Νέα μεταβλητή για να μην εμφανίζεται συνέχεια η προσφορά στο ίδιο γύρισμα ----------
if "already_offered_campaign" not in st.session_state:
    st.session_state["already_offered_campaign"] = False

# ---------- Βασική Διάταξη ----------
st.set_page_config(page_title="Extended Maritime Route", layout="wide")
st.title("Extended Maritime Board Game with Sponsor Campaign Offers")

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

# ---------- Διαδρομή 15 Στάσεων ----------
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
    st.session_state["distance_buffer"] += dist_nm
    points_gained = 0
    while st.session_state["distance_buffer"] >= 10:
        st.session_state["distance_buffer"] -= 10
        points_gained += 1
    return points_gained

# ---------- Διαδικασία για Sponsored Campaign Offer ----------
def maybe_offer_sponsored_campaign():
    """
    Με πιθανότητα 1/3 εμφανίζεται ένα popup για προσφορά χορηγίας.
    Εάν ο παίκτης δεχτεί, εμφανίζονται οι πληροφορίες καμπάνιας (εταιρεία, απαιτούμενα impressions, κτλ).
    """
    chance = random.random()
    if chance < 0.33:
        # Επιλέγουμε τυχαία στοιχεία της διαφημιστικής καμπάνιας
        sponsor_names = ["Vodafone", "Nike", "Adidas", "Coca-Cola", "Pepsi"]
        sponsor = random.choice(sponsor_names)
        required_impressions = random.randint(500, 2000)  # τυχαίο απαιτούμενο
        discount_percent = random.choice([20, 30, 50, 70])
        st.info(f"**Sponsored Campaign Offer**: {sponsor} ζητάει τουλάχιστον {required_impressions} impressions για να σου δώσει έκπτωση {discount_percent}%. Δέχεσαι;")
        
        accept = st.button(f"Ναι, δέχομαι την προσφορά της {sponsor}")
        decline = st.button("Όχι, προχωράω κανονικά")
        
        if accept:
            # Εμφανίζουμε λεπτομέρειες της καμπάνιας
            st.success(f"Έγινες δεκτός στην καμπάνια της {sponsor}!")
            duration_days = random.randint(2, 7)
            startD = date.today()
            endD = startD + timedelta(days=duration_days)
            st.markdown(f"- **Διάρκεια**: {duration_days} ημέρες ({startD} έως {endD})")
            st.markdown(f"- **Απαιτούμενα Impressions**: {required_impressions}")
            st.markdown(f"- **Παραλίες**: Lindos, Faliraki, Tsambika")
            st.markdown(f"- **Διαφημιστικό Υλικό**: Μπλουζάκια, banners της {sponsor}")
            
            # Αν θες να συνδέσεις την επιτυχία της καμπάνιας με τα actual impressions του παίκτη, π.χ.:
            st.session_state["profiles"]["player"]["campaigns_joined"] += 1
            # ...και όποιους πόντους θέλεις να δώσεις
            st.session_state["total_points"] += 5  # π.χ. +5 πόντοι για το accept
            add_scoreboard_entry(
                action=f"Accepted {sponsor} campaign",
                distance_nm=0,
                total_points_gained=5
            )
        elif decline:
            st.warning("Απέρριψες την καμπάνια και συνεχίζεις.")

# ---------- Κουμπί Ζαριού ----------
if st.button("Roll the Dice"):
    if st.session_state["skip_turn"]:
        st.warning("You must skip this turn due to a previous event!")
        st.session_state["skip_turn"] = False
    else:
        st.session_state["already_offered_campaign"] = False  # reset για νέα ζαριά
        dice = random.randint(1, 6)
        st.success(f"You rolled a {dice}.")
        
        old_index = st.session_state["current_index"]
        new_index = old_index + dice
        if new_index >= len(ROUTE_SQUARES):
            new_index = len(ROUTE_SQUARES) - 1
        
        # Κίνηση βήμα-βήμα
        for step in range(old_index, new_index):
            start_coords = ROUTE_SQUARES[step]["coords"]
            end_coords = ROUTE_SQUARES[step+1]["coords"]
            dist_step = distance_nm(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
            st.session_state["total_nm_traveled"] += dist_step
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
        
        if "ad zone" in event_text:
            run_ad_click = st.button("Run Ad")
            join_camp_click = st.button("Join Ad Campaign")
            
            if run_ad_click:
                ad_points = 10
                st.session_state["total_points"] += ad_points
                st.session_state["profiles"]["player"]["ad_score"] += 10
                l = random.randint(5, 15)
                sh = random.randint(2, 8)
                st.session_state["profiles"]["player"]["likes"] += l
                st.session_state["profiles"]["player"]["shares"] += sh
                points_from_likes = l * 10
                points_from_shares = sh * 10
                st.session_state["total_points"] += (points_from_likes + points_from_shares)
                
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
                st.markdown("#### Join Ad Campaign")
                with st.form(key=f"ad_campaign_form_{new_index}"):
                    fb = st.number_input("Number of Facebook Friends", min_value=0, step=1)
                    ig = st.number_input("Number of Instagram Followers", min_value=0, step=1)
                    adon = st.number_input("Number of AdOnBoard Friends", min_value=0, step=1)
                    posting_freq = st.selectbox("Posting Frequency", ["Daily", "Weekly", "Monthly", "Rarely"])
                    duration_days = st.number_input("Campaign Duration (days)", min_value=1, value=3, step=1)
                    submit_campaign = st.form_submit_button("Submit Campaign Info")
                    if submit_campaign:
                        st.session_state["profiles"]["player"]["social_stats"]["facebook_friends"] = fb
                        st.session_state["profiles"]["player"]["social_stats"]["instagram_followers"] = ig
                        st.session_state["profiles"]["player"]["social_stats"]["adonboard_friends"] = adon
                        st.session_state["profiles"]["player"]["social_stats"]["posting_frequency"] = posting_freq
                        st.session_state["profiles"]["player"]["campaigns_joined"] += 1
                        base_camp_points = 20
                        st.session_state["total_points"] += base_camp_points
                        rand_impressions = random.randint(1000, 5000)
                        st.session_state["profiles"]["player"]["impressions"] += rand_impressions
                        
                        add_scoreboard_entry(
                            action="Join Ad Campaign",
                            total_points_gained=base_camp_points
                        )
                        
                        st.success(f"Campaign joined! +{base_camp_points} pts, +{rand_impressions} impressions.")
                        start_date = date.today()
                        end_date = start_date + timedelta(days=duration_days)
                        st.markdown(f"**Campaign Dates:** {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                        st.image("https://via.placeholder.com/800x400.png?text=Sailing+Ship", caption="Sailing Ship in Action")
                        beaches = ["Lindos Beach", "Faliraki Beach", "Tsambika Beach"]
                        st.markdown("**Beaches on the Route:** " + ", ".join(beaches))
        
        if "become ship owner" in event_text:
            if st.button("Become Ship Owner"):
                st.session_state["profiles"]["player"]["role"] = "Ship Owner"
                st.success("You are now Ship Owner!")
        if "become sponsor" in event_text:
            if st.button("Become Sponsor"):
                st.session_state["profiles"]["player"]["role"] = "Sponsor"
                st.success("You are now Sponsor!")
        
        # Τυχαία προσφορά χορηγίας (εάν δεν έγινε ήδη σε αυτή τη ζαριά)
        if not st.session_state["already_offered_campaign"]:
            maybe_offer_sponsored_campaign()
            st.session_state["already_offered_campaign"] = True
        
        # Τέλος Διαδρομής;
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
