import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta
import random

# ---------- Minimal distance function ----------
def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lat2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# ========== Session State ==========

# 1) Προφίλ όπως πριν
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "photo": None,
        "facebook_friends": 0,
        "instagram_followers": 0,
        "adonboard_friends": 0,
        "friend_count": 0
    }

# 2) Sponsor route squares (Rhodes -> Kallithea -> Lindos -> Prasonisi -> Finish) όπως είχαμε
if "sponsor_squares" not in st.session_state:
    st.session_state["sponsor_squares"] = [
        {
            "name": "Rhodes - Main Port",
            "coords": (36.4349, 28.2176),
            "sponsor_logo": "https://via.placeholder.com/60.png?text=Vodafone"
        },
        {
            "name": "Kallithea Beach",
            "coords": (36.3825, 28.2472),
            "sponsor_logo": None
        },
        {
            "name": "Lindos Beach",
            "coords": (36.0917, 28.0850),
            "sponsor_logo": None
        },
        {
            "name": "Prasonisi Beach",
            "coords": (35.8873, 27.7876),
            "sponsor_logo": "https://via.placeholder.com/60.png?text=Nike"
        },
        {
            "name": "Sponsor Finish",
            "coords": (35.6000, 27.5000),
            "sponsor_logo": None
        }
    ]

# 3) "Monopoly" route squares (Rhodes -> ... -> Kos) με events
#   - engine failure, strong winds, strong currents, beach party κτλ.
if "monopoly_squares" not in st.session_state:
    st.session_state["monopoly_squares"] = [
        {
            "name": "Rhodes Start",
            "coords": (36.4349, 28.2176),
            "event": "Starting point."
        },
        {
            "name": "Square 1",
            "coords": (36.4000, 28.10),
            "event": "Engine failure! Lose a turn."
        },
        {
            "name": "Square 2",
            "coords": (36.3000, 28.00),
            "event": "Beach party! Stay here 1 turn to enjoy."
        },
        {
            "name": "Square 3",
            "coords": (36.2000, 27.90),
            "event": "Strong currents - move forward 1 extra step."
        },
        {
            "name": "Square 4",
            "coords": (36.1000, 27.80),
            "event": "Strong winds - slower speed next turn."
        },
        {
            "name": "Kos Finish",
            "coords": (36.8938, 27.2877),
            "event": "Arrived at Kos!"
        }
    ]

# Αρχικοποίηση index/dice logic για το Monopoly route
if "monopoly_index" not in st.session_state:
    st.session_state["monopoly_index"] = 0  # σε ποιο square βρισκόμαστε

# Τα υπόλοιπα session states
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False

if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None

if "final_campaign_decision" not in st.session_state:
    st.session_state["final_campaign_decision"] = None

# ---------- Sidebar & progress ----------
st.sidebar.title("AddOnBoard Stats")
st.sidebar.info("Active users: 35,000")
MAX_FRIENDS = 100
ratio = min(st.session_state["profile"]["friend_count"] / MAX_FRIENDS, 1.0)
st.sidebar.progress(ratio)
st.sidebar.write(f"You have {st.session_state['profile']['friend_count']} / {MAX_FRIENDS} potential AddOnBoard friends.")

# ---------- Tabs (4) ----------
tabs = st.tabs([
    "1. Profile Setup",
    "2. Board Game (Two Routes)",
    "3. Sponsor Requirements",
    "4. Sponsor Admin"
])

