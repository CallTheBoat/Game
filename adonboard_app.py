import streamlit as st
import random
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ---------- Utility: minimal distance -----------
def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# ---------- Session State -----------
if "current_square" not in st.session_state:
    st.session_state["current_square"] = 0

if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "role": "Passenger",
        "ad_score": 0,
        "likes": 0,
        "shares": 0,
        "campaigns_joined": 0,
        "impressions": 0
    }

if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None  # dict with sponsor details

if "sponsor_approval" not in st.session_state:
    st.session_state["sponsor_approval"] = None  # "Approved" or "Rejected" or None

if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

# ---------- Create Tabs -----------
tabs = st.tabs(["Board Game", "Sponsor Requirements"])

# ========== TAB 2: Sponsor Requirements ==========
with tabs[1]:
    st.title("Sponsor Requirements")
    
    # Εάν δεν υπάρχει καμπάνια, δεν εμφανίζει τίποτα
    if st.session_state["active_sponsor"] is None:
        st.info("No active sponsor campaign.")
    else:
        sp = st.session_state["active_sponsor"]
        st.success(f"Sponsor: {sp['sponsor_name']}")
        st.write(f"**Required Impressions**: {sp['required_impressions']}")
        st.write(f"**Discount**: {sp['discount_percent']}% off boat costs")
        st.write(f"**Duration**: {sp['duration_days']} days")
        st.write(f"**Dates**: {sp['start_date']} → {sp['end_date']}")

        st.markdown("### Sponsor Demands")
        st.write(f"- **Posts per Day**: {sp['daily_posts']}")
        st.write(f"- **Hours near Popular Beaches**: {sp['hours_near_beach']} / day")
        st.write(f"- **Branded Materials**: {sp['tshirts']}")

        # Επιπλέον κουμπί: "Send my Profile to Sponsor"
        st.markdown("### Send Profile to Sponsor?")
        send_btn = st.button("Send my Profile to Sponsor")
        if send_btn:
            # Τυχαία πιθανότητα έγκρισης/απόρριψης
            approve_chance = random.random()
            if approve_chance < 0.6:
                st.session_state["sponsor_approval"] = "Approved"
                st.success("Sponsor has APPROVED your profile! Congrats!")
            else:
                st.session_state["sponsor_approval"] = "Rejected"
                st.error("Sponsor has REJECTED your profile. Sorry!")
        
        # Εμφάνιση αν έχουμε ήδη approval/rejection
        if st.session_state["sponsor_approval"] == "Approved":
            st.success("Your profile is ALREADY APPROVED by sponsor!")
        elif st.session_state["sponsor_approval"] == "Rejected":
            st.error("Your profile was REJECTED by sponsor.")

# ========== TAB 1: Board Game ==========
with tabs[0]:
    st.title("Minimal Board Game with Sponsor Demo")

    # Route squares (2 squares)
    squares = [
        {"name": "Start", "coords": (36.45, 28.22)},
        {"name": "Finish", "coords": (36.40, 28.15)}
    ]
    
    st.write(f"**Current Square**: {squares[st.session_state['current_square']]['name']}")
    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")

    # Map
    m = folium.Map(location=squares[0]["coords"], zoom_start=7)
    for sq in squares:
        folium.Marker(sq["coords"], tooltip=sq["name"]).add_to(m)
    folium.Marker(
        squares[st.session_state["current_square"]]["coords"],
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip="Boat Position"
    ).add_to(m)
    st_folium(m, width=700, height=450)

    # Profile
    st.markdown("### Player Profile")
    pr = st.session_state["profile"]
    st.write(f"- Role: {pr['role']}")
    st.write(f"- ad_score: {pr['ad_score']}")
    st.write(f"- likes: {pr['likes']}")
    st.write(f"- shares: {pr['shares']}")
    st.write(f"- campaigns_joined: {pr['campaigns_joined']}")
    st.write(f"- impressions: {pr['impressions']}")

    # Roll Dice
    if st.button("Roll the Dice"):
        if st.session_state["current_square"] == 0:
            # move to Finish
            c1 = squares[0]["coords"]
            c2 = squares[1]["coords"]
            distnm = distance_nm(c1[0], c1[1], c2[0], c2[1])
            st.session_state["total_nm"] += distnm
            st.session_state["current_square"] = 1
            st.success("Moved from Start to Finish!")
        else:
            st.warning("Already at Finish!")

    # Sponsor Offer
    st.markdown("### Sponsor Offer")
    st.info("Sponsor: 'Vodafone' wants 1000 impressions, 50% discount. Accept?")
    accept_btn = st.button("Yes, Accept Sponsor")
    decline_btn = st.button("No, Decline Sponsor")

    if accept_btn:
        # Δημιουργούμε τη χορηγία
        dur_days = 5
        startD = date.today()
        endD = startD + timedelta(days=dur_days)
        st.session_state["active_sponsor"] = {
            "sponsor_name": "Vodafone",
            "required_impressions": 1000,
            "discount_percent": 50,
            "duration_days": dur_days,
            "start_date": startD,
            "end_date": endD,
            "daily_posts": 2,
            "hours_near_beach": 4,
            "tshirts": "Vodafone T-shirts & Banners"
        }
        # Reset sponsor_approval
        st.session_state["sponsor_approval"] = None
        st.success("Accepted sponsor from Vodafone! Go to 'Sponsor Requirements' tab to see details.")
    elif decline_btn:
        st.warning("Declined sponsor offer.")

    st.markdown("Continue or check the second tab.")
