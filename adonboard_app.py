import streamlit as st
import random
import time
import folium
from streamlit_folium import st_folium

# -------------------------------------
# 1) Προαιρετικά: Φόρτωση CSS από αρχείο
# -------------------------------------
def load_css():
    """Φόρτωση custom CSS (προαιρετικά)."""
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Αν δεν υπάρχει styles.css, προχωράμε

# -------------------------------------
# 2) Ρυθμίσεις σελίδας & φόρτωση CSS
# -------------------------------------
st.set_page_config(page_title="AdOnBoard - Futuristic UI", layout="wide")
load_css()

# -------------------------------------
# 3) Τίτλος & εισαγωγικό κείμενο
# -------------------------------------
st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Futuristic Experience</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose your role in the world of maritime advertising.</p>", unsafe_allow_html=True)

# -------------------------------------
# 4) Αρχικοποίηση Session State (Dynamic Routes)
# -------------------------------------
if "routes" not in st.session_state:
    st.session_state["routes"] = {
        "Santorini - Mykonos": [(36.3932, 25.4615), (37.4467, 25.3289)],
        "Rhodes - Athens": [(36.4349, 28.2176), (37.9838, 23.7275)]
    }

# -------------------------------------
# 5) Επιλογή Ρόλου
# -------------------------------------
role = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])

if role == "Passenger":
    st.write("Explore destinations, earn rewards, and interact with sponsors.")
elif role == "Ship Owner":
    st.write("List your routes, attract sponsors, and maximize profits.")
elif role == "Sponsor":
    st.write("Choose routes, advertise your brand, and track engagement.")

# -------------------------------------
# 6) Προσθήκη Δυναμικής Διαδρομής (φορμα)
# -------------------------------------
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

# -------------------------------------
# 7) Επιλογή Διαδρομής από το session_state
# -------------------------------------
selected_route = st.selectbox("Choose a Route:", list(st.session_state["routes"].keys()))
coords = st.session_state["routes"][selected_route]

# -------------------------------------
# 8) Δημιουργία χάρτη με τα σημεία
# -------------------------------------
m = folium.Map(location=coords[0], zoom_start=6)
folium.Marker(coords[0], tooltip="Start").add_to(m)
folium.Marker(coords[1], tooltip="Destination").add_to(m)

# -------------------------------------
# 9) Ρίψη Ζαριού & Προσομοίωση κίνησης πλοίου
# -------------------------------------
if st.button("Roll the Dice 🎲"):
    dice_value = random.randint(1, 6)
    st.success(f"You rolled: {dice_value}")
    
    # Απλή λογική προσέγγισης στο χάρτη (δείγμα)
    for step in range(dice_value):
        lat_step = coords[0][0] + (step * 0.1)
        lon_step = coords[0][1] + (step * 0.1)
        folium.Marker([lat_step, lon_step], icon=folium.Icon(color="blue")).add_to(m)
        time.sleep(0.5)

# Εμφάνιση χάρτη
st_folium(m, width=800, height=500)

# -------------------------------------
# 10) Διαφημίσεις & Χορηγοί
# -------------------------------------
if role == "Sponsor":
    st.markdown("## 📢 Advertising Dashboard")
    st.write("View potential reach based on your chosen route.")
    
    reach = random.randint(5000, 50000)
    st.metric("Potential Engagement", f"{reach} impressions")

    if st.button("Start Campaign 🚀"):
        st.success("Campaign Launched Successfully!")

    # Επιλογή επιβατών για διαφήμιση
    st.markdown("## 🎭 Choose Passengers for Sponsored Content")
    passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
    selected_passenger = st.selectbox("Select a Passenger:", passengers)
    
    engagement = random.randint(1000, 10000)
    st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

# -------------------------------------
# 11) Οπτικό εφέ (iframe ή Lottie) - Προαιρετικό
# -------------------------------------
st.markdown("---")
st.markdown("""
<iframe src="https://lottiefiles.com/animations/boat-sailing"
        width="100%" height="400" frameborder="0" allowfullscreen>
</iframe>
""", unsafe_allow_html=True)

