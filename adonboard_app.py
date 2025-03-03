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
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371.0 * c

def distance_nm(lat1, lon1, lat2, lon2):
    """Υπολογίζει απόσταση σε Ναυτικά Μίλια μεταξύ δύο συντεταγμένων."""
    km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return km * 0.539957

# ---------- Session State Initialization ----------
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "skip_turn" not in st.session_state:
    st.session_state["skip_turn"] = False
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = []

# Ενεργή χορηγία (None αν δεν έχει δεχτεί κάποια)
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

# ---------- Ορισμός 2 Καρτελών (Board Game & Sponsor Requirements) ----------
tabs = st.tabs(["Board Game", "Sponsor Requirements"])

# ========== TAB 2: "Sponsor Requirements" ==========
with tabs[1]:
    st.subheader("Sponsor Requirements - Active Campaign")
    sponsor = st.session_state["active_sponsor"]
    if sponsor is None:
        st.info("No active sponsor campaign at the moment.")
    else:
        st.success(f"**Sponsor**: {sponsor['sponsor_name']}")
        st.write(f"**Required Impressions**: {sponsor['required_impressions']}")
        st.write(f"**Discount**: {sponsor['discount_percent']}%")
        st.write(f"**Duration**: {sponsor['duration_days']} days")
        st.write(f"**Dates**: {sponsor['start_date']} → {sponsor['end_date']}")
        st.markdown("### Sponsor's Demands")
        st.write(f"- **Posts per Day**: {sponsor['daily_posts']}")
        st.write(f"- **Hours near Beaches**: {sponsor['hours_near_beach']} hrs/day")
        st.write(f"- **Promo Materials**: {sponsor['tshirts']}")
        st.info("Keep playing in the Board Game tab to gather impressions / fulfill sponsor demands.")

# ========== TAB 1: "Board Game" ==========
with tabs[0]:
    st.title("Maritime Board Game (Sponsor Demo)")

    # ----- Προφίλ Παίκτη -----
    st.markdown("### Player Profile")
    prof = st.session_state["profile"]
    st.write(f"- Role: {prof['role']}")
    st.write(f"- ad_score: {prof['ad_score']}")
    st
