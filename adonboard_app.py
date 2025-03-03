import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import math

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
    km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return km * 0.539957  # μετατροπή σε ναυτικά μίλια

# ---------- Initial Session State Setup ----------
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {
        "player": {
            "role": "Passenger",
            "ad_score": 0,
            "likes": 0,
            "shares": 0,
            "badges": [],
            # Social στατιστικά
            "social_stats": {
                "facebook_friends": 0,
                "instagram_followers": 0,
                "adonboard_friends": 0,
                "posting_frequency": "Never"
            },
            # Στατιστικά καμπάνιας
            "campaigns_joined": 0,
            "impressions": 0
        }
    }
if "boat_index" not in st.session_state:
    st.session_state["boat_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0

# ---------- Main App Header ----------
st.set_page_config(page_title="Interactive Maritime Board Game", layout="wide")
st.title("Interactive Maritime Board Game with Profile Dashboard")

# ---------- Tabs Setup ----------
tabs = st.tabs(["Board Game", "Vodafone Campaign Simulation"])

# ------------------ TAB 1: BOARD GAME ------------------
with tabs[0]:
    # Επιλογή Ξεκινήματος Ρόλου
    starting_role = st.selectbox("Select Your Starting Role:", 
                                 ["Passenger", "Ship Owner", "Sponsor"], 
                                 key="starting_role")
    st.session_state["profiles"]["player"]["role"] = starting_role

    st.markdown("### Profile Dashboard")
    profile = st.session_state["profiles"]["player"]
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
    
    # Ορισμός Board Squares (10 κουτάκια)
    BOX_SIZE = 0.03  
    box_colors = ['#a8dadc', '#f1faee', '#457b9d', '#e63946', '#2a9d8f',
                  '#ffb703', '#8ecae6', '#219ebc', '#023047', '#ffb703']
    board_squares = [
        {"name": "Start", "coords": (36.3932, 25.4615), "event": "Begin your journey."},
        {"name": "Calm Waters", "coords": (36.50, 25.55), "event": "Smooth sailing."},
        {"name": "Ad Zone A", "coords": (36.60, 25.60), "event": "Ad Zone: Run Ad & Option: Become Ship Owner & Join Ad Campaign."},
        {"name": "Choppy Seas", "coords": (36.70, 25.65), "event": "Waves! Lose a turn."},
        {"name": "Ad Zone B", "coords": (36.80, 25.70), "event": "Ad Zone: Run Ad & Option: Become Sponsor & Join Ad Campaign."},
        {"name": "Stormy Waters", "coords": (36.90, 25.75), "event": "Severe storm! Skip turn."},
        {"name": "Treasure Island", "coords": (37.00, 25.80), "event": "Bonus: Advance 1 square."},
        {"name": "Social Hub", "coords": (37.10, 25.85), "event": "Ad Zone: Run Ad to gain likes and shares."},
        {"name": "Mystery Port", "coords": (37.20, 25.90), "event": "Nothing special here."},
        {"name": "Finish", "coords": (37.30, 25.95), "event": "Journey's End."}
    ]
    
    st.markdown(f"**Current Board Position:** {board_squares[st.session_state['boat_index']]['name']}")
    st.markdown(f"**Total NM Traveled:** {st.session_state['total_nm_traveled']:.2f} NM")
    
    center_coords = board_squares[0]["coords"]
    m = folium.Map(location=center_coords, zoom_start=6, tiles="cartodbpositron")
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
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f"""<div style="font-size: 13pt; color: #1d3557; font-weight: bold">{square['name']}</div>"""
            )
        ).add_to(m)
    current_square = board_squares[st.session_state["boat_index"]]
    folium.Marker(
        current_square["coords"],
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip=f"Boat is here: {current_square['name']}"
    ).add_to(m)
    st_folium(m, width=800, height=500)
    
    if st.button("Roll the Dice"):
        if st.session_state["skip_turn"]:
            st.warning("You must skip this turn due to a previous event!")
            st.session_state["skip_turn"] = False
        else:
            prev_index = st.session_state["boat_index"]
            prev_coords = board_squares[prev_index]["coords"]
            dice = random.randint(1, 6)
            st.success(f"You rolled: {dice}")
            new_index = st.session_state["boat_index"] + dice
            if new_index >= len(board_squares):
                new_index = len(board_squares) - 1
            st.session_state["boat_index"] = new_index
            new_coords = board_squares[new_index]["coords"]
            additional_nm = distance_nm(prev_coords[0], prev_coords[1], new_coords[0], new_coords[1])
            st.session_state["total_nm_traveled"] += additional_nm
            
            current_square = board_squares[new_index]
            st.info(f"Boat landed on: {current_square['name']}")
            event_text = current_square["event"].lower()
            if "lose a turn" in event_text or "skip turn" in event_text or "storm" in event_text:
                st.info("Event: You lose your turn!")
                st.session_state["skip_turn"] = True
            if "bonus: advance" in event_text:
                st.success("Bonus: Advance 1 square!")
                st.session_state["boat_index"] = min(new_index + 1, len(board_squares) - 1)
                bonus_coords = board_squares[st.session_state["boat_index"]]["coords"]
                additional_nm_bonus = distance_nm(new_coords[0], new_coords[1], bonus_coords[0], bonus_coords[1])
                st.session_state["total_nm_traveled"] += additional_nm_bonus
            if "ad zone" in event_text:
                if st.button("Run Ad", key=f"run_ad_{new_index}"):
                    added_score = 10
                    added_likes = random.randint(5, 15)
                    added_shares = random.randint(2, 8)
                    st.session_state["profiles"]["player"]["ad_score"] += added_score
                    st.session_state["profiles"]["player"]["likes"] += added_likes
                    st.session_state["profiles"]["player"]["shares"] += added_shares
                    st.success(f"Ad run! +{added_score} ad score, +{added_likes} likes, +{added_shares} shares.")
                    if "become ship owner" in event_text:
                        if st.button("Become Ship Owner", key=f"owner_{new_index}"):
                            st.session_state["profiles"]["player"]["role"] = "Ship Owner"
                            st.success("Role changed: You are now a Ship Owner!")
                    if "become sponsor" in event_text:
                        if st.button("Become Sponsor", key=f"sponsor_{new_index}"):
                            st.session_state["profiles"]["player"]["role"] = "Sponsor"
                            st.success("Role changed: You are now a Sponsor!")
                if st.button("Join Ad Campaign", key=f"join_ad_{new_index}"):
                    st.markdown("#### Ad Campaign Participation")
                    with st.form(key=f"ad_campaign_form_{new_index}"):
                        fb = st.number_input("Number of Facebook Friends", min_value=0, step=1)
                        ig = st.number_input("Number of Instagram Followers", min_value=0, step=1)
                        adon = st.number_input("Number of AdOnBoard Friends", min_value=0, step=1)
                        posting_freq = st.selectbox("Posting Frequency", ["Daily", "Weekly", "Monthly", "Rarely"])
                        submit_campaign = st.form_submit_button("Submit Campaign Info")
                        if submit_campaign:
                            st.session_state["profiles"]["player"]["social_stats"]["facebook_friends"] = fb
                            st.session_state["profiles"]["player"]["social_stats"]["instagram_followers"] = ig
                            st.session_state["profiles"]["player"]["social_stats"]["adonboard_friends"] = adon
                            st.session_state["profiles"]["player"]["social_stats"]["posting_frequency"] = posting_freq
                            bonus_campaign = 20
                            st.session_state["profiles"]["player"]["ad_score"] += bonus_campaign
                            st.session_state["profiles"]["player"]["campaigns_joined"] += 1
                            campaign_impressions = random.randint(1000, 5000)
                            st.session_state["profiles"]["player"]["impressions"] += campaign_impressions
                            st.success(f"Campaign joined! Bonus +{bonus_campaign} ad score, +{campaign_impressions} impressions.")
            
        if st.session_state["boat_index"] == len(board_squares) - 1:
            st.markdown("## Final Scoreboard")
            st.write(f"Total Ad Campaigns Participated: {st.session_state['profiles']['player']['campaigns_joined']}")
            st.write(f"Total Impressions: {st.session_state['profiles']['player']['impressions']}")
            st.write(f"Total Nautical Miles Traveled: {st.session_state['total_nm_traveled']:.2f} NM")
            if st.button("Restart Game"):
                for key in ["boat_index", "skip_turn", "total_nm_traveled"]:
                    st.session_state[key] = 0 if key != "total_nm_traveled" else 0.0
                st.session_state["profiles"]["player"]["ad_score"] = 0
                st.session_state["profiles"]["player"]["likes"] = 0
                st.session_state["profiles"]["player"]["shares"] = 0
                st.session_state["profiles"]["player"]["campaigns_joined"] = 0
                st.session_state["profiles"]["player"]["impressions"] = 0
                st.session_state["profiles"]["player"]["role"] = "Passenger"
                st.success("Game restarted!")
        
        current_sq = board_squares[st.session_state["boat_index"]]
        st.write(f"**Boat is now at:** {current_sq['name']}")
        st.write(f"**Square Event:** {current_sq['event']}")
        
        st.markdown("### Updated Profile Dashboard")
        profile = st.session_state["profiles"]["player"]
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

# ------------------ TAB 2: VODAFONE CAMPAIGN SIMULATION ------------------
with tabs[1]:
    st.subheader("Vodafone Campaign Simulation")
    st.write("This is a test scenario for a Vodafone ad campaign over 3 days.")
    st.write("**Campaign Requirements:** Spend at least 70% of the campaign time near Rhodes beaches and gather at least 1000 impressions to win an 80% discount on a boat rental (initial price: €1500).")
    # Καμπάνια 3 ημερών
    st.write("Campaign Duration: 3 Days")
    near_beach = st.slider("Percentage of time spent near Rhodes beaches", 0, 100, 70)
    impressions = st.number_input("Total impressions collected during campaign", min_value=0, value=1000, step=50)
    if st.button("Run Vodafone Campaign"):
        if near_beach >= 70 and impressions >= 1000:
            discount = 0.8
            final_cost = 1500 * (1 - discount)
            st.success(f"Campaign Successful! You win an 80% discount. Final boat rental cost: €{final_cost:.2f}")
        else:
            st.error("Campaign Failed. Requirements not met. (Need ≥70% time near beaches and ≥1000 impressions)")
