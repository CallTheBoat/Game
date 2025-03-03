import streamlit as st
import random
import math
from datetime import date, timedelta
import folium
from streamlit_folium import st_folium

# ---------- Utility Functions ----------
def haversine_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371.0 * c

def distance_nm(lat1, lon1, lat2, lon2):
    km = haversine_km(lat1, lon1, lat2, lon2)
    return km * 0.539957

# ---------- Session State ----------
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []
if "already_offered" not in st.session_state:
    st.session_state["already_offered"] = False

# Ενεργή χορηγία
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# Βασικό Προφίλ Παίκτη
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "role": "Passenger",
        "ad_score": 0,
        "likes": 0,
        "shares": 0,
        "campaigns_joined": 0,
        "impressions": 0
    }

# ---------- Tabs ----------
tabs = st.tabs(["Board Game", "Sponsor Requirements"])

# ========== TAB 2: Sponsor Requirements ==========
with tabs[1]:
    st.subheader("Sponsor Requirements / Campaign Details")
    sponsor_data = st.session_state["active_sponsor"]
    if sponsor_data is None:
        st.info("No active sponsor campaign.")
    else:
        # Εμφάνιση των απαιτήσεων του χορηγού
        st.success(f"You accepted a sponsor from **{sponsor_data['sponsor_name']}**!")
        st.write(f"**Required Impressions**: {sponsor_data['required_impressions']}")
        st.write(f"**Discount**: {sponsor_data['discount_percent']}%")
        st.write(f"**Duration**: {sponsor_data['duration_days']} days")
        st.write(f"**Dates**: {sponsor_data['start_date']} to {sponsor_data['end_date']}")

        st.markdown("### Sponsor Demands")
        st.write(f"- **Posts/Day**: {sponsor_data['daily_posts']}")
        st.write(f"- **Hours near Popular Beaches**: {sponsor_data['hours_near_beach']} hrs/day")
        st.write(f"- **T-Shirts**: {sponsor_data['tshirts']}")

        st.write("Continue rolling in the Board Game tab while fulfilling these requirements.")

