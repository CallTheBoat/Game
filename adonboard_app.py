import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# -------------- Minimal distance function --------------
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

# -------------- Session State --------------
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "facebook_friends": 0,
        "instagram_followers": 0,
        "adonboard_friends": 0
    }

if "passenger_game_stats" not in st.session_state:
    # Περιέχει μετρικές σχετικά με ad_score, likes, shares, κλπ.
    st.session_state["passenger_game_stats"] = {
        "ad_score": 0,
        "likes": 0,
        "shares": 0,
        "campaigns_joined": 0,
        "impressions": 0
    }

if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

if "current_square" not in st.session_state:
    st.session_state["current_square"] = 0

if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

# profile_sent = έχει στείλει ο επιβάτης το προφίλ στον sponsor;
if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False

# sponsor_decision = "Approved", "Rejected", ή None
if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None

# -------------- Tabs: 4 --------------
tabs = st.tabs(["1. Profile Setup", "2. Board Game", "3. Sponsor Requirements", "4. Sponsor Admin"])

# ========== TAB 1: Profile Setup ==========
with tabs[0]:
    st.title("Profile Setup (Passenger)")
    st.info("Fill in your personal details here. Then go to 'Board Game' tab.")
    
    # Απλή φόρμα για τα στοιχεία προφίλ
    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        
        st.session_state["profile"]["facebook_friends"] = st.number_input("Facebook Friends", min_value=0, value=st.session_state["profile"]["facebook_friends"])
        st.session_state["profile"]["instagram_followers"] = st.number_input("Instagram Followers", min_value=0, value=st.session_state["profile"]["instagram_followers"])
        st.session_state["profile"]["adonboard_friends"] = st.number_input("AdOnBoard Friends", min_value=0, value=st.session_state["profile"]["adonboard_friends"])
        
        submit_btn = st.form_submit_button("Save Profile")
        if submit_btn:
            st.success("Profile saved successfully! Now go to 'Board Game' tab.")

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

    # Minimal passenger stats (Game stats)
    pstats = st.session_state["passenger_game_stats"]
    st.markdown("### Passenger's Game Stats")
    st.write(f"- ad_score: {pstats['ad_score']}")
    st.write(f"- likes: {pstats['likes']}")
    st.write(f"- shares: {pstats['shares']}")
    st.write(f"- campaigns_joined: {pstats['campaigns_joined']}")
    st.write(f"- impressions: {pstats['impressions']}")

    # Roll the Dice => move from Start to Finish
    if st.button("Roll the Dice"):
        if st.session_state["current_square"] == 0:
            st.session_state["current_square"] = 1
            # Count distance
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
        today = date.today()
        end_day = today + timedelta(days=dur_days)
        
        st.session_state["active_sponsor"] = {
            "sponsor_name": "Vodafone",
            "required_impressions": 1000,
            "discount_percent": 50,
            "duration_days": dur_days,
            "start_date": today,
            "end_date": end_day,
            "daily_posts": 2,
            "hours_near_beach": 4,
            "tshirts": "Vodafone T-shirts & Banners"
        }
        # Reset so sponsor can reevaluate
        st.session_state["profile_sent"]    = False
        st.session_state["sponsor_decision"] = None
        
        st.success("You accepted the sponsor. Now go to 'Sponsor Requirements' tab for demands.")
    elif decline_btn:
        st.warning("Declined sponsor.")

    if st.session_state["current_square"] == 1:
        st.subheader("Journey Completed!")
        if st.button("Restart Game"):
            st.session_state["current_square"] = 0
            st.session_state["total_nm"]       = 0.0
            st.session_state["active_sponsor"] = None
            st.session_state["profile_sent"]   = False
            st.session_state["sponsor_decision"] = None
            st.session_state["passenger_game_stats"] = {
                "ad_score": 0,
                "likes": 0,
                "shares": 0,
                "campaigns_joined": 0,
                "impressions": 0
            }
            st.success("Game restarted!")


# ========== TAB 3: Sponsor Requirements (Passenger side) ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger)")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor. Accept one in the Board Game tab.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}% off boat costs")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} → {sp['end_date']})")
        st.markdown("**Demands**:")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near busy beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        st.info("Send your 'profile' to the sponsor for final approval?")

        if st.session_state["profile_sent"]:
            st.warning("You have ALREADY sent your profile to sponsor.")
            # Show sponsor decision if any
            if st.session_state["sponsor_decision"] == "Approved":
                st.success("Sponsor has approved you!")
            elif st.session_state["sponsor_decision"] == "Rejected":
                st.error("Sponsor has rejected you!")
            else:
                st.info("Waiting for sponsor decision (pending).")
        else:
            send_btn = st.button("Send My Profile to Sponsor for Approval")
            if send_btn:
                st.session_state["profile_sent"] = True
                st.session_state["sponsor_decision"] = None
                st.success("Profile sent! Go to 'Sponsor Admin' tab to see sponsor's decision.")


# ========== TAB 4: Sponsor Admin ========== 
with tabs[3]:
    st.title("Sponsor Admin Page")
    st.info("This simulates the sponsor's role. The sponsor sees the passenger's profile if they have 'sent' it.")

    # Αν δεν υπάρχει χορηγία, τίποτα
    if st.session_state["active_sponsor"] is None:
        st.warning("No sponsor campaign accepted by passenger yet.")
    else:
        sponsor = st.session_state["active_sponsor"]
        st.success(f"Active Sponsor: {sponsor['sponsor_name']}")
        
        # Έχει ο passenger στείλει το προφίλ;
        if st.session_state["profile_sent"]:
            st.markdown("### Passenger Profile Data")
            # Δείχνουμε τα στοιχεία που συμπλήρωσε ο Passenger στο Tab 1
            prof = st.session_state["profile"]
            st.write(f"- Name: {prof['name']}")
            st.write(f"- Surname: {prof['surname']}")
            st.write(f"- Age: {prof['age']}")
            st.write(f"- Facebook Friends: {prof['facebook_friends']}")
            st.write(f"- Instagram Followers: {prof['instagram_followers']}")
            st.write(f"- AdOnBoard Friends: {prof['adonboard_friends']}")

            # Sponsor can decide
            st.markdown("### Sponsor Decision")
            if st.session_state["sponsor_decision"] == "Approved":
                st.success("You have ALREADY Approved this passenger.")
            elif st.session_state["sponsor_decision"] == "Rejected":
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
        else:
            st.info("Passenger has NOT sent their profile yet.")
