import streamlit as st
import random
import time
import math
import folium
from streamlit_folium import st_folium

# ---------------------------
# 1) Χρήσιμα constants / funcs
# ---------------------------
EARTH_RADIUS_KM = 6371.0
KM_TO_NM = 0.539957  # 1 km ~ 0.54 nautical miles

def haversine_distance_km(lat1, lon1, lat2, lon2):
    """
    Επιστρέφει την απόσταση σε χιλιόμετρα (km) μεταξύ δύο σημείων
    (lat1, lon1) - (lat2, lon2) με χρήση του τύπου haversine.
    """
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = EARTH_RADIUS_KM * c
    return distance_km

def distance_nm(lat1, lon1, lat2, lon2):
    """Υπολογίζει την απόσταση σε Ναυτικά Μίλια (NM) μεταξύ 2 σημείων."""
    dist_km = haversine_distance_km(lat1, lon1, lat2, lon2)
    dist_nm = dist_km * KM_TO_NM
    return dist_nm

def load_css():
    """Φόρτωση custom CSS (προαιρετικά)."""
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


# ---------------------------
# 2) Βασικές ρυθμίσεις σελίδας
# ---------------------------
st.set_page_config(page_title="AdOnBoard - Futuristic UI", layout="wide")
load_css()

st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Futuristic Experience</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose your role in the world of maritime advertising.</p>", unsafe_allow_html=True)

# ---------------------------
# 3) Session State
# ---------------------------
if "routes" not in st.session_state:
    # Default routes
    st.session_state["routes"] = {
        "Santorini - Mykonos": [(36.3932, 25.4615), (37.4467, 25.3289)],
        "Rhodes - Athens": [(36.4349, 28.2176), (37.9838, 23.7275)]
    }

# Θα αποθηκεύουμε εδώ την απόσταση της τρέχουσας διαδρομής (σε NM)
if "current_dist_nm" not in st.session_state:
    st.session_state["current_dist_nm"] = 0.0

# Θα αποθηκεύουμε εδώ πόσα NM έχει διανύσει το σκάφος στη συγκεκριμένη διαδρομή
if "progress_nm" not in st.session_state:
    st.session_state["progress_nm"] = 0.0

# Θα κρατάμε και ποια διαδρομή είναι επιλεγμένη για να μη μπερδεύονται οι αποστάσεις
if "selected_route" not in st.session_state:
    # Αρχικοποιείται στην πρώτη διαδρομή που υπάρχει σαν default
    default_route = list(st.session_state["routes"].keys())[0]
    st.session_state["selected_route"] = default_route
    # Υπολόγισε απόσταση για default
    coords = st.session_state["routes"][default_route]
    st.session_state["current_dist_nm"] = distance_nm(
        coords[0][0], coords[0][1],
        coords[1][0], coords[1][1]
    )
    st.session_state["progress_nm"] = 0.0

# ---------------------------
# 4) Επιλογή Ρόλου
# ---------------------------
role = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])
if role == "Passenger":
    st.write("Explore destinations, earn rewards, and interact with sponsors.")
elif role == "Ship Owner":
    st.write("List your routes, attract sponsors, and maximize profits.")
elif role == "Sponsor":
    st.write("Choose routes, advertise your brand, and track engagement.")

# ---------------------------
# 5) Δυναμική προσθήκη νέων routes
# ---------------------------
st.markdown("---")
st.subheader("Add a New Route Dynamically")

with st.form("route_form"):
    route_name = st.text_input("Route Name", placeholder="e.g. Corfu - Patras")
    start_lat = st.number_input("Start Latitude", value=36.0)
    start_lon = st.number_input("Start Longitude", value=25.0)
    end_lat = st.number_input("End Latitude", value=37.0)
    end_lon = st.number_input("End Longitude", value=25.5)
    
    submitted = st.form_submit_button("Add Route")
    if submitted:
        if route_name.strip() != "":
            st.session_state["routes"][route_name] = [(start_lat, start_lon), (end_lat, end_lon)]
            st.success(f"Route '{route_name}' added successfully!")
        else:
            st.warning("Please enter a valid route name.")

st.markdown("---")

# ---------------------------
# 6) Επιλογή Διαδρομής
# ---------------------------
all_route_names = list(st.session_state["routes"].keys())
selected_route = st.selectbox("Choose a Route:", all_route_names)