# ========== TAB 1: Profile Setup ==========
with tabs[0]:
    st.title("Profile Setup (Passenger)")
    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])

        st.session_state["profile"]["facebook_friends"] = st.number_input("Facebook Friends", min_value=0, value=st.session_state["profile"]["facebook_friends"])
        st.session_state["profile"]["instagram_followers"] = st.number_input("Instagram Followers", min_value=0, value=st.session_state["profile"]["instagram_followers"])
        st.session_state["profile"]["adonboard_friends"] = st.number_input("AdOnBoard Friends", min_value=0, value=st.session_state["profile"]["adonboard_friends"])

        photo_file = st.file_uploader("Upload a Profile Photo", type=["jpg","jpeg","png"])
        save_btn = st.form_submit_button("Save Profile")
        if save_btn:
            if photo_file:
                st.session_state["profile"]["photo"] = photo_file.read()
                st.success("Profile photo uploaded!")
            else:
                st.session_state["profile"]["photo"] = None
            st.success("Profile data saved!")
    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Your Profile Photo", width=150)


# ========== TAB 2: Board Game (Two Routes) ==========
with tabs[1]:
    st.title("Board Game with Two Routes")
    route_choice = st.radio("Select a Route:", ["Sponsor Route", "Monopoly Route"])

    # 1) If sponsor route selected
    if route_choice == "Sponsor Route":
        st.subheader("Sponsor Route - Dotted Purple")
        squares = st.session_state["sponsor_squares"]
        center_coords = squares[0]["coords"]
        sponsor_map = folium.Map(location=center_coords, zoom_start=6)

        coords_list = []
        for sq in squares:
            coords_list.append(sq["coords"])
            # CircleMarker για Beach?
            if "Beach" in sq["name"]:
                folium.CircleMarker(
                    location=sq["coords"],
                    radius=8,
                    color="red",
                    fill=True,
                    fill_color="yellow",
                    fill_opacity=0.7,
                    tooltip=sq["name"]
                ).add_to(sponsor_map)
            else:
                folium.Marker(sq["coords"], tooltip=sq["name"]).add_to(sponsor_map)

            # Sponsor logo εάν υπάρχει
            if sq["sponsor_logo"]:
                icon_html = folium.CustomIcon(sq["sponsor_logo"], icon_size=(60,60))
                folium.Marker(
                    location=sq["coords"],
                    icon=icon_html,
                    tooltip=f"Sponsor at {sq['name']}"
                ).add_to(sponsor_map)

        # Διακεκομμένη (dotted) polyline σε μωβ
        folium.PolyLine(coords_list, color="purple", weight=4, dash_array="10,5").add_to(sponsor_map)

        st_folium(sponsor_map, width=700, height=450)

        # Ειδοποίηση αν sponsor_decision == Approved
        if st.session_state["sponsor_decision"] == "Approved":
            st.markdown("### 🚨 **New Sponsor Notification** 🚨")
            st.info("Your sponsor has APPROVED your profile! Click below to open.")
            if st.button("Open Notification"):
                st.image("https://via.placeholder.com/600x300.png?text=Boat+with+Sponsor+Logos",
                         caption="Καλώς ήρθες στο ταξίδι! (Sponsored).")
                st.success("Enjoy your sponsored journey with custom logos & t-shirts!")

        st.markdown("### Sponsor Offer")
        st.info("""Sponsor: 'Vodafone' wants 1000 impressions, 50% discount. 
Proposed route: 
- Rhodes - Main Port
- Kallithea Beach
- Lindos Beach
- Prasonisi Beach
- Sponsor Finish
""")

        accept_btn = st.button("Yes, Accept Sponsor")
        decline_btn = st.button("No, Decline Sponsor")
        if accept_btn:
            dur_days = 5
            sday = date.today()
            eday = sday + timedelta(days=dur_days)
            st.session_state["active_sponsor"] = {
                "sponsor_name": "Vodafone",
                "required_impressions": 1000,
                "discount_percent": 50,
                "duration_days": dur_days,
                "start_date": sday,
                "end_date": eday,
                "daily_posts": 2,
                "hours_near_beach": 4,
                "tshirts": "Vodafone T-shirts & Banners"
            }
            st.session_state["profile_sent"] = False
            st.session_state["sponsor_decision"] = None
            st.session_state["final_campaign_decision"] = None
            st.success("Sponsor accepted. Send your profile or see Tab 3.")
        elif decline_btn:
            st.warning("Declined sponsor.")
            st.session_state["active_sponsor"] = None
            st.session_state["profile_sent"] = False
            st.session_state["sponsor_decision"] = None
            st.session_state["final_campaign_decision"] = None

        # If there's an active sponsor, show “Send My Profile”
        sp = st.session_state["active_sponsor"]
        if sp is not None:
            st.markdown("### Sponsor Requirements (quick view)")
            st.write(f"- Required Impressions: {sp['required_impressions']}")
            st.write(f"- Discount: {sp['discount_percent']}%")
            st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']}→{sp['end_date']})")
            st.write(f"- {sp['daily_posts']} posts/day, {sp['hours_near_beach']} hrs near beaches/day")
            st.write(f"- Materials: {sp['tshirts']}")

            if st.session_state["profile_sent"]:
                st.warning("Profile already sent. Wait sponsor's decision (Tab 3/4).")
            else:
                if st.button("Send My Profile to Sponsor"):
                    st.session_state["profile_sent"] = True
                    st.session_state["sponsor_decision"] = None
                    st.session_state["final_campaign_decision"] = None
                    st.success("Profile sent! The sponsor sees it in 'Sponsor Admin' tab.")

    # 2) If Monopoly Route selected
    else:
        st.subheader("Monopoly-Style Route (Rhodes -> Kos) with Dice & Events")
        squares = st.session_state["monopoly_squares"]
        center = squares[0]["coords"]
        mono_map = folium.Map(location=center, zoom_start=6)

        coords_list = []
        for sq in squares:
            coords_list.append(sq["coords"])
            # Marker (circle) for each square
            # Color them differently if it's Start/Finish or a normal event
            if "Finish" in sq["name"]:
                folium.CircleMarker(
                    location=sq["coords"],
                    radius=8,
                    color="green",
                    fill=True,
                    fill_color="lime",
                    fill_opacity=0.8,
                    tooltip=sq["name"]
                ).add_to(mono_map)
            elif "Start" in sq["name"]:
                folium.CircleMarker(
                    location=sq["coords"],
                    radius=8,
                    color="blue",
                    fill=True,
                    fill_color="aqua",
                    fill_opacity=0.8,
                    tooltip=sq["name"]
                ).add_to(mono_map)
            else:
                folium.CircleMarker(
                    location=sq["coords"],
                    radius=6,
                    color="gray",
                    fill=True,
                    fill_color="white",
                    fill_opacity=0.8,
                    tooltip=f"{sq['name']} | {sq['event']}"
                ).add_to(mono_map)

        # Solid green line for the Monopoly route
        folium.PolyLine(coords_list, color="green", weight=4).add_to(mono_map)

        st_folium(mono_map, width=700, height=450)

        st.write(f"**Current Index**: {st.session_state['monopoly_index']} / {len(squares)-1}")
        st.write(f"**Current Square**: {squares[st.session_state['monopoly_index']]['name']}")
        st.info(f"Event: {squares[st.session_state['monopoly_index']]['event']}")

        if st.button("Roll the Dice for Monopoly Route"):
            dice = random.randint(1, 6)
            st.success(f"You rolled a {dice}!")
            old_index = st.session_state["monopoly_index"]
            new_index = old_index + dice
            if new_index >= len(squares) - 1:
                new_index = len(squares) - 1
            # Calculate distance moved
            startC = squares[old_index]["coords"]
            endC   = squares[new_index]["coords"]
            dist_nm_ = distance_nm(startC[0], startC[1], endC[0], endC[1])
            st.session_state["total_nm"] += dist_nm_
            st.session_state["monopoly_index"] = new_index
            st.info(f"Arrived at {squares[new_index]['name']}")
            st.info(f"Event: {squares[new_index]['event']}")

            # Some simple event logic:
            if "Lose a turn" in squares[new_index]["event"]:
                st.warning("You lose a turn next time (not fully implemented).")
            elif "Beach party" in squares[new_index]["event"]:
                st.success("Party time! Stay 1 turn? (not fully implemented).")
            elif "Strong currents" in squares[new_index]["event"]:
                st.info("Move forward 1 extra square! (not fully implemented).")
            elif "Strong winds" in squares[new_index]["event"]:
                st.info("Slower speed next turn (not fully implemented).")

        # If final square
        if st.session_state["monopoly_index"] == len(squares) - 1:
            st.balloons()
            st.success("Arrived at Kos Finish!")
            if st.button("Restart Monopoly Route"):
                st.session_state["monopoly_index"] = 0
                st.success("Monopoly route restarted.")


