import streamlit as st

# Φόρτωση CSS από αρχείο
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Αρχικοποίηση της σελίδας
st.set_page_config(page_title="AdOnBoard - Futuristic UI", layout="wide")

# Φόρτωση του CSS
load_css()

# UI
st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Futuristic Experience</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose your adventure in the world of maritime advertising.</p>", unsafe_allow_html=True)

# Επιλογές χρηστών
role = st.selectbox("Select Your Role:", ["Passenger", "Ship Owner", "Sponsor"])

if role == "Passenger":
    st.write("As a Passenger, you can explore new destinations and earn rewards for engagement.")

elif role == "Ship Owner":
    st.write("As a Ship Owner, you can list your routes and attract sponsors.")

elif role == "Sponsor":
    st.write("As a Sponsor, you can choose routes and advertise your brand.")

# Προσθήκη κουμπιού για έναρξη παιχνιδιού
if st.button("Start Game 🚀"):
    st.success("Game Started! Enjoy your journey! 🚢")

# Προσθήκη animation μέσω iframe
st.markdown("""
<iframe src="https://lottiefiles.com/animations/boat-sailing" width="100%" height="400" frameborder="0" allowfullscreen></iframe>
""", unsafe_allow_html=True)
