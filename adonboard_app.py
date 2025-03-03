import streamlit as st
import random
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ---------- Utility Functions ----------
def haversine_distance_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c

def distance_nm(lat1, lon1, lat2, lon2):
    km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return km * 0.539957

# ---------- Session State Initialization ----------
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []
if "already_offered" not in st.session_state:
    st.session_state["already_offered"] = False
# Ενεργή χορηγία (None αν δεν έχουμε)
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# Προφίλ παίκτη
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "role": "Passenger",
        "ad_score": 0,
        "likes": 0,
        "shares": 0,
        "campaigns_joined": 0,
        "impressions": 0
    }

# ---------- Define Tabs ----------
tabs = st.tabs(["Board Game", "Sponsor Requirements"])

# ========== TAB 2: Sponsor Requirements ==========
with tabs[1]:
    st.subheader("Sponsor Requirements - Active Campaign")
    sponsor_data = st.session_state["active_sponsor"]
    if sponsor_data is None:
        st.info("No active sponsor campaign at the moment.")
    else:
        # Εμφανίζουμε τις απαιτήσεις της χορηγίας
        st.success(f"Sponsor: {sponsor_data['sponsor_name']}")
        st.write(f"**Required Impressions**: {sponsor_data['required_impressions']}")
        st.write(f"**Discount Offered**: {sponsor_data['discount_percent']}%")
        st.write(f"**Duration**: {sponsor_data['duration_days']} days")
        st.write(f"**Dates**: {sponsor_data['start_date']} → {sponsor_data['end_date']}")
        
        st.markdown("### Sponsor's Demands")
        st.write(f"- **Posts per Day**: {sponsor_data['daily_posts']}")
        st.write(f"- **Hours near Popular Beaches**: {sponsor_data['hours_near_beach']} hrs/day")
        st.write(f"- **Branded T-shirts & Materials**: {sponsor_data['tshirts']}")
        
        st.info("Continue playing in the Board Game tab to gather impressions and fulfill sponsor requirements.")

