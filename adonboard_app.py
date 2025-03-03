import streamlit as st
import random
import math
from datetime import date, timedelta
import folium
from streamlit_folium import st_folium

# ========== Utility Functions ==========
def haversine_distance_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist_km = 6371.0 * c
    return dist_km

def distance_nm(lat1, lon1, lat2, lon2):
    """Υπολογίζει τη ναυτική απόσταση μεταξύ δύο συντεταγμένων."""
    km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return km * 0.539957

# ========== Session State ==========
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []
if "already_offered_campaign" not in st.session_state:
    st.session_state["already_offered_campaign"] = False
if "active_campaign" not in st.session_state:
    st.session_state["active_campaign"] = None

# Απλό προφίλ με βασικές μετρικές
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "role": "Passenger",
        "ad_score": 0,
        "likes": 0,
        "shares": 0,
        "campaigns_joined": 0,
        "impressions": 0
    }

# ========== Tabs ==========
tabs = st.tabs(["Board Game", "Campaign Details"])

# ========== TAB 2: Campaign Details ==========
with tabs[1]:
    st.subheader("Campaign Details")
    if st.session_state["active_campaign"] is None:
        st.info("No active campaign at the moment.")
    else:
        camp = st.session_state["active_campaign"]
        st.success(f"You accepted a campaign from **{camp['sponsor']}**!")
        st.write(f"**Required Impressions**: {camp['required_impressions']}")
        st.write(f"**Discount**: {camp['discount_percent']}%")
        st.write(f"**Duration**: {camp['duration_days']} days")
        st.write(f"**Dates**: {camp['start_date']} to {camp['end_date']}")
        st.write(f"**Beaches**: {', '.join(camp['beaches'])}")
        st.write(f"**Materials**: {camp['materials']}")
        st.write("***Now you can gather impressions to reach the sponsor's goal!***")

