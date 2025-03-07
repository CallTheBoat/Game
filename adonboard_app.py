import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import time

# ------------------------------ #
#       ΑΡΧΙΚΕΣ ΡΥΘΜΙΣΕΙΣ
# ------------------------------ #
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Ναυτιλίας", layout="wide")

# Προκαθορισμένες διαδρομές
routes = {
    "Σαντορίνη - Μύκονος": [[36.3932, 25.4615], [37.4467, 25.3289]],
    "Ρόδος - Αθήνα": [[36.4349, 28.2176], [37.9838, 23.7275]],
    "Κέρκυρα - Πάτρα": [[39.6243, 19.9217], [38.2466, 21.7346]]
}

# Επιλογή διαδρομής από τον παίκτη
selected_route = st.selectbox("Επέλεξε διαδρομή:", list(routes.keys()))
route_coordinates = routes[selected_route]

# ------------------------------ #
#       ΧΑΡΤΗΣ ΜΕ ΣΚΑΦΗ
# ------------------------------ #
st.header("🌊 AdOnBoard - Επιτραπέζιο Ναυτιλίας")

# Δημιουργία χάρτη Folium
map_center = route_coordinates[0]
m = folium.Map(location=map_center, zoom_start=6, tiles="CartoDB Positron")

# Προσθήκη των σημείων της διαδρομής
for coord in route_coordinates:
    folium.Marker(location=coord, icon=folium.Icon(color="blue", icon="ship", prefix="fa")).add_to(m)

# Προβολή του χάρτη
folium_static(m)

# ------------------------------ #
#       ΜΗΧΑΝΙΣΜΟΣ ΖΑΡΙΟΥ
# ------------------------------ #
st.sidebar.header("🎲 Ρίξε το ζάρι!")
if st.sidebar.button("Ρίξε το ζάρι!"):
    dice_roll = random.randint(1, 6)
    st.sidebar.write(f"🎲 Έφερες {dice_roll}!")

    # Προσομοίωση κίνησης του σκάφους
    progress_bar = st.progress(0)
    for i in range(dice_roll):
        time.sleep(0.5)
        progress_bar.progress((i + 1) / dice_roll)

    st.sidebar.success("Το σκάφος προχώρησε!")

# ------------------------------ #
#       ΣΥΣΤΗΜΑ ΧΟΡΗΓΙΩΝ
# ------------------------------ #
sponsors = ["Coca-Cola", "Nike", "Red Bull", "Samsung"]
selected_sponsor = st.sidebar.selectbox("Επέλεξε χορηγό:", sponsors)
st.sidebar.write(f"Ο χορηγός σου: {selected_sponsor}")

# ------------------------------ #
#       ΣΤΑΤΙΣΤΙΚΑ ΠΑΙΚΤΗ
# ------------------------------ #
st.sidebar.subheader("📊 Στατιστικά Παίκτη")
st.sidebar.write(f"👍 Likes: {random.randint(50, 500)}")
st.sidebar.write(f"💰 Χορηγικά Έσοδα: {random.randint(1000, 10000)}€")
st.sidebar.write(f"🏆 Εμπειρία: {random.randint(1, 10)} επίπεδο")

# ------------------------------ #
#       ΟΛΟΚΛΗΡΩΣΗ
# ------------------------------ #
st.success("🎮 Είσαι έτοιμος να παίξεις! Επιλογή διαδρομής, ρίξε το ζάρι και κέρδισε χορηγούς!")
