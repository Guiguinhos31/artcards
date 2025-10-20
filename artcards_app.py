import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- Chargement des cartes depuis CSV ---
cards = pd.read_csv("cartes50.csv")

# --- Initialisation session state ---
if "collection" not in st.session_state:
    st.session_state.collection = []
if "last_day" not in st.session_state:
    st.session_state.last_day = datetime.today().date()
if "days_connected" not in st.session_state:
    st.session_state.days_connected = 1  # Commence à 1 à la première connexion

# --- Titre ---
st.title("ArtCards - Collection d'art")

# --- Mise à jour des jours de connexion ---
today = datetime.today().date()
if st.session_state.last_day != today:
    st.session_state.days_connected += 1
    st.session_state.last_day = today

st.write(f"Jours de connexion cumulés : {st.session_state.days_connected}")

# --- Déblocage du pack mystère tous les 7 jours ---
if st.session_state.days_connected >= 7 and st.session_state.days_connected % 7 == 0:
    st.subheader("Pack Mystère Débloqué !")
    mystery_cards = cards.sample(5)
    for _, card in mystery_cards.iterrows():
        if card["ID"] not in st.session_state.collection:
            st.session_state.collection.append(card["ID"])
        st.write(f"{card['Nom de l’œuvre']} ({card['Rareté']}) - {card['Période / Thème']}")

# --- Choix du pack thématique ---
theme_list = cards["Période / Thème"].unique()
chosen_theme = st.selectbox("Choisis ton pack du jour :", theme_list)

if st.button("Ouvrir le pack"):
    pack_cards = cards[cards["Période / Thème"] == chosen_theme].sample(5)
    st.subheader(f"Pack {chosen_theme} ouvert !")
    for _, card in pack_cards.iterrows():
        if card["ID"] not in st.session_state.collection:
            st.session_state.collection.append(card["ID"])
        st.write(f"{card['Nom de l’œuvre']} ({card['Rareté']}) - {card['Artiste']}")

# --- Affichage des albums ---
st.subheader("Albums par thème")
for theme in theme_list:
    st.write(f"### {theme}")
    theme_cards = cards[cards["Période / Thème"] == theme]
    owned = theme_cards[theme_cards["ID"].isin(st.session_state.collection)]
    missing = theme_cards[~theme_cards["ID"].isin(st.session_state.collection)]
    
    # Barre de progression
    progress = len(owned) / len(theme_cards)
    st.progress(progress)
    
    # Affichage des cartes possédées en grille
    cols = st.columns(5)
    for idx, (_, card) in enumerate(owned.iterrows()):
        col = cols[idx % 5]
        col.image(card["URL Image"], width=100, caption=f"{card['Nom de l’œuvre']} ({card['Rareté']})")
    
    # Cartes manquantes en silhouette
    for idx, (_, card) in enumerate(missing.iterrows()):
        col = cols[idx % 5]
        col.image("https://via.placeholder.com/100?text=??", width=100, caption="Carte manquante")
