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
         math.sin(d_lon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# ========== Session State Setup ==========

# 1) Προφίλ Επιβάτη
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "photo": None,
        "friend_count": 0
    }

# 2) Corporate Feed (εταιρικά post) - dummy
if "corporate_feed" not in st.session_state:
    st.session_state["corporate_feed"] = [
        {
            "post_id": 101,
            "company": "Vodafone",
            "logo": "https://via.placeholder.com/50.png?text=Vodafone",
            "text": "Special 5G plans for travelers!",
            "adds": 0,
            "shares": 0,
            "follows": 0
        },
        {
            "post_id": 102,
            "company": "Nike",
            "logo": "https://via.placeholder.com/50.png?text=Nike",
            "text": "Maritime running shoes – for deck jogging!",
            "adds": 0,
            "shares": 0,
            "follows": 0
        },
        {
            "post_id": 103,
            "company": "Coca-Cola",
            "logo": "https://via.placeholder.com/50.png?text=Coke",
            "text": "Stay refreshed at sea with a Coke!",
            "adds": 0,
            "shares": 0,
            "follows": 0
        }
    ]

# 3) Sponsors με τις διαδρομές τους (στο sidebar)
# Προσθέτουμε και έναν sponsor “COVID”, όπως ζητήθηκε.
if "sponsors" not in st.session_state:
    st.session_state["sponsors"] = [
        {
            "name": "COVID",   # Ο sponsor COVID
            "logo": "https://via.placeholder.com/50.png?text=COVID",
            "route_points": [
                {"name": "COVID Start", "coords": (36.0, 24.0)},
                {"name": "COVID Mid",   "coords": (36.5, 24.5)},
                {"name": "COVID Finish", "coords": (37.0, 25.0)}
            ]
        },
        {
            "name": "Vodafone",
            "logo": "https://via.placeholder.com/50.png?text=Vodafone",
            "route_points": [
                {"name": "Rhodes Port",  "coords": (36.4497, 28.2241)},
                {"name": "Kos",          "coords": (36.8938, 27.2877)},
                {"name": "Finish",       "coords": (37.0000, 26.5000)}
            ]
        },
        {
            "name": "Nike",
            "logo": "https://via.placeholder.com/50.png?text=Nike",
            "route_points": [
                {"name": "Athens Port", "coords": (37.9838, 23.7275)},
                {"name": "Santorini",   "coords": (36.3932, 25.4615)},
                {"name": "Finish",      "coords": (36.80,   25.30)}
            ]
        }
    ]

# 4) Ποιος sponsor είναι “highlighted”
if "highlighted_sponsor" not in st.session_state:
    st.session_state["highlighted_sponsor"] = None

# 5) Ενεργός sponsor (active_sponsor) όταν ο χρήστης πατήσει “Yes, proceed with ...”
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# 6) Έχει σταλεί το προφίλ; Απόφαση sponsor;
if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False
if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None
if "final_campaign_decision" not in st.session_state:
    st.session_state["final_campaign_decision"] = None

# 7) Total NM - dummy
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

# ---------- SIDEBAR: Sponsor list & highlight logic ----------
st.sidebar.title("Available Sponsors / Routes")
st.sidebar.write("Click sponsor to see its route in Board Game.")
for s in st.session_state["sponsors"]:
    if st.sidebar.button(s["name"]):
        st.session_state["highlighted_sponsor"] = s["name"]
        # reset sponsor decision etc.
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None
        st.experimental_rerun()

st.sidebar.write(f"Currently highlighted: {st.session_state['highlighted_sponsor'] or 'None'}")

# Επιπλέον: ένα progress bar ή info
st.sidebar.write("---")
st.sidebar.info("Active users: 35,000")

MAX_FRIENDS = 100
current_friends = st.session_state["profile"]["friend_count"]
ratio = min(current_friends / MAX_FRIENDS, 1.0)
st.sidebar.progress(ratio)
st.sidebar.write(f"Your AddOnBoard friend_count: {current_friends}/{MAX_FRIENDS}")

# ---------- Tabs (4) ----------
tabs = st.tabs([
    "1. Profile Setup & Corporate Feed",
    "2. Board Game",
    "3. Sponsor Requirements",
    "4. Sponsor Admin"
])

# ========== TAB 1: Profile Setup & Corporate Feed ========== 
with tabs[0]:
    st.title("Profile & Corporate Feed (Reverse-Facebook)")

    st.markdown("### Profile Setup")
    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        
        pfile = st.file_uploader("Profile Photo", type=["jpg","jpeg","png"])
        if st.form_submit_button("Save Profile"):
            if pfile is not None:
                st.session_state["profile"]["photo"] = pfile.read()
                st.success("Photo uploaded!")
            else:
                st.session_state["profile"]["photo"] = None
            st.success("Profile data saved!")

    # Show photo if any
    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Profile Photo", width=150)

    st.markdown("### Corporate (Sponsor) Feed")
    st.write("Companies post content to attract YOU, the passenger!")
    for post in st.session_state["corporate_feed"]:
        colA, colB = st.columns([0.15, 0.85])
        with colA:
            st.image(post["logo"], width=50)
        with colB:
            st.write(f"**{post['company']}**: {post['text']}")
            st.write(f"Adds: {post['adds']} | Shares: {post['shares']} | Follows: {post['follows']}")
        c1, c2, c3 = st.columns(3)
        if c1.button(f"Add (Post {post['post_id']})"):
            post["adds"] += 1
            st.experimental_rerun()
        if c2.button(f"Share (Post {post['post_id']})"):
            post["shares"] += 1
            st.experimental_rerun()
        if c3.button(f"Follow {post['company']} (Post {post['post_id']})"):
            post["follows"] += 1
            # optionally increment passenger's friend_count
            st.experimental_rerun()

