import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ----------- Session State -----------
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

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

# ----------- Tabs -----------
tabs = st.tabs(["Board Game", "Sponsor Requirements"])

# ========== TAB 2: Sponsor Requirements ==========
with tabs[1]:
    st.title("Sponsor Requirements")
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
        st.write(f"- Posts per Day: {sp['daily_posts']}")
        st.write(f"- Hours near Beach per Day: {sp['hours_near_beach']}")
        st.write(f"- Branded Materials: {sp['tshirts']}")
        st.info("Check the Board Game tab to continue playing...")

# ========== TAB 1: Board Game ==========
with tabs[0]:
    st.title("Minimal Board Game Demo")

    # Minimal route squares (two squares only)
    squares = [
        {"name": "Start",  "coords": (36.45, 28.22)},
        {"name": "Finish", "coords": (36.40, 28.15)}
    ]

    st.write(f"**Current Square**: {squares[st.session_state['current_square']]['name']}")

    # Folium map
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

    # Roll Dice (with 2 squares, we just move to finish)
    if st.button("Roll the Dice"):
        if st.session_state["current_square"] == 0:
            st.session_state["current_square"] = 1
            st.success("Moved from Start to Finish!")
        else:
            st.warning("You are already at Finish!")

    # A stable sponsor offer
    st.markdown("## Sponsor Offer")
    st.info("We have a sponsor: Vodafone. Wants 1000 impressions, 50% discount. Accept?")
    yes_btn = st.button("Yes, Accept Vodafone")
    no_btn  = st.button("No, Decline")

    if yes_btn:
        st.session_state["active_sponsor"] = {
            "sponsor_name": "Vodafone",
            "required_impressions": 1000,
            "discount_percent": 50,
            "duration_days": 5,
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=5),
            "daily_posts": 2,
            "hours_near_beach": 4,
            "tshirts": "Vodafone T-shirts & Banners"
        }
        st.success("Accepted sponsor from Vodafone! Check 'Sponsor Requirements' tab.")
    elif no_btn:
        st.warning("Declined sponsor.")

    st.write("Continue playing or go to Sponsor Requirements tab to see the details if accepted.")
