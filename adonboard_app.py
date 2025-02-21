import streamlit as st
import folium
from streamlit_folium import folium_static
import time
import random
import numpy as np
import requests

# 🔄 Real-Time Weather API (Ανοίγει δυνατότητες για το simulator)
def get_weather(location):
    API_KEY = "YOUR_OPENWEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={location[0]}&lon={location[1]}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return response.get("weather", [{}])[0].get("description", "No Data"), response.get("wind", {}).get("speed", 0)

# 📦 Trading System - Αγορά/Πώληση Προϊόντων
products = {
    "Φρέσκο Ψάρι 🐟": {"buy_price": 100, "sell_price": 130},
    "Ναυτιλιακά Καύσιμα ⛽": {"buy_price": 500, "sell_price": 700},
    "Luxury Drinks 🍷": {"buy_price": 200, "sell_price": 280},
    "Εξοπλισμός Καταδύσεων 🤿": {"buy_price": 300, "sell_price": 400}
}

# 🎲 Multiplayer Mode
st.title("🌊 AdOnBoard Multiplayer Game")
num_players = st.slider("👥 Πόσοι παίκτες θα παίξουν;", 1, 4, 2)
players = {}

for i in range(num_players):
    player_name = st.text_input(f"🎮 Όνομα Παίκτη {i+1}:", f"Παίκτης {i+1}")
    players[player_name] = {"money": 100000, "cargo": {}, "location": [37.9838, 23.7275]}  # Αθήνα ως αρχική θέση

# 🚢 Επιλογή Διαδρομής & Καιρός
st.title("🌍 Επιλογή Διαδρομής")
routes = {
    "Luxury Tour 🌟": {"start": [36.3932, 25.4615], "end": [37.4467, 25.3289]},
    "Extreme Water Sports 🏄": {"start": [36.434, 28.217], "end": [36.892, 27.287]},
    "Speed Challenge 🏎️": {"start": [37.9838, 23.7275], "end": [37.2634, 23.1592]}
}
selected_route = st.selectbox("📍 **Επέλεξε διαδρομή:**", list(routes.keys()))
route_data = routes[selected_route]

weather_desc, wind_speed = get_weather(route_data["start"])

st.write(f"🌤 **Καιρός στη διαδρομή:** {weather_desc}")
st.write(f"💨 **Ταχύτητα Ανέμου:** {wind_speed} m/s (επηρεάζει την ταχύτητα του σκάφους)")

# 🚢 Χάρτης με Κινούμενα Σκάφη
map = folium.Map(location=[37.5, 24.5], zoom_start=6, tiles="Stamen Terrain")
folium.Marker(route_data["start"], tooltip="Αφετηρία", icon=folium.Icon(color="green", icon="cloud")).add_to(map)
folium.Marker(route_data["end"], tooltip="Προορισμός", icon=folium.Icon(color="red", icon="flag")).add_to(map)

if st.button("⚡ Ξεκίνα το ταξίδι"):
    st.write(f"🏁 **Το σκάφος ξεκινά:** {selected_route}!")

    progress_bar = st.progress(0)
    lat_steps = np.linspace(route_data["start"][0], route_data["end"][0], 10)
    lon_steps = np.linspace(route_data["start"][1], route_data["end"][1], 10)

    for i in range(10):
        progress_bar.progress((i + 1) / 10)
        map = folium.Map(location=[lat_steps[i], lon_steps[i]], zoom_start=6, tiles="Stamen Terrain")
        folium.Marker([lat_steps[i], lon_steps[i]], icon=folium.Icon(color="blue", icon="ship")).add_to(map)
        folium.PolyLine([route_data["start"], route_data["end"]], color="cyan", weight=6, opacity=0.7).add_to(map)
        folium_static(map)
        time.sleep(0.5 - (wind_speed * 0.03))  # Ρύθμιση ταχύτητας ταξιδιού με βάση τον άνεμο

    st.success("🎉 **Το ταξίδι ολοκληρώθηκε!**")

# 💰 Trading System - Αγορές/Πωλήσεις
st.title("📦 Trading System")
for player in players.keys():
    st.subheader(f"{player}")
    for product in products.keys():
        if st.button(f"Αγορά {product} για {player} ({products[product]['buy_price']}€)"):
            if players[player]["money"] >= products[product]["buy_price"]:
                players[player]["money"] -= products[product]["buy_price"]
                players[player]["cargo"][product] = players[player]["cargo"].get(product, 0) + 1
                st.success(f"✔ {player} αγόρασε {product}!")
            else:
                st.error("❌ Δεν έχεις αρκετά χρήματα!")
    
    for product in list(players[player]["cargo"].keys()):
        if st.button(f"Πώληση {product} από {player} ({products[product]['sell_price']}€)"):
            if players[player]["cargo"][product] > 0:
                players[player]["money"] += products[product]["sell_price"]
                players[player]["cargo"][product] -= 1
                if players[player]["cargo"][product] == 0:
                    del players[player]["cargo"][product]
                st.success(f"✔ {player} πούλησε {product}!")
            else:
                st.error("❌ Δεν έχεις προϊόντα προς πώληση!")

# 🏆 Leaderboard
st.title("🏆 Κατάταξη Παικτών")
sorted_players = sorted(players.items(), key=lambda x: x[1]["money"], reverse=True)
for i, (player, data) in enumerate(sorted_players):
    st.write(f"**{i+1}. {player}** - 💰 {data['money']}€ | 📦 Εμπόρευμα: {list(data['cargo'].keys())}")

# 🚢 Σύνδεση με Προσομοιωτή Γέφυρας (Προετοιμασία)
st.title("🔗 Σύνδεση με Προσομοιωτή Γέφυρας")
st.write("📡 **Σύνδεση σε εξέλιξη!** Σύντομα θα μπορείς να ελέγχεις το σκάφος στον **προσομοιωτή γέφυρας**.")
st.write("🔧 **Θα χρειαστεί API σύνδεση για επικοινωνία με το simulator σου.**")