# ========== TAB 1: BOARD GAME ==========
with tabs[0]:
    st.title("Maritime Board Game with Sponsor Offers")

    # Show player's profile
    p = st.session_state["profile"]
    st.markdown("### Player Profile")
    st.write(f"- **Role**: {p['role']}")
    st.write(f"- **Ad Score**: {p['ad_score']}")
    st.write(f"- **Likes**: {p['likes']}")
    st.write(f"- **Shares**: {p['shares']}")
    st.write(f"- **Campaigns Joined**: {p['campaigns_joined']}")
    st.write(f"- **Impressions**: {p['impressions']}")

    # Define route squares
    route_squares = [
        {"name": "Rhodes Port", "coords": (36.4497, 28.2241), "event": "Start - Explore."},
        {"name": "Ialysos Coast", "coords": (36.4200, 28.1616), "event": "Ad Zone: Potential Sponsor."},
        {"name": "Kalithea Beach", "coords": (36.3825, 28.2472), "event": "Calm Waters."},
        {"name": "Faliraki", "coords": (36.3435, 28.2110), "event": "Ad Zone: Potential Sponsor."},
        {"name": "Lindos Bay", "coords": (36.0917, 28.0850), "event": "Lose a turn."},
        {"name": "Prasonisi", "coords": (35.8873, 27.7876), "event": "Bonus: Advance 1 square."},
        {"name": "Karpathos", "coords": (35.5077, 27.2139), "event": "Ad Zone: Potential Sponsor."},
        {"name": "Finish", "coords": (35.20, 26.90), "event": "End of Journey."}
    ]

    st.write(f"**Current Square**: {route_squares[st.session_state['current_index']]['name']}")
    st.write(f"**Total NM**: {st.session_state['total_nm_traveled']:.2f}")

    # Map with Folium
    m = folium.Map(location=route_squares[0]["coords"], zoom_start=7)
    for i, sq in enumerate(route_squares):
        folium.Marker(
            sq["coords"],
            tooltip=sq["name"],
            popup=sq["event"]
        ).add_to(m)
    current_coord = route_squares[st.session_state["current_index"]]["coords"]
    folium.Marker(
        current_coord,
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip="Boat Position"
    ).add_to(m)
    st_folium(m, width=700, height=450)

    # Roll the Dice
    if st.button("Roll the Dice"):
        if st.session_state["skip_turn"]:
            st.warning("You skip this turn due to an event!")
            st.session_state["skip_turn"] = False
        else:
            st.session_state["already_offered"] = False
            dice_val = random.randint(1, 6)
            st.success(f"You rolled a {dice_val}")

            old_idx = st.session_state["current_index"]
            new_idx = old_idx + dice_val
            if new_idx >= len(route_squares):
                new_idx = len(route_squares) - 1

            # Move step-by-step
            for step in range(old_idx, new_idx):
                c1 = route_squares[step]["coords"]
                c2 = route_squares[step+1]["coords"]
                dist_nm_ = distance_nm(c1[0], c1[1], c2[0], c2[1])
                st.session_state["total_nm_traveled"] += dist_nm_
                # Add to scoreboard
                st.session_state["scoreboard"].append({
                    "Action": f"Moved {route_squares[step]['name']} => {route_squares[step+1]['name']}",
                    "Distance(NM)": round(dist_nm_, 2),
                    "Likes": 0,
                    "Shares": 0,
                    "AdRun?": "No",
                    "Points Gained": 0
                })

            st.session_state["current_index"] = new_idx
            current_sq = route_squares[new_idx]
            st.info(f"Boat arrived at {current_sq['name']}")

            # Check event
            if "lose a turn" in current_sq["event"].lower():
                st.warning("Lose your next turn!")
                st.session_state["skip_turn"] = True
            if "bonus: advance" in current_sq["event"].lower():
                st.success("Bonus: Advance +1 square!")
                bonus_index = min(new_idx + 1, len(route_squares) - 1)
                cA = route_squares[new_idx]["coords"]
                cB = route_squares[bonus_index]["coords"]
                dist_b = distance_nm(cA[0], cA[1], cB[0], cB[1])
                st.session_state["total_nm_traveled"] += dist_b
                st.session_state["current_index"] = bonus_index
                st.info(f"Ended up at {route_squares[bonus_index]['name']} after bonus move.")

            # If it's ad zone, run ad?
            if "ad zone" in current_sq["event"].lower():
                if st.button("Run Ad"):
                    st.session_state["profile"]["ad_score"] += 10
                    st.session_state["profile"]["likes"] += 4
                    st.session_state["profile"]["shares"] += 2
                    st.success("Ran Ad! +10 ad_score, +4 likes, +2 shares.")

            # Random sponsor offer if not offered yet
            if not st.session_state["already_offered"]:
                chance = random.random()
                if chance < 0.4:
                    # Generate sponsor data
                    sponsor_names = ["Vodafone", "Nike", "Adidas", "Coca-Cola"]
                    sp_name = random.choice(sponsor_names)
                    required_impr = random.randint(500, 3000)
                    disc = random.choice([20, 30, 50, 70])
                    daily_posts = random.randint(1, 4)
                    hours_beach = random.randint(2, 8)

                    st.info(f"Sponsor Offer: {sp_name} wants {required_impr} impressions for a {disc}% discount. Accept?")
                    accept_btn = st.button(f"Yes, accept {sp_name} offer")
                    decline_btn = st.button("No, decline offer")

                    if accept_btn:
                        dur_days = random.randint(3, 7)
                        startD = date.today()
                        endD = startD + timedelta(days=dur_days)
                        st.session_state["active_sponsor"] = {
                            "sponsor_name": sp_name,
                            "required_impressions": required_impr,
                            "discount_percent": disc,
                            "duration_days": dur_days,
                            "start_date": startD,
                            "end_date": endD,
                            "daily_posts": daily_posts,
                            "hours_near_beach": hours_beach,
                            "tshirts": f"{sp_name} T-shirts & Banners"
                        }
                        st.success(f"You accepted {sp_name}'s sponsorship! Go to the 'Sponsor Requirements' tab.")
                    elif decline_btn:
                        st.warning("Declined sponsor offer.")

                st.session_state["already_offered"] = True

            # Check if finished
            if st.session_state["current_index"] == len(route_squares) - 1:
                st.balloons()
                st.subheader("Journey Completed!")
                st.write(f"**Total NM**: {st.session_state['total_nm_traveled']:.2f}")
                st.write(f"**ad_score**: {st.session_state['profile']['ad_score']}")
                st.write(f"**likes**: {st.session_state['profile']['likes']}")
                st.write(f"**shares**: {st.session_state['profile']['shares']}")
                st.write(f"**campaigns_joined**: {st.session_state['profile']['campaigns_joined']}")
                if st.button("Restart Game"):
                    st.session_state["current_index"] = 0
                    st.session_state["skip_turn"] = False
                    st.session_state["total_nm_traveled"] = 0.0
                    st.session_state["scoreboard"] = []
                    st.session_state["already_offered"] = False
                    st.session_state["active_sponsor"] = None
                    st.session_state["profile"] = {
                        "role": "Passenger",
                        "ad_score": 0,
                        "likes": 0,
                        "shares": 0,
                        "campaigns_joined": 0,
                        "impressions": 0
                    }
                    st.success("Game restarted!")

    st.markdown("## Scoreboard")
    if len(st.session_state["scoreboard"]) == 0:
        st.write("No moves yet.")
    else:
        st.dataframe(st.session_state["scoreboard"])
