import streamlit as st

# Φόρτωση CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Αρχικοποίηση της σελίδας
st.set_page_config(page_title="AdOnBoard - Futuristic UI", layout="wide")

# Φόρτωση CSS
load_css()

# UI
st.markdown("<h1 style='text-align: center;'>🚢 AdOnBoard - The Futuristic Experience</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose your adventure in the world of maritime advertising.</p>", unsafe_allow_html=True)

# Προσθήκη κουμπιού
if st.button("Start Game"):
    st.success("Game Started! 🚀")

# Ενσωμάτωση animation (με iframe)
st.markdown("""
<iframe src="https://lottiefiles.com/animations/boat-sailing" width="100%" height="400" frameborder="0" allowfullscreen></iframe>
""", unsafe_allow_html=True)
