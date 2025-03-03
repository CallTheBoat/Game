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
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# ========== Session State Setup ==========

# Πληροφορίες προφίλ επιβάτη
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "photo": None,
        "friend_count": 0
    }

# Διαθέσιμες διαδρομές/χορηγοί στο sidebar
if "sponsors" not in st.session_state:
    # Π.χ. 2-3 sponsors με τις δικές τους διαδρομές (start->...)
    st.session_state["sponsors"] = [
        {
            "name": "Vodafone",
            "logo": "https://via.placeholder.com/50.png?text=Vodafone",
            "route_points": [
                # λίγα dummy νησιά για τη διαδρομή
                {"name": "Rhodes Port",  "coords": (36.4497, 28.2241)},
                {"name": "Kos",         "coords": (36.8938, 27.2877)},
                {"name": "Finish",      "coords": (37.0000, 26.5000)}
            ]
        },
        {
            "name": "Nike",
            "logo": "https://via.placeholder.com/50.png?text=Nike",
            "route_points": [
                {"name": "Athens Port", "coords": (37.9838, 23.7275)},
                {"name": "Santorini",   "coords": (36.3932, 25.4615)},
                {"name": "Finish",      "coords": (36.80, 25.30)}
            ]
        }
    ]

# Ποιος sponsor είναι highlighted
if "highlighted_sponsor" not in st.session_state:
    st.session_state["highlighted_sponsor"] = None

# Επιλεγμένος sponsor ως "active" (στο board game, requirements κ.λπ.)
if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

# Έχει σταλεί το προφίλ; Η απόφαση του sponsor;
if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False
if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None
if "final_campaign_decision" not in st.session_state:
    st.session_state["final_campaign_decision"] = None

# Για σκοπούς demo: total NM από αυτές τις διαδρομές
if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

# ---------- SIDEBAR: Sponsors list ----------
st.sidebar.title("Choose a Sponsor to see its route")
for s in st.session_state["sponsors"]:
    if st.sidebar.button(s["name"]):
        # Αν πατηθεί, ορίζουμε highlighted_sponsor σε αυτόν
        st.session_state["highlighted_sponsor"] = s["name"]
        # Μηδενίζουμε sponsor_decision & final_campaign_decision
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None
        # Και δεν ξεχνάμε to reset "profile_sent" κ.λπ.
        st.experimental_rerun()

# ---------- Tabs (4) ----------
tabs = st.tabs([
    "1. Profile Setup",
    "2. Board Game",
    "3. Sponsor Requirements",
    "4. Sponsor Admin"
])

# ========== TAB 1: Profile Setup ==========
with tabs[0]:
    st.title("Profile Setup (Passenger)")
    st.info("Fill your data; we might attract sponsors easier.")

    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        photo_file = st.file_uploader("Upload a Profile Photo", type=["jpg","jpeg","png"])
        if st.form_submit_button("Save Profile"):
            if photo_file is not None:
                st.session_state["profile"]["photo"] = photo_file.read()
                st.success("Uploaded photo.")
            else:
                st.session_state["profile"]["photo"] = None
            st.success("Profile saved. Check 'Board Game' tab or sponsor route from the sidebar.")

    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Profile Photo", width=150)

# ========== TAB 2: Board Game ==========
with tabs[1]:
    st.title("Board Game with Sponsor Route")

    # Αν δεν έχει επιλεγεί κανένας sponsor προς highlight, απλά κεντρικός χάρτης
    if st.session_state["highlighted_sponsor"] is None:
        st.info("Pick a sponsor from the left sidebar to see its route here.")
    else:
        # Βρίσκουμε τον sponsor data
        sponsor_data = None
        for s in st.session_state["sponsors"]:
            if s["name"] == st.session_state["highlighted_sponsor"]:
                sponsor_data = s
                break
        if sponsor_data:
            st.success(f"Showing route for sponsor: {sponsor_data['name']}")
            # Φτιάχνουμε Folium map με τα route_points
            route_points = sponsor_data["route_points"]
            center = route_points[0]["coords"]
            m = folium.Map(location=center, zoom_start=6)
            
            # Προσθέτουμε markers & γραμμή
            coords_list = []
            for pt in route_points:
                coords_list.append(pt["coords"])
                # Marker ίσως με λογότυπο sponsor
                folium.Marker(
                    pt["coords"],
                    tooltip=f"{pt['name']} - {sponsor_data['name']}",
                    icon=folium.Icon(color="blue", icon="flag")
                ).add_to(m)
            folium.PolyLine(coords_list, color="red", weight=3).add_to(m)

            st_folium(m, width=700, height=450)
            # Αν θέλουμε κουμπί "Yes, proceed with sponsor route"
            st.info(f"Do you want to proceed with the route of {sponsor_data['name']}?")
            if st.button(f"Yes, proceed with {sponsor_data['name']} route?"):
                # Αν πατήσει Yes, τότε ορίζουμε "active_sponsor"
                # Στον Tab 3 θα δούμε sponsor requirements
                st.session_state["active_sponsor"] = {
                    "sponsor_name": sponsor_data["name"],
                    "required_impressions": 1000,
                    "discount_percent": 50,
                    "duration_days": 5,
                    "start_date": date.today(),
                    "end_date": date.today() + timedelta(days=5),
                    "daily_posts": 2,
                    "hours_near_beach": 4,
                    "tshirts": f"{sponsor_data['name']} T-shirts & Banners"
                }
                st.session_state["profile_sent"]   = False
                st.session_state["sponsor_decision"] = None
                st.session_state["final_campaign_decision"] = None

                st.success(f"Ok, {sponsor_data['name']} sponsor route selected! Now see Sponsor Requirements (Tab 3).")

# ========== TAB 3: Sponsor Requirements ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")

    if st.session_state["active_sponsor"] is None:
        st.info("No active sponsor route chosen yet. Select from Board Game tab or left sidebar.")
    else:
        sp = st.session_state["active_sponsor"]
        st.success(f"Active Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- daily_posts: {sp['daily_posts']}, hours_near_beach: {sp['hours_near_beach']}")
        st.write(f"- Materials: {sp['tshirts']}")

        if not st.session_state["profile_sent"]:
            st.warning("You haven't sent your profile to sponsor. Maybe do so from Board Game tab.")
        else:
            dec = st.session_state["sponsor_decision"]
            if dec is None:
                st.info("Waiting for sponsor to Approve/Reject. See Sponsor Admin tab.")
            elif dec == "Rejected":
                st.error("Sponsor REJECTED your profile. Sorry!")
            elif dec == "Approved":
                st.success("Sponsor APPROVED your profile! Final acceptance?")
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
            st.markdown("### Passenger Profile")
            prof = st.session_state["profile"]
            st.write(f"- Name: {prof['name']}")
            st.write(f"- Surname: {prof['surname']}")
            st.write(f"- Age: {prof['age']}")
            st.write(f"- friend_count: {prof['friend_count']}")
            if prof["photo"]:
                st.image(prof["photo"], caption="Passenger's Photo", width=150)

            st.markdown("#### Approve or Reject passenger's profile?")
            dec = st.session_state["sponsor_decision"]
            if dec == "Approved":
                st.success("ALREADY Approved.")
            elif dec == "Rejected":
                st.error("REJECTED passenger.")
            else:
                approve_btn = st.button("Approve Passenger")
                reject_btn = st.button("Reject Passenger")
                if approve_btn:
                    st.session_state["sponsor_decision"] = "Approved"
                    st.success("Passenger Approved! They see it in Tab 2/3.")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")