# ========== TAB 3: Sponsor Requirements (Passenger) ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")
    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor. Accept one in 'Board Game' tab's Sponsor Route.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}% off boat costs")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if not st.session_state["profile_sent"]:
            st.warning("Haven't sent your profile to sponsor. Go to 'Board Game' tab (Sponsor Route).")
        else:
            dec = st.session_state["sponsor_decision"]
            if dec is None:
                st.info("Waiting for sponsor's decision. See Tab 4.")
            elif dec == "Rejected":
                st.error("Sponsor REJECTED your profile. Sorry!")
            elif dec == "Approved":
                st.success("Sponsor APPROVED your profile!")
                st.markdown("#### Final acceptance of the campaign?")
                final_dec = st.session_state["final_campaign_decision"]
                if final_dec == "Yes":
                    st.success("You have FINALLY accepted the sponsor's campaign!")
                elif final_dec == "No":
                    st.warning("You refused the final campaign. No sponsor for you.")
                elif final_dec == "Think":
                    st.info("Still thinking…")
                else:
                    yes_btn   = st.button("Yes, I accept final campaign!")
                    no_btn    = st.button("No, I refuse final campaign.")
                    think_btn = st.button("I Will Think About It.")
                    if yes_btn:
                        st.session_state["final_campaign_decision"] = "Yes"
                        st.success("You have FINALLY accepted the sponsor's campaign!")
                    elif no_btn:
                        st.session_state["final_campaign_decision"] = "No"
                        st.warning("You refused the final campaign. Maybe next time.")
                    elif think_btn:
                        st.session_state["final_campaign_decision"] = "Think"
                        st.info("You're still thinking…")

