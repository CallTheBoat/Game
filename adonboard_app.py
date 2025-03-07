import streamlit as st

# Λίστα διαθέσιμων σκαφών με εικόνες και περιγραφές
boats = {
    "🚤 Luxury Yacht": {
        "img": "https://cdn.pixabay.com/photo/2017/06/04/19/47/yacht-2378329_960_720.jpg",
        "desc": "Ιδανικό για VIP εμπειρίες και πολυτελή ταξίδια.",
        "capacity": 10
    },
    "⛵ Catamaran": {
        "img": "https://cdn.pixabay.com/photo/2016/03/26/22/14/boat-1286060_960_720.jpg",
        "desc": "Σταθερό και ιδανικό για ταξίδια με πολλούς επιβάτες.",
        "capacity": 8
    },
    "🚀 Speed Boat": {
        "img": "https://cdn.pixabay.com/photo/2017/07/31/22/33/speedboat-2564120_960_720.jpg",
        "desc": "Γρήγορο και δυναμικό για περιπέτειες στο νερό.",
        "capacity": 6
    },
    "🌊 Classic Sailboat": {
        "img": "https://cdn.pixabay.com/photo/2016/11/19/12/42/sailing-boat-1834310_960_720.jpg",
        "desc": "Παραδοσιακό ιστιοπλοϊκό για χαλαρές αποδράσεις.",
        "capacity": 5
    }
}

# Τίτλος
st.title("⛵ Επιλογή Σκάφους για το Ταξίδι")

# Δυναμική παρουσίαση των σκαφών
selected_boat = None
for name, details in boats.items():
    col1, col2 = st.columns([1, 2])  # Χωρίζουμε τη σελίδα για εικόνα + περιγραφή
    with col1:
        st.image(details["img"], width=150)  # Φωτογραφία του σκάφους
    with col2:
        st.subheader(name)
        st.write(details["desc"])
        st.write(f"👥 Χωρητικότητα: {details['capacity']} άτομα")
        if st.button(f"🚢 Επιλογή {name}"):
            selected_boat = name

# Αποθήκευση επιλογής
if selected_boat:
    st.session_state["boat"] = selected_boat
    st.success(f"✅ Επέλεξες: {selected_boat}! Ετοιμάσου για το ταξίδι!")
