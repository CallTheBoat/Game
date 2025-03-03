import streamlit as st
import random
import math
from datetime import date, timedelta
import folium
from streamlit_folium import st_folium

# ========== Βοηθητικές Συναρτήσεις ==========
def haversine_distance_km(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c

def distance_nm(lat1, lon1, lat2, lon2):
    """Υπολογίζει απόσταση σε Ναυτικά Μίλια μεταξύ δύο σημείων."""
    km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return km * 0.539957

# ========== Session State ==========
# Δείκτης πλοίου
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0

# Skip turn
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False

# Συνολικά NM που έχουμε διανύσει
if "total_nm_traveled" not in st.session_state:
    st.session_state["total_nm_traveled"] = 0.0

# Scoreboard (λίστα από dict)
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []

# Για να μην εμφανίζεται δεύτερη φορά η χορηγία στην ίδια ρίψη
if "already_offered" not in st.session_state:
    st.session_state["already_offered"] = False

# Ενεργή χορηγία/καμπάνια
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# Βασικές μετρικές παίκτη
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "role": "Passenger",
        "ad_score": 0,
        "likes": 0,
        "shares": 0,
        "campaigns_joined": 0,
        "impressions": 0
    }

# ========== Δημιουργία Δύο Καρτελών ==========
tabs = st.tabs(["Board Game", "Sponsor Requirements"])

# ========== TAB 2: "Sponsor Requirements" ==========
with tabs[1]:
    st.subheader("Sponsor Requirements")
    if st.session_state["active_sponsor"] is None:
        st.info("No active sponsor campaign yet.")
    else:
        sponsor_data = st.session_state["active_sponsor"]
        st.success(f"You accepted a sponsor from {sponsor_data['sponsor_name']}!")
        st.write(f"**Required Impressions**: {sponsor_data['required_impressions']}")
        st.write(f"**Discount**: {sponsor_data['discount_percent']}% on boat costs")
        st.write(f"**Duration**: {sponsor_data['duration_days']} days")
        st.write(f"**Dates**: {sponsor_data['start_date']} to {sponsor_data['end_date']}")
        st.write(f"**Daily Posts**: {sponsor_data['daily_posts']} (photos, stories, etc.)")
        st.write(f"**Hours near Popular Beaches**: {sponsor_data['hours_near_beach']} hours/day")
        st.write(f"**Branded T-shirts**: {sponsor_data['tshirts']}")
        st.info("You can continue rolling the dice in the Board Game tab.")

