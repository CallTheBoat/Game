import streamlit as st
import folium
from streamlit_folium import folium_static
import time

st.set_page_config(page_title="AdOnBoard Game", layout="wide")

# 🎲 Βήμα 1: Επιλογή Ρόλου Παίκτη
st.title("🌊 AdOnBoard - Επιτραπέζιο Ναυτιλίας 🚢")
roles = {
    "🛥️ Πλοιοκτήτης": "Διαχειρίζεται το σκάφος, επιλέγει δρομολόγια, αναζητά χορηγούς.",
    "🧑‍✈️ Επιβάτης": "Ταξιδεύει, κάνει social media αναρτήσεις και κερδίζει likes.",
    "💰 Χορηγός": "Προσφέρει χρήματα και επιλέγει διαφημιστικές τοποθετήσεις."
}
selected_role = st.radio("📌 **Επίλεξε τον ρόλο σου**:", list(roles.keys()))
st.info(roles[selected_role])

if st.button("✅ Επιβεβαίωση και Συνέχεια"):
    st.session_state["role"] = selected_role
    st.success(f"🎉 Επέλεξες: {selected_role}! Ετοιμάσου για το παιχνίδι!")

# 🚢 Βήμα 2: Επιλογή Σκάφους
boats = {
    "🚤 Luxury Yacht": {"img": "https://cdn.pixabay.com/photo/2017/06/04/19/47/yacht-2378329_960_720.jpg", "desc": "VIP εμπειρία", "capacity": 10},
    "⛵ Catamaran": {"img": "https://cdn.pixabay.com/photo/2016/03/26/22/14/boat-1286060_960_720.jpg", "desc": "Σταθερό και ιδανικό για ταξίδια", "capacity": 8},
    "🚀 Speed Boat": {"img": "https://cdn.pixabay.com/photo/2017/07/31/22/33/speedboat-2564120_960_720.jpg", "desc": "Γρήγορο και δυναμικό", "capacity": 6}
}
st.title("⛵ Επιλογή Σκάφους για το Ταξίδι")
selected_boat = st.selectbox("📌 Επέλεξε το σκάφος σου:", list(boats.keys()))
st.image(boats[selected_boat]["img"], width=300)
st.write(boats[selected_boat]["desc"])

if st.button("🚢 Επιβεβαίωση Σκάφους"):
    st.session_state["boat"] = selected_boat
    st.success(f"✅ Επέλεξες το {selected_boat}!")

# 🏆 Βήμα 3: Επιλογή Χορηγού
sponsors = {
    "🚀 Red Bull Sailing": {"img": "https://upload.wikimedia.org/wikipedia/commons/d/d1/RedBull_Racing_2018.jpg", "bonus": "+10% Ταχύτητα"},
    "🥤 Coca-Cola Beach Club": {"img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Coca-Cola_logo.svg", "bonus": "+20% Κέρδη στις παραλίες"},
    "🏄 Nike Aqua Sports": {"img": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Nike_logo.svg", "bonus": "+15% Events και extreme sports"}
}
st.title("🏆 Επιλογή Χορηγού")
selected_sponsor = st.selectbox("📌 Επίλεξε χορηγό:", list(sponsors.keys()))
st.image(sponsors[selected_sponsor]["img"], width=200)
st.write(f"🎁 **Μπόνους:** {sponsors[selected_sponsor]['bonus']}")

if st.button("✅ Επιβεβαίωση Χορηγού"):
    st.session_state["sponsor"] = selected_sponsor
    st.success(f"🎉 Έχεις χορηγό τον {selected_sponsor}!")

# 🗺️ Βήμα 4: Επιλογή Διαδρομής και Προβολή στο Χάρτη
routes = {
    "Luxury Tour": {"start": [36.3932, 25.4615], "end": [37.4467, 25.3289], "desc": "VIP τουριστικό ταξίδι", "bonus": "+25% από Greek Islands Luxury"},
    "Beach Party Route": {"start": [37.0856, 25.1478], "end": [36.7261, 25.2810], "desc": "Beach party και παραλίες", "bonus": "+20% από Coca-Cola Beach"},
    "Extreme Water Sports": {"start": [36.434, 28.217], "end": [36.892, 27.287], "desc": "Events με extreme sports", "bonus": "+15% από Nike Aqua"},
    "Speed Challenge": {"start": [37.9838, 23.7275], "end": [37.2634, 23.1592], "desc": "Αγώνας ταχύτητας", "bonus": "+10% από Red Bull"}
}
st.title("⛵ Επιλογή Διαδρομής")
selected_route = st.selectbox("📌 Επίλεξε διαδρομή:", list(routes.keys()))
route_data = routes[selected_route]

# Δημιουργία δυναμικού χάρτη με διαδρομές
map = folium.Map(location=[37.5, 24.5], zoom_start=6)
folium.Marker(route_data["start"], tooltip="Αφετηρία", icon=folium.Icon(color="green")).add_to(map)
folium.Marker(route_data["end"], tooltip="Προορισμός", icon=folium.Icon(color="red")).add_to(map)
folium.PolyLine([route_data["start"], route_data["end"]], color="blue", weight=5).add_to(map)
folium_static(map)

st.write(f"📝 Περιγραφή: {route_data['desc']}")
st.write(f"🎯 Μπόνους: {route_data['bonus']}")

# Προσομοίωση κίνησης του σκάφους
if st.button("🚀 Ξεκίνα το ταξίδι"):
    st.write(f"🏁 Το σκάφος ξεκινά: {selected_route}!")
    progress_bar = st.progress(0)
    for i in range(10):
        progress_bar.progress((i + 1) / 10)
        time.sleep(0.5)
    st.success(f"🎉 Έφτασες στον προορισμό σου! {route_data['desc']}")

# 🏆 Υπολογισμός Κερδών με βάση τον Χορηγό
earnings = 100000  # Βασικό ποσό για τη διαδρομή
if selected_sponsor == "🚀 Red Bull Sailing" and selected_route == "Speed Challenge":
    earnings *= 1.1
elif selected_sponsor == "🥤 Coca-Cola Beach Club" and selected_route == "Beach Party Route":
    earnings *= 1.2
elif selected_sponsor == "🏄 Nike Aqua Sports" and selected_route == "Extreme Water Sports":
    earnings *= 1.15
elif selected_sponsor == "💎 Greek Islands Luxury Tours" and selected_route == "Luxury Tour":
    earnings *= 1.25

st.title("💰 Συνολικά Κέρδη")
st.write(f"📈 Τα κέρδη σου από τη διαδρομή: **{earnings:.2f}€**")

