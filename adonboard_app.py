import folium
from streamlit_folium import st_folium
import time

# Δημιουργία του χάρτη
m = folium.Map(location=[37.9838, 23.7275], zoom_start=6)

# Συντεταγμένες των στάσεων του σκάφους
route = [
    [37.9838, 23.7275],  # Αθήνα
    [36.3932, 25.4615],  # Σαντορίνη
    [37.4467, 25.3289],  # Μύκονος
]

# Προσθήκη του σκάφους στον χάρτη
marker = folium.Marker(location=route[0], popup="🚢 Σκάφος", icon=folium.Icon(color="blue"))
marker.add_to(m)

# Προβολή χάρτη στο Streamlit
st_folium(m, width=700, height=500)

# Προσομοίωση κίνησης του σκάφους
for coords in route:
    marker.location = coords
    time.sleep(1)
    st_folium(m, width=700, height=500)
