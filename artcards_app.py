import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Chargement des cartes depuis un CSV
cards = pd.read_csv("cartes50.csv")

# Initialisation session state
if "collection" not in st.session_state:
    st.session_state.collection = []
if "last_day" not in st.session_state:
    st.session_state.last_day = datetime.today()
if "days_connected" not in st.session_state:
    st.session_state.days_connected = 0

st.title("ArtCards - Collection d'art")

# Simuler connexion quotidienne
today = datetime.today().date()
if st.session_state.last_day.date() != today:
    st.session_state.days_connected += 1
    st.session_state.last_day = datetime.today()

st.write(f"Jours de connexion cumulés : {st.session_state.days_connected}")

# Pack mystère tous les 7 jours
if st.session_state.days_connected % 7 == 0:
    st.subheader("Pack Mystère Débloqué !")
    mystery_cards = cards.sample(5)
    for _, card in mystery_cards.iterrows():
        st.session_state.collection.append(card["ID"])
        st.write(f"{card['Nom de l’œuvre']} ({card['Rareté']}) - {card['Période / Thème']}")

# Choix du pack thématique
theme_list = cards["Période / Thème"].unique()
chosen_theme = st.selectbox("Choisis ton pack du jour :", theme_list)

if st.button("Ouvrir le pack"):
    pack_cards = cards[cards["Période / Thème"]==chosen_theme].sample(5)
    for _, card in pack_cards.iterrows():
        if card["ID"] not in st.session_state.collection:
            st.session_state.collection.append(card["ID"])
        st.write(f"{card['Nom de l’œuvre']} ({card['Rareté']}) - {card['Artiste']}")

# Affichage de l'album
st.subheader("Albums par thème")
for theme in theme_list:
    st.write(f"### {theme}")
    theme_cards = cards[cards["Période / Thème"]==theme]
    owned = theme_cards[theme_cards["ID"].isin(st.session_state.collection)]
    missing = theme_cards[~theme_cards["ID"].isin(st.session_state.collection)]
    st.write(f"Cartes possédées : {len(owned)}/{len(theme_cards)}")
    # Affichage cartes possédées
    for _, card in owned.iterrows():
        st.image(card["URL Image"], width=150, caption=f"{card['Nom de l’œuvre']} ({card['Rareté']})")
    # Affichage silhouettes cartes manquantes
    for _, card in missing.iterrows():
        st.image("https://via.placeholder.com/150?text=??", width=150, caption="Carte manquante")