# Αν αλλάξει η διαδρομή, κάνε reset την πρόοδο
if selected_route != st.session_state["selected_route"]:
    st.session_state["selected_route"] = selected_route
    # Υπολόγισε νέα απόσταση
    coords = st.session_state["routes"][selected_route]
    st.session_state["current_dist_nm"] = distance_nm(
        coords[0][0], coords[0][1],
        coords[1][0], coords[1][1]
    )
    st.session_state["progress_nm"] = 0.0

# ---------------------------
# 7) Φόρτωση συντεταγμένων + Υπολογισμός απόστασης
# ---------------------------
coords = st.session_state["routes"][st.session_state["selected_route"]]
current_dist = st.session_state["current_dist_nm"]  # Ολική απόσταση σε NM
progress_so_far = st.session_state["progress_nm"]   # Διανυθείσα απόσταση σε NM

# ---------------------------
# 8) Δημιουργία Χάρτη
# ---------------------------
m = folium.Map(location=coords[0], zoom_start=6)

# Σημείο Αφετηρίας
folium.Marker(coords[0], tooltip="Start").add_to(m)
# Σημείο Προορισμού
folium.Marker(coords[1], tooltip="Destination").add_to(m)

# Υπολογίζουμε πόση διαδρομή απομένει
remaining_nm = current_dist - progress_so_far
if remaining_nm < 0:
    remaining_nm = 0

st.write(f"**Total Route Distance**: ~{current_dist:.2f} NM")
st.write(f"**Ship has traveled**: ~{progress_so_far:.2f} NM")
st.write(f"**Remaining**: ~{remaining_nm:.2f} NM")

# ---------------------------
# 9) Ρίψη Ζαριού & Μετακίνηση Σκάφους
# ---------------------------
if st.button("Roll the Dice 🎲"):
    dice_value = random.randint(1, 6)
    st.success(f"You rolled: {dice_value}")

    # Για κάθε βήμα = 1 NM, μέχρι το dice_value
    # ή μέχρι να φτάσουμε στο τέλος
    steps_to_move = min(dice_value, remaining_nm)  # αν φτάνουμε στο τέλος
    steps_to_move = int(steps_to_move)            # π.χ. αν remaining είναι 3.2 και dice_value=6, κινούμαστε 3 βήματα

    for step in range(steps_to_move):
        # Αύξησε την πρόοδο κατά 1 NM
        st.session_state["progress_nm"] += 1
        # Νέα τιμή fraction (0 έως 1) = τρέχουσα_πρόοδος / συνολική_απόσταση
        fraction = st.session_state["progress_nm"] / current_dist

        # Μην ξεπερνάμε το 100%
        if fraction > 1:
            fraction = 1

        # Υπολόγισε το σημείο στο οποίο βρισκόμαστε
        lat1, lon1 = coords[0]
        lat2, lon2 = coords[1]

        current_lat = lat1 + fraction * (lat2 - lat1)
        current_lon = lon1 + fraction * (lon2 - lon1)

        # Τοποθέτησε ένα marker στο νέο σημείο
        folium.Marker([current_lat, current_lon],
                      icon=folium.Icon(color="blue"),
                      tooltip=f"Progress: {st.session_state['progress_nm']:.2f} NM").add_to(m)

        # Αυτό το time.sleep δεν θα παράξει “live animation” στο UI,
        # αλλά το αφήνουμε για να φαίνεται η λογική.
        time.sleep(0.5)

# ---------------------------
# 10) Εμφάνιση Χάρτη
# ---------------------------
st_folium(m, width=800, height=500)

# ---------------------------
# 11) Αν είμαστε Sponsor -> Διαφημίσεις
# ---------------------------
if role == "Sponsor":
    st.markdown("## 📢 Advertising Dashboard")
    st.write("View potential reach based on your chosen route.")
    
    reach = random.randint(5000, 50000)
    st.metric("Potential Engagement", f"{reach} impressions")

    if st.button("Start Campaign 🚀"):
        st.success("Campaign Launched Successfully!")

    st.markdown("## 🎭 Choose Passengers for Sponsored Content")
    passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
    selected_passenger = st.selectbox("Select a Passenger:", passengers)
    
    engagement = random.randint(1000, 10000)
    st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

# ---------------------------
# 12) Οπτικό Εφέ (iframe)
# ---------------------------
st.markdown("---")
st.markdown("""
<iframe src="https://lottiefiles.com/animations/boat-sailing"
        width="100%" height="400" frameborder="0" allowfullscreen>
</iframe>
""", unsafe_allow_html=True)
