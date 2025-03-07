import streamlit as st
import folium
from streamlit_folium import folium_static
import time

# 💡 Custom Background Image με θαλάσσιο θέμα
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()

# 🌊 UI Styling - Modern Transparent Panels
st.markdown(
    """
    <style>
    .floating-panel {
        background: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 15px;
        color: white;
        position: fixed;
        top: 20px;
        right: 20px;
        width: 320px;
        box-shadow: 0px 5px 25px rgba(255,255,255,0.2);
    }
    .stButton>button {
        background: linear-gradient(135deg, #0077be, #00aaff);
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎲 Επιλογή Διαδρομής με Ανανεωμένα Εικονίδια
st.title("🌊 Επιλογή Διαδρομής")
routes = {
    "Luxury Tour 🌟": {"start": [36.3932, 25.4615], "end": [37.4467, 25.3289], "desc": "VIP τουριστικό ταξίδι"},
    "Beach Party Route 🎉": {"start": [37.0856, 25.1478], "end": [36.7261, 25.2810], "desc": "Beach party και παραλίες"},
    "Extreme Water Sports 🏄": {"start": [36.434, 28.217], "end": [36.892, 27.287], "desc": "Watersports και extreme events"},
    "Speed Challenge 🏎️": {"start": [37.9838, 23.7275], "end": [37.2634, 23.1592], "desc": "Γρήγορη διαδρομή για αγώνες ταχύτητας"}
}
selected_route = st.selectbox("📍 **Επέλεξε διαδρομή:**", list(routes.keys()))
route_data = routes[selected_route]

# 🌍 Δημιουργία δυναμικού χάρτη με νέα εικονίδια
map = folium.Map(location=[37.5, 24.5], zoom_start=6, tiles="Stamen Terrain")
folium.Marker(route_data["start"], tooltip="Αφετηρία", icon=folium.Icon(color="green", icon="cloud")).add_to(map)
folium.Marker(route_data["end"], tooltip="Προορισμός", icon=folium.Icon(color="red", icon="flag")).add_to(map)
folium.PolyLine([route_data["start"], route_data["end"]], color="cyan", weight=6, opacity=0.7).add_to(map)
folium_static(map)

st.write(f"📝 **Περιγραφή:** {route_data['desc']}")

# 🚀 Προσθήκη Animation για Κίνηση Σκάφους
if st.button("⚡ Ξεκίνα το ταξίδι"):
    st.write(f"🏁 **Το σκάφος ξεκινά:** {selected_route}!")

    # ⚓ Progress Bar για την κίνηση του σκάφους
    progress_bar = st.progress(0)
    for i in range(12):
        progress_bar.progress((i + 1) / 12)
        time.sleep(0.4)

    st.success(f"🎉 **Έφτασες στον προορισμό σου!** {route_data['desc']}")

# 🏆 Floating Panel με Live Πληροφορίες
st.markdown(
    f"""
    <div class="floating-panel">
        <h3>🎮 Κατάσταση Παιχνιδιού</h3>
        <p>🚢 **Διαδρομή:** {selected_route}</p>
        <p>📍 **Αφετηρία:** {route_data['start']}</p>
        <p>🏁 **Προορισμός:** {route_data['end']}</p>
        <p>💰 **Κέρδη:** 120,000€ + Bonus</p>
    </div>
    """,
    unsafe_allow_html=True
)