# ========== TAB 1: Board Game ==========
with tabs[0]:
    st.title("Maritime Board Game with Sponsor Offers")

    # Profile
    st.markdown("### Player Profile")
    p = st.session_state["profile"]
    st.write(f"**Role**: {p['role']}")
    st.write(f"**ad_score**: {p['ad_score']}")
    st.write(f"**likes**: {p['likes']}")
    st.write(f"**shares**: {p['shares']}")
    st.write(f"**campaigns_joined**: {p['campaigns_joined']}")
    st.write(f"**impressions**: {p['impressions']}")

    # Route
    route_squares = [
        {"name": "Rhodes Port", "coords": (36.4497, 28.2241), "event": "Start - Explore."},
        {"name": "Ialysos Coast", "coords": (36.4200, 28.1616), "event": "Ad Zone: Potential sponsor."},
        {"name": "Kalithea Beach", "coords": (36.3825, 28.2472), "event": "Calm Waters."},
        {"name": "Faliraki", "coords": (36.3435, 28.2110), "event": "Ad Zone: Potential sponsor."},
        {"name": "Lindos Bay", "coords": (36.0917, 28.0850), "event": "Lose a turn."},
        {"name": "Prasonisi", "coords": (35.8873, 27.7876), "event": "Bonus: Advance 1 square."},
        {"name": "Karpathos", "coords": (35.5077, 27.2139), "event": "Ad Zone: Potential sponsor."},
        {"name": "Finish", "coords": (35.20, 26.90), "event": "End of Journey."}
    ]

    st.write(f"**Current Square**: {route_squares[st.session_state['current_index']]['name']}")
    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")

    # Folium map
    m = folium.Map(location=route_squares[0]["coords"], zoom_start=7)
    for i, sq in enumerate(route_squares):
        folium.Marker(sq["coords"], tooltip=sq["name"], popup=sq["event"]).add_to(m)
    c_coords = route_squares[st.session_state["current_index"]]["coords"]
    folium.Marker(
        c_coords,
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip="Boat Position"
    ).add_to(m)

    st_folium(m, width=700, height=450)

    # Roll dice
    if st.button("Roll the Dice"):
        if st.session_state["skip_turn"]:
            st.warning("You skip this turn!")
            st.session_state["skip_turn"] = False
        else:
            st.session_state["already_offered"] = False
            dice = random.randint(1, 6)
            st.success(f"You rolled a {dice}.")

            old_idx = st.session_state["current_index"]
            new_idx = old_idx + dice
            if new_idx >= len(route_squares):
                new_idx = len(route_squares) - 1

            # Move step by step
            for step in range(old_idx, new_idx):
                c1 = route_squares[step]["coords"]
                c2 = route_squares[step+1]["coords"]
                dist_nm_ = distance_nm(c1[0], c1[1], c2[0], c2[1])
                st.session_state["total_nm"] += dist_nm_
                # Scoreboard
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
            
            # Events
            if "lose a turn" in current_sq["event"].lower():
                st.warning("Lose next turn!")
                st.session_state["skip_turn"] = True
            if "bonus: advance" in current_sq["event"].lower():
                st.success("Bonus: Advance +1 square!")
                bonus_idx = min(new_idx + 1, len(route_squares)-1)
                cA = route_squares[new_idx]["coords"]
                cB = route_squares[bonus_idx]["coords"]
                dist_b = distance_nm(cA[0], cA[1], cB[0], cB[1])
                st.session_state["total_nm"] += dist_b
                st.session_state["current_index"] = bonus_idx
                st.info(f"Now at {route_squares[bonus_idx]['name']}")

            # Ad zone => run ad
            if "ad zone" in current_sq["event"].lower():
                run_ad_btn = st.button("Run Ad")
                if run_ad_btn:
                    st.session_state["profile"]["ad_score"] += 10
                    st.session_state["profile"]["likes"] += 4
                    st.session_state["profile"]["shares"] += 2
                    st.success("Ran Ad: +10 ad_score, +4 likes, +2 shares.")

            # Tυχαία προσφορά
            if not st.session_state["already_offered"]:
                chance = random.random()
                if chance < 0.4:
                    # Company sponsor
                    sponsors = ["Vodafone", "Nike", "Adidas", "Coca-Cola"]
                    sp_name = random.choice(sponsors)
                    req_impr = random.randint(500, 3000)
                    disc = random.choice([20, 30, 50, 70])
                    daily_posts = random.randint(1, 4)
                    hours_beach = random.randint(2, 8)
                    st.info(f"Sponsor Offer: {sp_name} wants {req_impr} impressions for a {disc}% discount. Accept?")

                    accept_btn = st.button(f"Yes, accept {sp_name} offer")
                    decline_btn = st.button("No, ignore")

                    if accept_btn:
                        dur_days = random.randint(3, 7)
                        sd = date.today()
                        ed = sd + timedelta(days=dur_days)
                        st.session_state["active_sponsor"] = {
                            "sponsor_name": sp_name,
                            "required_impressions": req_impr,
                            "discount_percent": disc,
                            "duration_days": dur_days,
                            "start_date": sd,
                            "end_date": ed,
                            "daily_posts": daily_posts,
                            "hours_near_beach": hours_beach,
                            "tshirts": f"{sp_name} T-shirts & Banners"
                        }
                        st.success(f"Accepted sponsor from {sp_name} – check 'Sponsor Requirements' tab!")
                    elif decline_btn:
                        st.warning("Declined sponsor.")

                st.session_state["already_offered"] = True

            # Check if finished
            if st.session_state["current_index"] == len(route_squares) - 1:
                st.subheader("Journey Completed!")
                st.balloons()
                st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")
                st.write(f"**ad_score**: {st.session_state['profile']['ad_score']}")
                st.write(f"**likes**: {st.session_state['profile']['likes']}")
                st.write(f"**shares**: {st.session_state['profile']['shares']}")
                st.write(f"**campaigns_joined**: {st.session_state['profile']['campaigns_joined']}")
                if st.button("Restart Game"):
                    # Reset
                    st.session_state["current_index"] = 0
                    st.session_state["skip_turn"] = False
                    st.session_state["total_nm"] = 0.0
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
