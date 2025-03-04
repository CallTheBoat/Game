import streamlit as st
import random
import time
import folium
from streamlit_folium import st_folium

# Φόρτωση CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Αρχικοποίηση σελίδας
st.set_page_config(page_title="AdOnBoard - Futuristic UI", layout="wide")

# Φόρτωση CSS
load_css()

# Τίτλος
st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Futuristic Experience</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose your role in the world of maritime advertising.</p>", unsafe_allow_html=True)

# Επιλογή ρόλου
role = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])

if role == "Passenger":
    st.write("Explore destinations, earn rewards, and interact with sponsors.")

elif role == "Ship Owner":
    st.write("List your routes, attract sponsors, and maximize profits.")

elif role == "Sponsor":
    st.write("Choose routes, advertise your brand, and track engagement.")

# Επιλογή διαδρομής
routes = {
    "Santorini - Mykonos": [(36.3932, 25.4615), (37.4467, 25.3289)],
    "Rhodes - Athens": [(36.4349, 28.2176), (37.9838, 23.7275)]
}

selected_route = st.selectbox("Choose a Route:", list(routes.keys()))

# Δημιουργία χάρτη με κινούμενο πλοίο
m = folium.Map(location=routes[selected_route][0], zoom_start=6)
folium.Marker(routes[selected_route][0], tooltip="Start").add_to(m)
folium.Marker(routes[selected_route][1], tooltip="Destination").add_to(m)

# Κουμπί για ρίψη ζαριού & προώθηση πλοίου
if st.button("Roll the Dice 🎲"):
    dice_value = random.randint(1, 6)
    st.success(f"You rolled: {dice_value}")

    # Προσομοίωση κίνησης πλοίου
    for step in range(dice_value):
        lat_step = routes[selected_route][0][0] + (step * 0.1)
        lon_step = routes[selected_route][0][1] + (step * 0.1)
        folium.Marker([lat_step, lon_step], icon=folium.Icon(color="blue")).add_to(m)
        time.sleep(0.5)

# Προβολή χάρτη
st_folium(m, width=800, height=500)

# Χορηγίες & Διαφημίσεις
if role == "Sponsor":
    st.markdown("## 📢 Advertising Dashboard")
    st.write("View potential reach based on your chosen route.")
    
    reach = random.randint(5000, 50000)
    st.metric("Potential Engagement", f"{reach} impressions")

    if st.button("Start Campaign 🚀"):
        st.success("Campaign Launched Successfully!")

# Επιλογή επιβατών για διαφήμιση
if role == "Sponsor":
    st.markdown("## 🎭 Choose Passengers for Sponsored Content")
    passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
    selected_passenger = st.selectbox("Select a Passenger:", passengers)

    engagement = random.randint(1000, 10000)
    st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

st.markdown("---")

st.markdown("""
<iframe src="https://lottiefiles.com/animations/boat-sailing" width="100%" height="400" frameborder="0" allowfullscreen></iframe>
""", unsafe_allow_html=True)
