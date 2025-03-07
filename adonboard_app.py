import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ---------- Minimal distance function ----------
def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lat2 - lon1)
    a = (math.sin(d_lat / 2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# ========== Session State ==========
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

# Λίστα νησιών - squares στο board game
# Τώρα προσθέτουμε επιπλέον παραλίες (ονομαστικά) + sponsor_logo
if "island_squares" not in st.session_state:
    # Παράδειγμα: έχουμε 5 στάσεις (2 νησιά κι 3 παραλίες)
    st.session_state["island_squares"] = [
        {
            "name": "Rhodes - Main Port",
            "coords": (36.4349, 28.2176),
            "sponsor_logo": "https://via.placeholder.com/50.png?text=Vodafone"
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
            "sponsor_logo": "https://via.placeholder.com/50.png?text=Nike"
        },
        {
            "name": "Finish Spot",
            "coords": (35.6000, 27.5000),
            "sponsor_logo": None
        }
    ]

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

# Για την “κόκκινη ειδοποίηση”
if "show_red_light" not in st.session_state:
    st.session_state["show_red_light"] = False

# ---------- Sidebar με progress bar ----------
st.sidebar.title("AddOnBoard Platform Stats")
st.sidebar.info("Active users: 35,000")
MAX_FRIENDS = 100
current_friends = st.session_state["profile"]["friend_count"]
progress_ratio = min(current_friends / MAX_FRIENDS, 1.0)
st.sidebar.progress(progress_ratio)
st.sidebar.write(f"You have {current_friends} / {MAX_FRIENDS} possible AddOnBoard friends.")
st.sidebar.write("Interact with companies or 'Add Friend' to grow your network & attract sponsors!")

# ---------- Tabs (4) ----------
tabs = st.tabs([
    "1. Profile Setup",
    "2. Board Game (Islands & Beaches)",
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
            if photo_file is not None:
                st.session_state["profile"]["photo"] = photo_file.read()
                st.success("Profile photo uploaded!")
            else:
                st.session_state["profile"]["photo"] = None
            st.success("Profile data saved. Next, go to 'Board Game' tab or proceed below to see sponsor logic.")

    # Show photo
    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Your Profile Photo", width=150)

# ========== TAB 2: Board Game (Islands & Beaches) ==========
with tabs[1]:
    st.title("Board Game: Islands & Beaches with Dotted Routes")

    st.write("We have multiple beach stops. Some squares may have sponsor logos pinned on them.")
    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")

    # Φτιάχνουμε χάρτη
    island_squares = st.session_state["island_squares"]
    center_coords = island_squares[0]["coords"]
    m = folium.Map(location=center_coords, zoom_start=6)

    coords_list = []
    for sq in island_squares:
        coords_list.append(sq["coords"])
        # βασικός marker
        folium.Marker(sq["coords"], tooltip=sq["name"]).add_to(m)
        # αν υπάρχει sponsor_logo
        if sq["sponsor_logo"] is not None:
            icon_html = folium.CustomIcon(sq["sponsor_logo"], icon_size=(50,50))
            folium.Marker(
                sq["coords"],
                icon=icon_html,
                tooltip=f"Sponsor at {sq['name']}"
            ).add_to(m)

    # Προσθήκη διακεκομμένης γραμμής (dashed/dotted) ανάμεσα στα σημεία
    # Με χρήση dash_array="5,5" 
    folium.PolyLine(
        coords_list,
        color="blue",
        weight=3,
        dash_array="5,5"
    ).add_to(m)

    st_folium(m, width=700, height=450)

    # Κόκκινη ειδοποίηση
    if st.session_state["sponsor_decision"] == "Approved":
        st.markdown("### 🚨 **New Sponsor Notification** 🚨")
        st.info("Your sponsor has APPROVED your profile! Click below to open.")
        if st.button("Open Notification"):
            st.image("https://via.placeholder.com/600x300.png?text=Boat+with+Sponsor+Logos",
                     caption="Καλώς ήρθες στο ταξίδι! (Sponsored).")
            st.success("Enjoy your sponsored journey with custom logos & t-shirts!")

    st.markdown("### Sponsor Offer")
    st.info("Sponsor: 'Vodafone' wants 1000 impressions, 50% discount. Accept or Decline?")
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
        st.success("Sponsor accepted. You may send your profile below or check Tab 3.")
    elif decline_btn:
        st.warning("Declined sponsor.")
        st.session_state["active_sponsor"] = None
        st.session_state["profile_sent"] = False
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None

    # If there's an active sponsor
    sp = st.session_state["active_sponsor"]
    if sp is not None:
        st.markdown("### Sponsor Requirements (quick view)")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']}→{sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if st.session_state["profile_sent"]:
            st.warning("Profile already sent. Wait for sponsor's decision in Tab 3 or Tab 4.")
        else:
            if st.button("Send My Profile to Sponsor"):
                st.session_state["profile_sent"] = True
                st.session_state["sponsor_decision"] = None
                st.session_state["final_campaign_decision"] = None
                st.success("Profile sent! The sponsor sees it in 'Sponsor Admin' tab.")

# ========== TAB 3: Sponsor Requirements (Passenger) ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor. Accept one in 'Board Game' tab.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}% off boat costs")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if not st.session_state["profile_sent"]:
            st.warning("You haven't sent your profile to sponsor. Go to Board Game tab.")
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
        st.warning("No sponsor campaign accepted by passenger yet.")
    else:
        st.success(f"Sponsor: {sp['sponsor_name']} is active.")
        
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
            st.write(f"- 'AddOnBoard' friend_count: {prof.get('friend_count',0)}")
            
            if prof["photo"]:
                st.image(prof["photo"], caption="Passenger's Profile Photo", width=150)

            st.markdown("#### Approve or Reject passenger's profile?")
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
                    st.success("Passenger Approved! Red light notification in Board Game tab.")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")
