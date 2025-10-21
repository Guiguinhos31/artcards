import streamlit as st
import pandas as pd

from page_packs import page_packs
from page_collection import page_collection 
from page_defis import page_defis

# --- Configuration de base ---
st.set_page_config(page_title="ArtCards", page_icon="🎨", layout="wide")

# --- Chargement du CSV ---
try:
    cards = pd.read_csv("cartes50.csv")
except FileNotFoundError:
    st.error("⚠️ Le fichier cartes50.csv est introuvable.")
    st.stop()

# --- Initialisation de la session ---
if "collection" not in st.session_state:
    st.session_state.collection = []
if "days_connected" not in st.session_state:
    st.session_state.days_connected = 1
if "last_day" not in st.session_state:
    from datetime import datetime
    st.session_state.last_day = datetime.today().date()

# --- Barre de navigation latérale ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Aller à :",
    ["📦 Ouverture de packs", "🎴 Collection", "🏆 Défis"]
)

# --- Routage vers les pages ---
if page == "📦 Ouverture de packs":
    page_packs(cards)
elif page == "🎴 Collection":
    page_collection(cards) 
elif page == "🏆 Défis":
    page_defis(cards)


