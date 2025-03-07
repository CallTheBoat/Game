import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import time

# ------------------------------ #
#       ΑΡΧΙΚΕΣ ΡΥΘΜΙΣΕΙΣ
# ------------------------------ #
st.set_page_config(page_title="AdOnBoard - Επιτραπέζιο Ναυτιλίας", layout="wide")

st.title("🚢 AdOnBoard - Επιτραπέζιο Ναυτιλίας")

# ------------------------------ #
#       ΕΠΙΛΟΓΗ ΡΟΛΟΥ ΠΑΙΚΤΗ
# ------------------------------ #
st.sidebar.header("🛠 Επιλέξτε Ρόλο")

role = st.sidebar.radio("Διάλεξε τον ρόλο σου:", ["🛳️ Πλοιοκτήτης", "🧑‍✈️ Επιβάτης", "💰 Χορηγός"])

if role == "🛳️ Πλοιοκτήτης":
    st.sidebar.subheader("⚓ Πλοιοκτήτης")
    st.sidebar.write("Διαχειρίζεσαι σκάφη και επιλέγεις διαδρομές.")
    ship_type = st.sidebar.selectbox("Επέλεξε τύπο σκάφους:", ["Luxury Yacht (10 άτομα)", "Catamaran (8 άτομα)", "Speedboat (5 άτομα)"])
    st.sidebar.write(f"🚤 Έχεις επιλέξει: {ship_type}")

elif role == "🧑‍✈️ Επιβάτης":
    st.sidebar.subheader("👥 Επιβάτης")
    st.sidebar.write("Διαλέγεις διαδρομές και συμμετέχεις στις εμπειρίες!")
    st.sidebar.write("Κέρδισε likes και χορηγίες μέσω των social media!")

elif role == "💰 Χορηγός":
    st.sidebar.subheader("💼 Χορηγός")
    st.sidebar.write("Επιλέγεις διαδρομές και προσφέρεις χορηγία σε επιβάτες και πλοιοκτήτες.")
    sponsor_name = st.sidebar.text_input("Όνομα χορηγού:")
    ad_budget = st.sidebar.slider("Προϋπολογισμός Χορηγίας (€)", 500, 50000, step=500)
    st.sidebar.write(f"🤑 Προσφέρεις χορηγία αξίας {ad_budget}€!")

# ------------------------------ #
#       ΕΠΙΛΟΓΗ ΔΙΑΔΡΟΜΗΣ
# ------------------------------ #
routes = {
    "Σαντορίνη - Μύκονος": [[36.3932, 25.4615], [37.4467, 25.3289]],
    "Ρόδος - Αθήνα": [[36.4349, 28.2176], [37.9838, 23.7275]],
    "Κέρκυρα - Πάτρα": [[39.6243, 19.9217], [38.2466, 21.7346]]
}

st.sidebar.header("🌍 Επιλογή Διαδρομής")
selected_route = st.sidebar.selectbox("Διάλεξε διαδρομή:", list(routes.keys()))
route_coordinates = routes[selected_route]

# ------------------------------ #
#       ΧΑΡΤΗΣ ΜΕ ΣΚΑΦΗ
# ------------------------------ #
st.header(f"🌊 Χάρτης Διαδρομής: {selected_route}")

map_center = route_coordinates[0]
m = folium.Map(location=map_center, zoom_start=6, tiles="CartoDB Positron")

for coord in route_coordinates:
    folium.Marker(location=coord, icon=folium.Icon(color="blue", icon="ship", prefix="fa")).add_to(m)

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

    st.sidebar.success("🚀 Το σκάφος προχώρησε στη διαδρομή!")

# ------------------------------ #
#       ΣΤΑΤΙΣΤΙΚΑ ΠΑΙΚΤΗ
# ------------------------------ #
st.sidebar.subheader("📊 Στατιστικά Παίκτη")
st.sidebar.write(f"👍 Likes: {random.randint(50, 500)}")
st.sidebar.write(f"💰 Χορηγικά Έσοδα: {random.randint(1000, 10000)}€")
st.sidebar.write(f"🏆 Εμπειρία: {random.randint(1, 10)} επίπεδο")

st.success("🎮 Είσαι έτοιμος να παίξεις! Επιλογή διαδρομής, ρίξε το ζάρι και κέρδισε χορηγούς!")
