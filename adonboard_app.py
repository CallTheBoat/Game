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
        "friend_count": 0
    }

# Σπόνσορες που εμφανίζονται & οι συντεταγμένες/λογότυπα τους
# π.χ. 3 sponsors σε διαφορετικά νησιά
if "sponsors" not in st.session_state:
    st.session_state["sponsors"] = [
        {
            "name": "Vodafone",
            "coords": (36.4349, 28.2176),  # Rhodes
            "logo": "https://via.placeholder.com/50.png?text=Voda"
        },
        {
            "name": "Nike",
            "coords": (36.3932, 25.4615),  # Santorini
            "logo": "https://via.placeholder.com/50.png?text=Nike"
        },
        {
            "name": "Coca-Cola",
            "coords": (37.4467, 25.3289),  # Mykonos
            "logo": "https://via.placeholder.com/50.png?text=Coke"
        }
    ]

# Ανάθεσε ένα “highlighted_sponsor” όταν ο χρήστης πατήσει στο sidebar
if "highlighted_sponsor" not in st.session_state:
    st.session_state["highlighted_sponsor"] = None

if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False

if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None

if "final_campaign_decision" not in st.session_state:
    st.session_state["final_campaign_decision"] = None

if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

# ---------- SIDEBAR: Display sponsors & let user highlight them ----------
st.sidebar.title("Sponsors on Map")
st.sidebar.write("Click a sponsor to highlight them on the Board Game map.")
for s in st.session_state["sponsors"]:
    if st.sidebar.button(s["name"]):
        st.session_state["highlighted_sponsor"] = s["name"]
        st.experimental_rerun()

st.sidebar.write("Highlight:", st.session_state["highlighted_sponsor"] or "None")

# ---------- Tabs -----------
tabs = st.tabs([
    "1. Profile Setup",
    "2. Board Game",
    "3. Sponsor Requirements",
    "4. Sponsor Admin"
])

# ========== TAB 1: Profile Setup ==========
with tabs[0]:
    st.title("Profile Setup (Passenger)")
    st.info("Fill your profile; your friend_count or other stats could help attract sponsors.")

    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        
        photo_file = st.file_uploader("Upload a Profile Photo", type=["jpg","jpeg","png"])
        save_btn = st.form_submit_button("Save Profile")
        if save_btn:
            if photo_file is not None:
                st.session_state["profile"]["photo"] = photo_file.read()
                st.success("Profile photo uploaded!")
            else:
                st.session_state["profile"]["photo"] = None
            st.success("Profile data saved! Now see 'Board Game' tab.")

    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Your Profile Photo", width=150)

# ========== TAB 2: Board Game ==========
with tabs[1]:
    st.title("Board Game: Islands & Sponsors")

    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")

    # Folium map
    center_coords = (36.8, 25.0)  # Some center in Greek islands
    m = folium.Map(location=center_coords, zoom_start=6)

    # Προσθέτουμε markers για κάθε sponsor
    for sponsor in st.session_state["sponsors"]:
        # αν αυτός ο sponsor είναι “highlighted”, βάζουμε custom icon size
        if st.session_state["highlighted_sponsor"] == sponsor["name"]:
            icon_size = (80, 80)  # μεγάλο icon για highlight
        else:
            icon_size = (50, 50)  # default

        icon_html = folium.CustomIcon(sponsor["logo"], icon_size=icon_size)
        folium.Marker(
            location=sponsor["coords"],
            icon=icon_html,
            tooltip=f"{sponsor['name']} Sponsor"
        ).add_to(m)

    st_folium(m, width=700, height=450)

    # Εάν ο sponsor_decision == "Approved", εμφάνισε “κόκκινη ειδοποίηση”
    if st.session_state["sponsor_decision"] == "Approved":
        st.markdown("### 🚨 **New Sponsor Notification** 🚨")
        st.info("Your sponsor has APPROVED your profile! Click below to open.")
        if st.button("Open Notification"):
            st.image("https://via.placeholder.com/600x300.png?text=Boat+with+Sponsor+Logos",
                     caption="Καλώς ήρθες στο ταξίδι! (Sponsored).")
            st.success("Enjoy your sponsored journey with custom logos & t-shirts!")
    
    # Χορηγική προσφορά (π.χ. Vodafone)
    st.markdown("### Sponsor Offer")
    st.info("Sponsor: 'Vodafone' wants 1000 impressions, 50% discount.")
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
        st.success("Sponsor accepted. You may send your profile below or see 'Sponsor Requirements' tab.")
    elif decline_btn:
        st.warning("Declined sponsor.")
        st.session_state["active_sponsor"] = None
        st.session_state["profile_sent"] = False
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None

    # If sponsor active => show “Send My Profile”
    sp = st.session_state["active_sponsor"]
    if sp is not None:
        st.markdown("### Sponsor Requirements (quick view)")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']}→{sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day, {sp['hours_near_beach']} hrs near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if st.session_state["profile_sent"]:
            st.warning("Profile already sent. Wait for sponsor decision.")
        else:
            if st.button("Send My Profile to Sponsor"):
                st.session_state["profile_sent"] = True
                st.session_state["sponsor_decision"] = None
                st.session_state["final_campaign_decision"] = None
                st.success("Profile sent! Sponsor sees it in 'Sponsor Admin' tab.")

# ========== TAB 3: Sponsor Requirements (Passenger) ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor accepted yet.")
    else:
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- daily_posts: {sp['daily_posts']}, hours_near_beach: {sp['hours_near_beach']}")
        st.write(f"- Materials: {sp['tshirts']}")

        if not st.session_state["profile_sent"]:
            st.warning("Haven't sent profile to sponsor. See Board Game tab.")
        else:
            dec = st.session_state["sponsor_decision"]
            if dec is None:
                st.info("Waiting for sponsor decision (Tab 4).")
            elif dec == "Rejected":
                st.error("Sponsor REJECTED your profile.")
            elif dec == "Approved":
                st.success("Sponsor APPROVED your profile!")
                st.markdown("#### Final Acceptance?")

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
            st.write(f"- 'friend_count': {prof['friend_count']} (AddOnBoard net)")

            if prof["photo"]:
                st.image(prof["photo"], caption="Passenger's Photo", width=150)

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
                    st.success("Passenger Approved! Will see red notice in Board Game tab.")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")
