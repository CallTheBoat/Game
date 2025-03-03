import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ---------------- Utility for minimal distance ----------------
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

# ---------------- Initialize Session State ----------------
if "current_square" not in st.session_state:
    st.session_state["current_square"] = 0

if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "role": "Passenger",
        "ad_score": 0,
        "likes": 10,      # Π.χ. ο παίκτης έχει 10 likes
        "shares": 5,
        "campaigns_joined": 0,
        "impressions": 200
    }

# Ενεργή χορηγία (None αν δεν έχει δεχτεί)
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# Έχει στείλει ο επιβάτης το προφίλ του στον χορηγό;
if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False

# Απόφαση χορηγού (None = pending, "Approved" ή "Rejected")
if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None

# Συνολική απόσταση
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0


# ---------------- Tabs ----------------
tabs = st.tabs(["Board Game", "Sponsor Requirements", "Sponsor Admin"])

# ========== TAB 3: Sponsor Admin ========== 
with tabs[2]:
    st.title("Sponsor Admin Page")
    st.info("This tab simulates the 'Sponsor' role, who sees the passenger's profile request if it was sent.")
    
    # Αν δεν υπάρχει ενεργή χορηγία, απλώς γράφουμε μήνυμα
    if st.session_state["active_sponsor"] is None:
        st.warning("No active sponsor campaign. The passenger has not accepted any sponsor yet.")
    else:
        sponsor = st.session_state["active_sponsor"]
        st.success(f"Sponsor: {sponsor['sponsor_name']} is waiting for the passenger's profile (if sent).")
        
        # Αν ο passenger έστειλε το προφίλ
        if st.session_state["profile_sent"]:
            st.markdown("### Passenger's Profile for Review")
            p = st.session_state["profile"]
            st.write(f"- Role: {p['role']}")
            st.write(f"- ad_score: {p['ad_score']}")
            st.write(f"- likes: {p['likes']}")
            st.write(f"- shares: {p['shares']}")
            st.write(f"- campaigns_joined: {p['campaigns_joined']}")
            st.write(f"- impressions: {p['impressions']}")
            
            st.markdown("Decision:")
            approve_btn = st.button("Approve Passenger")
            reject_btn  = st.button("Reject Passenger")
            
            if approve_btn:
                st.session_state["sponsor_decision"] = "Approved"
                st.success("You (Sponsor) approved this passenger's profile!")
            elif reject_btn:
                st.session_state["sponsor_decision"] = "Rejected"
                st.error("You (Sponsor) rejected this passenger's profile.")
        else:
            st.info("Passenger has NOT sent their profile yet (profile_sent = False). Nothing to review.")


# ========== TAB 2: Sponsor Requirements (for the passenger) ==========
with tabs[1]:
    st.title("Sponsor Requirements (Passenger View)")
    
    # Αν δεν υπάρχει καμπάνια => κενό
    if st.session_state["active_sponsor"] is None:
        st.info("No active sponsor campaign right now.")
    else:
        sp = st.session_state["active_sponsor"]
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"**Required Impressions**: {sp['required_impressions']}")
        st.write(f"**Discount**: {sp['discount_percent']}% discount")
        st.write(f"**Duration**: {sp['duration_days']} days ({sp['start_date']} to {sp['end_date']})")
        st.markdown("### Sponsor Demands")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near busy beaches daily")
        st.write(f"- Materials: {sp['tshirts']}")
        
        # Αν ο passenger έστειλε ήδη το προφίλ => δείχνουμε status
        if st.session_state["profile_sent"]:
            st.info("You have already sent your profile to the sponsor.")
            
            # Αν έχουμε απόφαση
            decision = st.session_state["sponsor_decision"]
            if decision == "Approved":
                st.success("Sponsor has APPROVED your profile! Congrats!")
            elif decision == "Rejected":
                st.error("Sponsor has REJECTED your profile. Sorry!")
            else:
                st.warning("Waiting for sponsor to decide (pending).")
        else:
            st.markdown("### Send your profile to the sponsor?")
            send_btn = st.button("Send My Profile to Sponsor")
            if send_btn:
                st.session_state["profile_sent"] = True
                st.session_state["sponsor_decision"] = None
                st.success("Profile sent to sponsor! Check the Sponsor Admin tab for the sponsor's decision.")


# ========== TAB 1: Board Game (Passenger) ==========
with tabs[0]:
    st.title("Board Game - Minimal Demo")
    
    squares = [
        {"name": "Start",  "coords": (36.45, 28.22)},
        {"name": "Finish", "coords": (36.40, 28.15)}
    ]
    
    st.write(f"**Current Square**: {squares[st.session_state['current_square']]['name']}")
    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")
    
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
    
    # Minimal profile view
    st.markdown("### Player Profile (Quick View)")
    p = st.session_state["profile"]
    st.write(f"- ad_score: {p['ad_score']}, likes: {p['likes']}, shares: {p['shares']}, impressions: {p['impressions']}")
    
    # Roll the Dice => move from Start to Finish
    if st.button("Roll the Dice"):
        if st.session_state["current_square"] == 0:
            st.session_state["current_square"] = 1
            c1 = squares[0]["coords"]
            c2 = squares[1]["coords"]
            distnm = distance_nm(c1[0], c1[1], c2[0], c2[1])
            st.session_state["total_nm"] += distnm
            st.success("Moved from Start to Finish!")
        else:
            st.warning("Already at Finish.")
    
    # Σταθερή προσφορά χορηγού
    st.markdown("### Sponsor Offer")
    st.info("Sponsor: 'Vodafone' wants 1000 impressions, 50% discount. Accept?")
    accept_btn = st.button("Yes, Accept Sponsor")
    decline_btn = st.button("No, Decline Sponsor")
    
    if accept_btn:
        dur_days = 5
        startD = date.today()
        endD   = startD + timedelta(days=dur_days)
        st.session_state["active_sponsor"] = {
            "sponsor_name": "Vodafone",
            "required_impressions": 1000,
            "discount_percent": 50,
            "duration_days": dur_days,
            "start_date": startD,
            "end_date": endD,
            "daily_posts": 2,
            "hours_near_beach": 4,
            "tshirts": "Vodafone T-Shirts & Banners"
        }
        # Reset to pending
        st.session_state["profile_sent"]     = False
        st.session_state["sponsor_decision"] = None
        
        st.success("You accepted the 'Vodafone' sponsor. Check 'Sponsor Requirements' tab for details.")
    elif decline_btn:
        st.warning("Declined the sponsor.")


    # If we are at Finish => show short summary
    if st.session_state["current_square"] == 1:
        st.balloons()
        st.subheader("Journey Completed!")
        if st.button("Restart Game"):
            # Reset everything
            st.session_state["current_square"] = 0
            st.session_state["total_nm"]       = 0.0
            st.session_state["active_sponsor"] = None
            st.session_state["profile_sent"]   = False
            st.session_state["sponsor_decision"] = None
            st.session_state["profile"] = {
                "role": "Passenger",
                "ad_score": 0,
                "likes": 10,
                "shares": 5,
                "campaigns_joined": 0,
                "impressions": 200
            }
            st.success("Restarted everything!")