# ========== TAB 4: Sponsor Admin ==========
with tabs[3]:
    st.title("Sponsor Admin Page")
    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.warning("No sponsor route accepted by passenger yet (Tab 2).")
    else:
        st.success(f"Sponsor: {sp['sponsor_name']}")
        if not st.session_state["profile_sent"]:
            st.info("Passenger hasn't sent profile yet.")
        else:
            st.markdown("### Passenger's Profile")
            prof = st.session_state["profile"]
            st.write(f"- Name: {prof['name']}")
            st.write(f"- Surname: {prof['surname']}")
            st.write(f"- Age: {prof['age']}")
            st.write(f"- Facebook Friends: {prof['facebook_friends']}")
            st.write(f"- Instagram Followers: {prof['instagram_followers']}")
            st.write(f"- AdOnBoard Friends: {prof['adonboard_friends']}")
            st.write(f"- 'AddOnBoard' friend_count: {prof['friend_count']}")

            if prof["photo"]:
                st.image(prof["photo"], caption="Passenger's Profile Photo", width=150)

            st.markdown("#### Approve or Reject passenger's profile?")
            dec = st.session_state["sponsor_decision"]
            if dec == "Approved":
                st.success("Already Approved.")
            elif dec == "Rejected":
                st.error("Already Rejected.")
            else:
                approve_btn = st.button("Approve Passenger")
                reject_btn  = st.button("Reject Passenger")
                if approve_btn:
                    st.session_state["sponsor_decision"] = "Approved"
                    st.success("Passenger Approved! Red notification in Board Game tab.")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")