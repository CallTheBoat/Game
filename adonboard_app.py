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
st.set_page_config(page_title="AdOnBoard - Maritime Monopoly", layout="wide")

# Φόρτωση CSS
load_css()

# Διάταξη σελίδας (Αριστερά: Διαφήμιση - Δεξιά: Παιχνίδι)
col1, col2 = st.columns([1, 3])

# 🎥 **Αριστερή Στήλη: NEXT Campaign Video**
with col1:
    st.markdown("### 📢 NEXT Advertising Campaign")
    st.video("https://www.youtube.com/watch?v=Fvn51iy9dy8")
    st.markdown("**Join the future of maritime advertising with NEXT!**")

# 🎲 **Δεξιά Στήλη: Παιχνίδι & Δρομολόγια**
with col2:
    st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Maritime Monopoly Experience</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Choose your role and start your maritime journey!</p>", unsafe_allow_html=True)

    # 🔹 **Επιλογή Ρόλου**
    role = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])

    if role == "Passenger":
        st.write("🌊 Travel between islands, share experiences, and gain sponsorships!")

    elif role == "Ship Owner":
        st.write("⚓ List your ships, choose profitable routes, and attract sponsors.")

    elif role == "Sponsor":
        st.write("📢 Advertise on popular sea routes and track engagement statistics.")

    # 🗺️ **Διαδρομές Πλοίων με Χορηγούς**
    routes = {
        "Santorini - Mykonos": {"coords": [(36.3932, 25.4615), (37.4467, 25.3289)], "sponsor": "Vodafone"},
        "Rhodes - Athens": {"coords": [(36.4349, 28.2176), (37.9838, 23.7275)], "sponsor": "Nike"},
        "Crete - Mykonos": {"coords": [(35.341, 25.133), (37.4467, 25.3289)], "sponsor": "Coca-Cola"},
        "Athens - Santorini": {"coords": [(37.9838, 23.7275), (36.3932, 25.4615)], "sponsor": "Adidas"}
    }

    selected_route = st.selectbox("Choose a Route:", list(routes.keys()))

    # 🗺️ **Δημιουργία Monopoly-style Χάρτη**
    m = folium.Map(location=routes[selected_route]["coords"][0], zoom_start=6)

    # Σημάδια εκκίνησης και προορισμού
    folium.Marker(routes[selected_route]["coords"][0], tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(routes[selected_route]["coords"][1], tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)

    # **Σήμανση του χορηγού**
    sponsor = routes[selected_route]["sponsor"]
    st.markdown(f"🏷 **Sponsor:** {sponsor}")

    # **Διαδρομή στο χάρτη**
    folium.PolyLine(routes[selected_route]["coords"], color="blue", weight=5, tooltip="Route").add_to(m)

    # 🎲 **Ρίψη Ζαριού και Προώθηση Πλοίου**
    if st.button("Roll the Dice 🎲"):
        dice_value = random.randint(1, 6)
        st.success(f"You rolled: {dice_value}")

        # Προσομοίωση κίνησης πλοίου
        for step in range(dice_value):
            lat_step = routes[selected_route]["coords"][0][0] + (step * 0.1)
            lon_step = routes[selected_route]["coords"][0][1] + (step * 0.1)
            folium.Marker([lat_step, lon_step], icon=folium.Icon(color="blue")).add_to(m)
            time.sleep(0.5)

    # 🗺️ **Προβολή Monopoly-style Χάρτη**
    st_folium(m, width=800, height=500)

    # 📢 **Χορηγίες & Διαφημίσεις**
    if role == "Sponsor":
        st.markdown("## 📢 Advertising Dashboard")
        st.write("View potential reach based on your chosen route.")
        
        reach = random.randint(5000, 50000)
        st.metric("Potential Engagement", f"{reach} impressions")

        if st.button("Start Campaign 🚀"):
            st.success("Campaign Launched Successfully!")

    # 🎭 **Επιλογή Επιβατών για Χορηγίες**
    if role == "Sponsor":
        st.markdown("## 🎭 Choose Passengers for Sponsored Content")
        passengers = ["Dimitris Chatzi", "Maria Kosta", "Alex Papadopoulos"]
        selected_passenger = st.selectbox("Select a Passenger:", passengers)

        engagement = random.randint(1000, 10000)
        st.metric(f"Estimated Engagement for {selected_passenger}", f"{engagement} views")

st.markdown("---")

# 🚢 **Animation με Lottie**
st.markdown("""
<iframe src="https://lottiefiles.com/animations/boat-sailing" width="100%" height="400" frameborder="0" allowfullscreen></iframe>
""", unsafe_allow_html=True)
