import streamlit as st

# Διαθέσιμοι χορηγοί με εικόνες και περιγραφές
sponsors = {
    "🚀 Red Bull Sailing Team": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/RedBull_Racing_2018.jpg/800px-RedBull_Racing_2018.jpg",
        "desc": "Ιδανικός για γρήγορα και δυναμικά σκάφη. Δίνει μπόνους στην ταχύτητα.",
        "bonus": "🚀 +10% Ταχύτητα σε κάθε διαδρομή!"
    },
    "🥤 Coca-Cola Beach Club": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Coca-Cola_logo.svg/800px-Coca-Cola_logo.svg.png",
        "desc": "Χορηγεί σκάφη που ταξιδεύουν σε δημοφιλείς παραλίες.",
        "bonus": "💰 +20% Κέρδη όταν περνάς από παραλίες με κόσμο!"
    },
    "🏄 Nike Aqua Sports": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Nike_logo.svg/800px-Nike_logo.svg.png",
        "desc": "Δίνει μπόνους σε extreme sports events και watersports στάσεις.",
        "bonus": "🎯 +15% Πόντους όταν σταματάς σε events με extreme sports!"
    },
    "💎 Greek Islands Luxury Tours": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Santorini_Caldera.jpg/800px-Santorini_Caldera.jpg",
        "desc": "Χορηγεί πολυτελή σκάφη και VIP τουριστικές διαδρομές.",
        "bonus": "🎩 +25% Μπόνους στα VIP τουριστικά πακέτα!"
    }
}

# Τίτλος
st.title("🏆 Επιλογή Χορηγού για το Σκάφος")

# Δυναμική παρουσίαση των χορηγών
selected_sponsor = None
for name, details in sponsors.items():
    col1, col2 = st.columns([1, 2])  # Χωρίζουμε τη σελίδα για εικόνα + περιγραφή
    with col1:
        st.image(details["img"], width=150)  # Φωτογραφία του χορηγού
    with col2:
        st.subheader(name)
        st.write(details["desc"])
        st.write(f"🎁 **Μπόνους:** {details['bonus']}")
        if st.button(f"✅ Επιλογή {name}"):
            selected_sponsor = name

# Αποθήκευση επιλογής
if selected_sponsor:
    st.session_state["sponsor"] = selected_sponsor
    st.success(f"✅ Έχεις πλέον χορηγό τον {selected_sponsor}! Το ταξίδι σου γίνεται πιο προσοδοφόρο!")
