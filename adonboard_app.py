Παρακάτω θα βρεις έναν απλοποιημένο και λειτουργικό κώδικα που σε κάθε ρίψη ζαριού μετακινεί το σκάφος κατά ολόκληρο τον αριθμό του ζαριού (π.χ. 4) σε ναυτικά μίλια πάνω στην επιλεγμένη διαδρομή (χωρίς να βλέπεις σταδιακά βήμα-βήμα).

Αν λείπουν περισσότερα NM από όσα “δίνει” το ζάρι, το σκάφος απλώς θα φτάσει στο τέλος.

Σε κάθε ρίψη, βλέπεις ένα νέο marker με την τελική θέση του σκάφους.

Ο κώδικας διατηρεί (με session_state) την πρόοδο σε NM για την τρέχουσα διαδρομή, έτσι ώστε σε επόμενη ρίψη να συνεχίσει από το τελευταίο σημείο.

Αν θες “κανονικό animation” (να βλέπεις σε πραγματικό χρόνο την κίνηση), απαιτείται πιο προχωρημένη προσέγγιση με επαναλαμβανόμενα refresh ή sockets, αλλά ο παρακάτω κώδικας αρκεί για να βλέπεις την επόμενη θέση του σκάφους σε κάθε ρίψη.



---

app.py

import streamlit as st
import random
import time
import math
import folium
from streamlit_folium import st_folium

# ---------------------------
# 1) Σταθερές και Συναρτήσεις
# ---------------------------
EARTH_RADIUS_KM = 6371.0
KM_TO_NM = 0.539957  # 1 km ≈ 0.54 nautical miles

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
    """Υπολογίζει την απόσταση σε Ναυτικά Μίλια (NM) μεταξύ δύο σημείων."""
    dist_km = haversine_distance_km(lat1, lon1, lat2, lon2)
    return dist_km * KM_TO_NM

def load_css():
    """Προαιρετική φόρτωση custom CSS."""
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# ---------------------------
# 2) Ρυθμίσεις σελίδας
# ---------------------------
st.set_page_config(page_title="AdOnBoard - Futuristic UI", layout="wide")
load_css()

st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Futuristic Experience</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose your role in the world of maritime advertising.</p>", unsafe_allow_html=True)

# ---------------------------
# 3) Session State
# ---------------------------
if "routes" not in st.session_state:
    # Διαδρομές προεπιλογής
    st.session_state["routes"] = {
        "Santorini - Mykonos": [(36.3932, 25.4615), (37.4467, 25.3289)],
        "Rhodes - Athens": [(36.4349, 28.2176), (37.9838, 23.7275)]
    }

if "selected_route" not in st.session_state:
    # Αρχική επιλεγμένη διαδρομή
    st.session_state["selected_route"] = list(st.session_state["routes"].keys())[0]

if "current_dist_nm" not in st.session_state:
    # Ολική απόσταση διαδρομής (NM)
    coords = st.session_state["routes"][st.session_state["selected_route"]]
    st.session_state["current_dist_nm"] = distance_nm(*coords[0], *coords[1])

if "progress_nm" not in st.session_state:
    # Διανυθείσα απόσταση σε NM
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
# 5) Προσθήκη Δυναμικής Διαδρομής
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
selected_route = st.selectbox("Choose a Route:", list(st.session_state["routes"].keys()))

# Αν αλλάξει η διαδρομή από τον χρήστη, κάνουμε reset την πρόοδο
if selected_route != st.session_state["selected_route"]:
    st.session_state["selected_route"] = selected_route
    coords = st.session_state["routes"][selected_route]
    st.session_state["current_dist_nm"] = distance_nm(*coords[0], *coords[1])
    st.session_state["progress_nm"] = 0.0

# ---------------------------
# 7) Φόρτωση συντεταγμένων
# ---------------------------
coords = st.session_state["routes"][st.session_state["selected_route"]]
total_dist_nm = st.session_state["current_dist_nm"]
progress_nm = st.session_state["progress_nm"]

# Υπολογισμός των NM που απομένουν
remaining_nm = total_dist_nm - progress_nm
if remaining_nm < 0:
    remaining_nm = 0

st.write(f"**Total Route Distance:** ~{total_dist_nm:.2f} NM")
st.write(f"**Ship has traveled:** ~{progress_nm:.2f} NM")
st.write(f"**Remaining:** ~{remaining_nm:.2f} NM")

# ---------------------------
# 8) Δημιουργία Χάρτη
# ---------------------------
m = folium.Map(location=coords[0], zoom_start=6)

# Σημείο Αφετηρίας & Προορισμού
folium.Marker(coords[0], tooltip="Start").add_to(m)
folium.Marker(coords[1], tooltip="Destination").add_to(m)

# Υπολογίζουμε την τρέχουσα θέση του σκάφους από το fraction της διαδρομής
if total_dist_nm > 0:
    fraction = progress_nm / total_dist_nm
    if fraction > 1:
        fraction = 1.0
else:
    fraction = 0

lat1, lon1 = coords[0]
lat2, lon2 = coords[1]
current_lat = lat1 + fraction * (lat2 - lat1)
current_lon = lon1 + fraction * (lon2 - lon1)

# Marker τρέχουσας θέσης
folium.Marker(
    [current_lat, current_lon],
    icon=folium.Icon(color="blue"),
    tooltip=f"Ship Position: {progress_nm:.2f} / {total_dist_nm:.2f} NM"
).add_to(m)

# ---------------------------
# 9) Ρίψη Ζαριού & Μετακίνηση
# ---------------------------
if st.button("Roll the Dice 🎲"):
    dice_value = random.randint(1, 6)
    st.success(f"You rolled: {dice_value}")

    # Μετακινούμαστε κατά dice_value NM ή μέχρι το τέλος
    move_nm = min(dice_value, remaining_nm)
    st.session_state["progress_nm"] += move_nm

    st.info(f"The ship moved {move_nm:.2f} NM forward.")

# ---------------------------
# 10) Προβολή Χάρτη
# ---------------------------
st_folium(m, width=800, height=500)

# ---------------------------
# 11) Advertising (αν είμαστε Sponsor)
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

