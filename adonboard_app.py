import streamlit as st

# Τίτλος του παιχνιδιού
st.title("🌊 AdOnBoard - Επιτραπέζιο Ναυτιλίας 🚢")

# Περιγραφή του παιχνιδιού
st.markdown("**Επέλεξε τον ρόλο σου για να ξεκινήσεις!**")

# Λίστα ρόλων
roles = {
    "🛥️ Πλοιοκτήτης": "Διαχειρίζεται το σκάφος, επιλέγει δρομολόγια, αναζητά χορηγούς.",
    "🧑‍✈️ Επιβάτης": "Ταξιδεύει, κάνει social media αναρτήσεις και κερδίζει likes.",
    "💰 Χορηγός": "Προσφέρει χρήματα και επιλέγει διαφημιστικές τοποθετήσεις."
}

# Επιλογή ρόλου
selected_role = st.radio("📌 **Επίλεξε τον ρόλο σου**:", list(roles.keys()))

# Εμφάνιση πληροφοριών για τον ρόλο
st.info(roles[selected_role])

# Κουμπί για να προχωρήσει στο επόμενο στάδιο
if st.button("✅ Επιβεβαίωση και Συνέχεια"):
    st.session_state["role"] = selected_role
    st.success(f"🎉 Επέλεξες: {selected_role}! Ετοιμάσου για το παιχνίδι!")
