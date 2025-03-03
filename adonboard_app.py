import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# -------------- Minimal Utility for Distance --------------
def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lat2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# -------------- Session State Initialization --------------
# 1) Profile
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "facebook_friends": 0,
        "instagram_followers": 0,
        "adonboard_friends": 0
    }

# 2) Active Sponsor
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# 3) Board Game
if "current_square" not in st.session_state:
    st.session_state["current_square"] = 0
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

# 4) Profile Sent?
if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False

# 5) Sponsor Decision: "Approved", "Rejected", or None
if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None

# 6) Final acceptance by passenger (Yes/No/Think)
if "final_campaign_decision" not in st.session_state:
    st.session_state["final_campaign_decision"] = None  # "Yes", "No", or "Think" or None

# -------------- Tabs (4) --------------
tabs = st.tabs([
    "1. Profile Setup",
    "2. Board Game",
    "3. Sponsor Requirements",
    "4. Sponsor Admin"
])

# ========== TAB 1: Profile Setup ==========
with tabs[0]:
    st.title("Profile Setup (Passenger)")
    st.info("Fill in your details so the Sponsor can see them later.")

    with st.form("passenger_profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        
        st.session_state["profile"]["facebook_friends"] = st.number_input(
            "Facebook Friends", 
            min_value=0, 
            value=st.session_state["profile"]["facebook_friends"]
        )
        st.session_state["profile"]["instagram_followers"] = st.number_input(
            "Instagram Followers", 
            min_value=0, 
            value=st.session_state["profile"]["instagram_followers"]
        )
        st.session_state["profile"]["adonboard_friends"] = st.number_input(
            "AdOnBoard Friends",
            min_value=0,
            value=st.session_state["profile"]["adonboard_friends"]
        )
        
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.success("Profile saved! Go to 'Board Game' tab to continue.")


# ========== TAB 2: Board Game ==========
with tabs[1]:
    st.title("Board Game (Passenger)")

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
    
    st.markdown("### Sponsor Offer")
    st.info("Sponsor: 'Vodafone' wants 1000 impressions, 50% discount. Accept or Decline?")
    accept_btn = st.button("Yes, Accept Sponsor")
    decline_btn = st.button("No, Decline Sponsor")

    if accept_btn:
        dur_days = 5
        start_d = date.today()
        end_d   = start_d + timedelta(days=dur_days)
        st.session_state["active_sponsor"] = {
            "sponsor_name": "Vodafone",
            "required_impressions": 1000,
            "discount_percent": 50,
            "duration_days": dur_days,
            "start_date": start_d,
            "end_date": end_d,
            "daily_posts": 2,
            "hours_near_beach": 4,
            "tshirts": "Vodafone T-Shirts & Banners"
        }
        st.session_state["profile_sent"]        = False
        st.session_state["sponsor_decision"]    = None
        st.session_state["final_campaign_decision"] = None
        st.success("Sponsor accepted. Check sponsor's demands below or go to tab 3.")
    elif decline_btn:
        st.warning("Declined sponsor.")
        st.session_state["active_sponsor"] = None
        st.session_state["profile_sent"]   = False
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None

    # Αν υπάρχει ενεργό sponsor => δείχνουμε τι ζητάει
    if st.session_state["active_sponsor"] is not None:
        sp = st.session_state["active_sponsor"]
        st.markdown("### Sponsor Requirements")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} to {sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if st.session_state["profile_sent"]:
            st.warning("Profile already sent to Sponsor. Waiting for Sponsor's decision.")
        else:
            if st.button("Send My Profile to Sponsor"):
                st.session_state["profile_sent"] = True
                st.session_state["sponsor_decision"] = None
                st.session_state["final_campaign_decision"] = None
                st.success("Profile sent! The sponsor sees it in 'Sponsor Admin' tab.")
    
    if st.session_state["current_square"] == 1:
        st.subheader("Journey Completed!")
        if st.button("Restart Game"):
            st.session_state["current_square"] = 0
            st.session_state["total_nm"]       = 0.0
            st.session_state["active_sponsor"] = None
            st.session_state["profile_sent"]   = False
            st.session_state["sponsor_decision"] = None
            st.session_state["final_campaign_decision"] = None
            st.success("Game restarted!")


# ========== TAB 3: Sponsor Requirements (Passenger) ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor. Accept one in 'Board Game' tab.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        # Έλεγχος sponsor_decision
        dec = st.session_state["sponsor_decision"]
        if not st.session_state["profile_sent"]:
            st.warning("You haven't sent your profile yet to the sponsor. Go to Board Game tab.")
        else:
            if dec is None:
                st.info("Waiting for sponsor to Approve or Reject your profile (Tab 4).")
            elif dec == "Rejected":
                st.error("Sponsor has REJECTED your profile.")
            elif dec == "Approved":
                st.success("Sponsor has APPROVED your profile!")
                st.markdown("#### Do you finally accept the sponsor's final campaign? Choose one:")
                
                final_dec = st.session_state["final_campaign_decision"]
                if final_dec == "Yes":
                    st.success("You have FINALLY accepted the sponsor's campaign! Congrats!")
                elif final_dec == "No":
                    st.warning("You have declined the final campaign. No sponsor for you.")
                elif final_dec == "Think":
                    st.info("You're still thinking about it…")
                else:
                    yes_btn = st.button("Yes, I accept the final campaign")
                    no_btn  = st.button("No, I refuse the final campaign")
                    think_btn = st.button("I Will Think About It")
                    if yes_btn:
                        st.session_state["final_campaign_decision"] = "Yes"
                        st.success("You have FINALLY accepted the sponsor's campaign! Congrats!")
                    elif no_btn:
                        st.session_state["final_campaign_decision"] = "No"
                        st.warning("You have refused the final campaign. Maybe next time.")
                    elif think_btn:
                        st.session_state["final_campaign_decision"] = "Think"
                        st.info("You're still thinking…")


# ========== TAB 4: Sponsor Admin ========== 
with tabs[3]:
    st.title("Sponsor Admin Page")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.warning("No sponsor campaign accepted by passenger yet.")
    else:
        st.success(f"Sponsor: {sp['sponsor_name']} is active.")
        
        if not st.session_state["profile_sent"]:
            st.info("Passenger has NOT sent their profile yet.")
        else:
            # Show passenger profile data
            st.markdown("### Passenger's Profile")
            prof = st.session_state["profile"]
            st.write(f"- Name: {prof['name']}")
            st.write(f"- Surname: {prof['surname']}")
            st.write(f"- Age: {prof['age']}")
            st.write(f"- Facebook Friends: {prof['facebook_friends']}")
            st.write(f"- Instagram Followers: {prof['instagram_followers']}")
            st.write(f"- AdOnBoard Friends: {prof['adonboard_friends']}")

            st.markdown("#### Decision")
            dec = st.session_state["sponsor_decision"]
            if dec == "Approved":
                st.success("You have ALREADY Approved this passenger.")
            elif dec == "Rejected":
                st.error("You have Rejected this passenger.")
            else:
                approve_btn = st.button("Approve Passenger")
                reject_btn  = st.button("Reject Passenger")
                if approve_btn:
                    st.session_state["sponsor_decision"] = "Approved"
                    st.success("Passenger Approved!")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")