# ========== TAB 1: Board Game ==========
with tabs[0]:
    st.title("Extended Maritime Board Game")
    
    # -- Board squares (10 stops)
    board_squares = [
        {"name": "Rhodes Port", "coords": (36.4497, 28.2241), "event": "Start here."},
        {"name": "Ialysos Coast", "coords": (36.4200, 28.1616), "event": "Ad Zone: Sponsor deals possible."},
        {"name": "Kalithea Beach", "coords": (36.3825, 28.2472), "event": "Calm Waters."},
        {"name": "Faliraki", "coords": (36.3435, 28.2110), "event": "Ad Zone: Potential Sponsor deals."},
        {"name": "Lindos Bay", "coords": (36.0917, 28.0850), "event": "Lose a turn."},
        {"name": "Prasonisi", "coords": (35.8873, 27.7876), "event": "Bonus: Advance 1 square."},
        {"name": "Karpathos", "coords": (35.5077, 27.2139), "event": "Ad Zone: Run Ad or Join Campaign."},
        {"name": "Kasos Island", "coords": (35.4055, 26.9255), "event": "Storm area! Skip turn."},
        {"name": "Crete East", "coords": (35.2763, 26.1930), "event": "Nothing special."},
        {"name": "Finish", "coords": (35.0, 26.0), "event": "Journey ends here."},
    ]
    
    st.write(f"**Current Position**: {board_squares[st.session_state['current_index']]['name']}")
    st.write(f"**Total NM Traveled**: {st.session_state['total_nm_traveled']:.2f}")

    # -- Map
    m = folium.Map(location=board_squares[0]["coords"], zoom_start=7)
    for i, sq in enumerate(board_squares):
        folium.Marker(
            sq["coords"],
            tooltip=sq["name"],
            popup=sq["event"]
        ).add_to(m)
    
    # Marker for current position
    current_coords = board_squares[st.session_state["current_index"]]["coords"]
    folium.Marker(
        current_coords,
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip=f"Boat is here: {board_squares[st.session_state['current_index']]['name']}"
    ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    # -- Roll dice
    if st.button("Roll the Dice"):
        if st.session_state["skip_turn"]:
            st.warning("You skip this turn due to an event!")
            st.session_state["skip_turn"] = False
        else:
            st.session_state["already_offered_campaign"] = False
            dice = random.randint(1, 6)
            st.success(f"You rolled: {dice}")
            
            old_index = st.session_state["current_index"]
            new_index = old_index + dice
            if new_index >= len(board_squares):
                new_index = len(board_squares) - 1
            
            # Move step-by-step
            for step in range(old_index, new_index):
                c1 = board_squares[step]["coords"]
                c2 = board_squares[step+1]["coords"]
                dist_nm = distance_nm(c1[0], c1[1], c2[0], c2[1])
                st.session_state["total_nm_traveled"] += dist_nm
                st.session_state["scoreboard"].append({
                    "Action": f"Moved from {board_squares[step]['name']} to {board_squares[step+1]['name']}",
                    "Distance(NM)": round(dist_nm, 2),
                    "Likes": 0,
                    "Shares": 0,
                    "AdRun?": "No",
                    "Points Gained": 0,
                    "Total Points So Far": 0
                })
            
            st.session_state["current_index"] = new_index
            current_sq = board_squares[new_index]
            st.info(f"Landed on: {current_sq['name']}")
            
            # Check event
            if "lose a turn" in current_sq["event"].lower():
                st.warning("You lose your next turn!")
                st.session_state["skip_turn"] = True
            if "bonus: advance" in current_sq["event"].lower():
                st.success("Bonus: Advance 1 square!")
                bonus_new_idx = min(new_index + 1, len(board_squares) - 1)
                c1 = board_squares[new_index]["coords"]
                c2 = board_squares[bonus_new_idx]["coords"]
                dist_nm = distance_nm(c1[0], c1[1], c2[0], c2[1])
                st.session_state["total_nm_traveled"] += dist_nm
                st.info(f"Boat ended up at {board_squares[bonus_new_idx]['name']}")
                st.session_state["current_index"] = bonus_new_idx
            
            # Potential sponsor zone (just an example)
            if "ad zone" in current_sq["event"].lower():
                run_ad_click = st.button("Run Ad")
                if run_ad_click:
                    st.session_state["profile"]["ad_score"] += 10
                    st.session_state["profile"]["likes"] += 5
                    st.session_state["profile"]["shares"] += 2
                    st.success("Ran an Ad +10 ad_score, +5 likes, +2 shares.")
            
            # Chance to offer sponsor campaign (once per roll)
            if not st.session_state["already_offered_campaign"]:
                chance = random.random()
                if chance < 0.5:  # 50% example
                    sponsor_names = ["Vodafone", "Nike", "Adidas", "Coca-Cola", "Pepsi"]
                    sponsor = random.choice(sponsor_names)
                    required_impressions = random.randint(500, 2000)
                    discount_percent = random.choice([20, 30, 50, 70])
                    st.info(f"**Sponsored Campaign Offer**: {sponsor} needs {required_impressions} impressions for a {discount_percent}% discount. Accept?")
                    
                    accept = st.button(f"Yes, accept {sponsor} offer")
                    decline = st.button("No, keep rolling")
                    
                    if accept:
                        duration_days = random.randint(2, 7)
                        start_date = date.today()
                        end_date = start_date + timedelta(days=duration_days)
                        st.session_state["active_campaign"] = {
                            "sponsor": sponsor,
                            "required_impressions": required_impressions,
                            "discount_percent": discount_percent,
                            "duration_days": duration_days,
                            "start_date": start_date,
                            "end_date": end_date,
                            "beaches": ["Lindos", "Faliraki", "Tsambika"],
                            "materials": f"{sponsor} T-shirts & Banners"
                        }
                        st.success(f"You accepted {sponsor} campaign! Go to 'Campaign Details' tab for more info.")
                    elif decline:
                        st.warning("Declined the campaign.")
                    
                st.session_state["already_offered_campaign"] = True
            
            # Check if finished
            if st.session_state["current_index"] == len(board_squares) - 1:
                st.balloons()
                st.subheader("Journey Completed!")
                st.write(f"**Total NM**: {st.session_state['total_nm_traveled']:.2f}")
                st.write(f"**Ad Score**: {st.session_state['profile']['ad_score']}")
                st.write(f"**Likes**: {st.session_state['profile']['likes']}")
                st.write(f"**Shares**: {st.session_state['profile']['shares']}")
                st.write(f"**Campaigns Joined**: {st.session_state['profile']['campaigns_joined']}")
                
                if st.button("Restart Game"):
                    st.session_state["current_index"] = 0
                    st.session_state["skip_turn"] = False
                    st.session_state["total_nm_traveled"] = 0.0
                    st.session_state["scoreboard"] = []
                    st.session_state["already_offered_campaign"] = False
                    st.session_state["active_campaign"] = None
                    st.session_state["profile"] = {
                        "role": "Passenger",
                        "ad_score": 0,
                        "likes": 0,
                        "shares": 0,
                        "campaigns_joined": 0,
                        "impressions": 0
                    }
                    st.success("Game Restarted!")
    
    # ---- Scoreboard Display ----
    st.markdown("## Scoreboard")
    if len(st.session_state["scoreboard"]) > 0:
        st.dataframe(st.session_state["scoreboard"])
    else:
        st.write("No actions recorded yet.")