# ========== TAB 1: "Board Game" ==========
with tabs[0]:
    st.title("Maritime Board Game (Sponsor Offers)")

    # ---------- Εμφάνιση Προφίλ ----------
    st.markdown("### Player Profile")
    prof = st.session_state["profile"]
    st.write(f"**Role:** {prof['role']}")
    st.write(f"**Ad Score:** {prof['ad_score']}")
    st.write(f"**Likes:** {prof['likes']}")
    st.write(f"**Shares:** {prof['shares']}")
    st.write(f"**Campaigns Joined:** {prof['campaigns_joined']}")
    st.write(f"**Impressions:** {prof['impressions']}")

    # ---------- Ορισμός Διαδρομής (8-10 στάσεις) ----------
    route_squares = [
        {"name": "Rhodes Port", "coords": (36.4497, 28.2241), "event": "Start Point"},
        {"name": "Ialysos Coast", "coords": (36.4200, 28.1616), "event": "Ad Zone: Potential Sponsor"},
        {"name": "Kalithea Beach", "coords": (36.3825, 28.2472), "event": "Calm Waters."},
        {"name": "Faliraki", "coords": (36.3435, 28.2110), "event": "Ad Zone: Potential Sponsor"},
        {"name": "Lindos Bay", "coords": (36.0917, 28.0850), "event": "Lose a turn"},
        {"name": "Prasonisi", "coords": (35.8873, 27.7876), "event": "Bonus: Advance 1 square"},
        {"name": "Karpathos", "coords": (35.5077, 27.2139), "event": "Ad Zone: Potential Sponsor"},
        {"name": "Finish", "coords": (35.00, 26.90), "event": "End of Journey"}
    ]

    st.write(f"**Current Position**: {route_squares[st.session_state['current_index']]['name']}")
    st.write(f"**Total NM Traveled**: {st.session_state['total_nm_traveled']:.2f}")

    # ---------- Δημιουργία Χάρτη με Folium ----------
    m = folium.Map(location=route_squares[0]["coords"], zoom_start=7)
    for i, sq in enumerate(route_squares):
        folium.Marker(
            sq["coords"],
            tooltip=sq["name"],
            popup=sq["event"]
        ).add_to(m)
    currentC = route_squares[st.session_state["current_index"]]["coords"]
    folium.Marker(
        currentC,
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip="Current Boat Position"
    ).add_to(m)
    st_folium(m, width=700, height=450)

    # ---------- Roll the Dice Button ----------
    if st.button("Roll the Dice"):
        if st.session_state["skip_turn"]:
            st.warning("You skip this turn due to a previous event!")
            st.session_state["skip_turn"] = False
        else:
            st.session_state["already_offered"] = False
            dice_val = random.randint(1, 6)
            st.success(f"You rolled a {dice_val}.")

            old_index = st.session_state["current_index"]
            new_index = old_index + dice_val
            if new_index >= len(route_squares):
                new_index = len(route_squares) - 1

            # Βήμα-βήμα κίνηση
            for step in range(old_index, new_index):
                c1 = route_squares[step]["coords"]
                c2 = route_squares[step+1]["coords"]
                distnm = distance_nm(c1[0], c1[1], c2[0], c2[1])
                st.session_state["total_nm_traveled"] += distnm
                # Scoreboard entry
                st.session_state["scoreboard"].append({
                    "Action": f"Moved from {route_squares[step]['name']} to {route_squares[step+1]['name']}",
                    "Distance(NM)": round(distnm, 2),
                    "Likes": 0,
                    "Shares": 0,
                    "AdRun?": "No",
                    "Points Gained": 0
                })

            st.session_state["current_index"] = new_index
            new_sq = route_squares[new_index]
            st.info(f"Boat arrived at {new_sq['name']}.")
            
            # Check event
            if "lose a turn" in new_sq["event"].lower():
                st.warning("Event: Lose a turn!")
                st.session_state["skip_turn"] = True
            if "bonus: advance" in new_sq["event"].lower():
                st.success("Bonus: Advance +1 square!")
                bonus_idx = min(new_index + 1, len(route_squares) - 1)
                cA = route_squares[new_index]["coords"]
                cB = route_squares[bonus_idx]["coords"]
                distNM2 = distance_nm(cA[0], cA[1], cB[0], cB[1])
                st.session_state["total_nm_traveled"] += distNM2
                st.session_state["current_index"] = bonus_idx
                st.info(f"Ended up at {route_squares[bonus_idx]['name']} after bonus move.")

            # Ad zone => maybe run an ad
            if "ad zone" in new_sq["event"].lower():
                if st.button("Run Ad"):
                    st.session_state["profile"]["ad_score"] += 10
                    st.session_state["profile"]["likes"] += 5
                    st.session_state["profile"]["shares"] += 3
                    st.success("Ran an Ad: +10 ad_score, +5 likes, +3 shares.")

            # Τυχαία πιθανότητα να εμφανιστεί προσφορά
            if not st.session_state["already_offered"]:
                # Π.χ. 40% πιθανότητα
                chance = random.random()
                if chance < 0.4:
                    sponsor_list = ["Vodafone", "Nike", "Coca-Cola", "Adidas"]
                    sponsor_name = random.choice(sponsor_list)
                    needed_impressions = random.randint(500, 3000)
                    disc = random.choice([20, 30, 50, 60, 70])
                    daily_posts = random.randint(1, 3)
                    hours_beach = random.randint(2, 8)
                    st.info(f"Sponsor Offer: {sponsor_name} wants {needed_impressions} impressions for a {disc}% discount. Accept?")

                    yes_button = st.button(f"Yes, accept {sponsor_name} offer")
                    no_button = st.button("No, ignore sponsor")

                    if yes_button:
                        dur_days = random.randint(3, 7)
                        startD = date.today()
                        endD = startD + timedelta(days=dur_days)
                        st.session_state["active_sponsor"] = {
                            "sponsor_name": sponsor_name,
                            "required_impressions": needed_impressions,
                            "discount_percent": disc,
                            "duration_days": dur_days,
                            "start_date": startD,
                            "end_date": endD,
                            "daily_posts": daily_posts,
                            "hours_near_beach": hours_beach,
                            "tshirts": f"T-shirts with {sponsor_name} logo",
                        }
                        st.success(f"You accepted the {sponsor_name} campaign. Check 'Sponsor Requirements' tab!")
                    elif no_button:
                        st.warning("You declined the sponsor offer.")

                st.session_state["already_offered"] = True

            # Check if end
            if st.session_state["current_index"] == len(route_squares) - 1:
                st.balloons()
                st.subheader("Journey Completed!")
                st.write(f"**Total NM**: {st.session_state['total_nm_traveled']:.2f}")
                st.write(f"**Ad Score**: {st.session_state['profile']['ad_score']}")
                st.write(f"**Likes**: {st.session_state['profile']['likes']}")
                st.write(f"**Shares**: {st.session_state['profile']['shares']}")
                st.write(f"**Campaigns Joined**: {st.session_state['profile']['campaigns_joined']}")
                
                if st.button("Restart Game"):
                    # Reset session state
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
                    st.success("Game Restarted!")

    st.markdown("## Scoreboard")
    if len(st.session_state["scoreboard"]) == 0:
        st.write("No moves recorded.")
    else:
        st.dataframe(st.session_state["scoreboard"])