# ========== TAB 2: Board Game ==========
with tabs[1]:
    st.title("Board Game: Sponsor Routes & Map")
    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")

    # Ελέγχουμε αν έχει επιλεγεί κάποιος highlighted sponsor
    if st.session_state["highlighted_sponsor"] is None:
        st.info("Select a sponsor from left sidebar to see its route here.")
    else:
        # Βρίσκουμε τον sponsor
        sponsor_data = None
        for s in st.session_state["sponsors"]:
            if s["name"] == st.session_state["highlighted_sponsor"]:
                sponsor_data = s
                break
        if sponsor_data is not None:
            st.success(f"Showing route for sponsor: {sponsor_data['name']}")
            # Φτιάχνουμε folium map
            route_pts = sponsor_data["route_points"]
            center = route_pts[0]["coords"]
            mm = folium.Map(location=center, zoom_start=6)
            coords_list = []
            for pt in route_pts:
                coords_list.append(pt["coords"])
                folium.Marker(pt["coords"], tooltip=f"{pt['name']} - {sponsor_data['name']}").add_to(mm)
            folium.PolyLine(coords_list, color="red", weight=3).add_to(mm)

            st_folium(mm, width=700, height=450)

            # Κουμπί proceed with route?
            if st.button(f"Yes, proceed with {sponsor_data['name']} route?"):
                # Δημιουργούμε active_sponsor
                dur_days = 5
                startd = date.today()
                endd   = startd + timedelta(days=dur_days)
                st.session_state["active_sponsor"] = {
                    "sponsor_name": sponsor_data["name"],
                    "required_impressions": 1000,
                    "discount_percent": 50,
                    "duration_days": dur_days,
                    "start_date": startd,
                    "end_date": endd,
                    "daily_posts": 2,
                    "hours_near_beach": 4,
                    "tshirts": f"{sponsor_data['name']} T-shirts & Banners"
                }
                st.session_state["profile_sent"] = False
                st.session_state["sponsor_decision"] = None
                st.session_state["final_campaign_decision"] = None
                st.success(f"You selected {sponsor_data['name']}! Now see Tab 3 for Sponsor Requirements.")
    
    # Αν sponsor_decision == Approved => κόκκινη ειδοποίηση
    if st.session_state["sponsor_decision"] == "Approved":
        st.markdown("### 🚨 **New Sponsor Notification** 🚨")
        st.info("Your sponsor has APPROVED your profile! Click below to open.")
        if st.button("Open Notification"):
            st.image("https://via.placeholder.com/600x300.png?text=Boat+with+Sponsor+Logos",
                     caption="Καλώς ήρθες στο ταξίδι! (Sponsored).")
            st.success("Enjoy your sponsored journey with custom logos & t-shirts!")

# ========== TAB 3: Sponsor Requirements ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor route chosen. See Board Game tab.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- daily_posts: {sp['daily_posts']}, hours_near_beach: {sp['hours_near_beach']}")
        st.write(f"- Materials: {sp['tshirts']}")

        if not st.session_state["profile_sent"]:
            st.warning("You haven't sent your profile to sponsor (Board Game tab).")
        else:
            dec = st.session_state["sponsor_decision"]
            if dec is None:
                st.info("Waiting for sponsor to Approve/Reject (Tab 4).")
            elif dec == "Rejected":
                st.error("Sponsor REJECTED your profile. Sorry!")
            elif dec == "Approved":
                st.success("Sponsor APPROVED your profile! Final acceptance?")
                final_dec = st.session_state["final_campaign_decision"]
                if final_dec == "Yes":
                    st.success("You have FINALLY accepted the sponsor's campaign!")
                elif final_dec == "No":
                    st.warning("You refused. No sponsor for you.")
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
                        st.warning("You refused. Maybe next time.")
                    elif think_btn:
                        st.session_state["final_campaign_decision"] = "Think"
                        st.info("You're still thinking…")

# ========== TAB 4: Sponsor Admin ==========
with tabs[3]:
    st.title("Sponsor Admin Page")
    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.warning("No sponsor route chosen by passenger yet.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        if not st.session_state["profile_sent"]:
            st.info("Passenger hasn't sent profile yet.")
        else:
            st.markdown("### Passenger's Profile")
            prof = st.session_state["profile"]
            st.write(f"- Name: {prof['name']}")
            st.write(f"- Surname: {prof['surname']}")
            st.write(f"- Age: {prof['age']}")
            st.write(f"- friend_count: {prof['friend_count']}")
            if prof["photo"]:
                st.image(prof["photo"], caption="Passenger Photo", width=150)

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
                    st.success("Passenger Approved! They see red notice in Board Game.")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")
