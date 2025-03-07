import streamlit as st
import folium
from streamlit_folium import folium_static
import time

# Διαθέσιμες διαδρομές
routes = {
    "Luxury Tour": {"start": [36.3932, 25.4615], "end": [37.4467, 25.3289], "desc": "VIP τουριστικό ταξίδι"},
    "Beach Party Route": {"start": [37.0856, 25.1478], "end": [36.7261, 25.2810], "desc": "Beach party και καλοκαίρι"},
    "Extreme Water Sports": {"start": [36.434, 28.217], "end": [36.892, 27.287], "desc": "Διαδρομή για watersports"},
    "Speed Challenge": {"start": [37.9838, 23.7275], "end": [37.2634, 23.1592], "desc": "Αγώνας ταχύτητας"}
}

# Επιλογή διαδρομής
st.title("⛵ Επιλογή Διαδρομής")
selected_route = st.selectbox("Επίλεξε τη διαδρομή σου:", list(routes.keys()))

# Δημιουργία χάρτη
map = folium.Map(location=[37.5, 24.5], zoom_start=6)

# Σχεδίαση διαδρομής
route_data = routes[selected_route]
folium.Marker(route_data["start"], tooltip="Αφετηρία", icon=folium.Icon(color="green")).add_to(map)
folium.Marker(route_data["end"], tooltip="Προορισμός", icon=folium.Icon(color="red")).add_to(map)
folium.PolyLine([route_data["start"], route_data["end"]], color="blue", weight=5).add_to(map)

# Εμφάνιση χάρτη
folium_static(map)

# Προσομοίωση κίνησης του σκάφους
if st.button("🚀 Ξεκίνα το ταξίδι"):
    st.write(f"🏁 Το σκάφος σου ξεκινά το ταξίδι: {selected_route}!")

    # Προσθήκη animation
    progress_bar = st.progress(0)
    steps = 10
    for i in range(steps):
        progress_bar.progress((i + 1) / steps)
        time.sleep(0.5)

    st.success(f"🎉 Έφτασες στον προορισμό σου! {route_data['desc']}")
