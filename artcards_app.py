import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- Charger les cartes ---
cards = pd.read_csv("cartes50.csv")  # Ton CSV avec URL Image de Wikipédia

# --- Session state ---
if "collection" not in st.session_state:
    st.session_state.collection = []
if "last_day" not in st.session_state:
    st.session_state.last_day = datetime.today().date()
if "days_connected" not in st.session_state:
    st.session_state.days_connected = 1

# --- Couleurs et styles ---
rarity_colors = {
    "Commun": "lightgray",
    "Peu commun": "#6495ED",
    "Rare": "#800080",
    "Légendaire": "#FFD700"
}

# --- Titre ---
st.markdown("<h1 style='text-align:center; color: darkblue;'>🎨 ArtCards - Collection d'art 🎨</h1>", unsafe_allow_html=True)

# --- Mise à jour jours de connexion ---
today = datetime.today().date()
if st.session_state.last_day != today:
    st.session_state.days_connected += 1
    st.session_state.last_day = today

st.markdown(f"<p style='text-align:center;'>Jours de connexion : <b>{st.session_state.days_connected}</b></p>", unsafe_allow_html=True)

# --- Fonction pour ouvrir un pack ---
def open_pack(pack_cards):
    st.subheader("📦 Ouverture du pack...")
    for _, card in pack_cards.iterrows():
        if card["ID"] not in st.session_state.collection:
            st.session_state.collection.append(card["ID"])
        rarity = card["Rareté"]
        star = "✨" if rarity in ["Rare", "Légendaire"] else ""
        color = rarity_colors.get(rarity, "black")
        st.markdown(f"<p style='color:{color}; font-weight:bold; font-size:18px;'>{star} {card['Nom de l’œuvre']} ({rarity}) - {card['Artiste']}</p>", unsafe_allow_html=True)
        st.image(card['URL Image'], width=200)  # <-- Ici on affiche l'image

# --- Pack mystère ---
if st.session_state.days_connected >= 7 and st.session_state.days_connected % 7 == 0:
    mystery_cards = cards.sample(5)
    st.subheader("🎁 Pack Mystère Débloqué !")
    open_pack(mystery_cards)

# --- Pack du jour ---
theme_list = cards["Période / Thème"].unique()
chosen_theme = st.selectbox("Choisis ton pack du jour :", theme_list)

if st.button("Ouvrir le pack"):
    pack_cards = cards[cards["Période / Thème"] == chosen_theme].sample(5)
    st.subheader(f"📦 Pack {chosen_theme} ouvert !")
    open_pack(pack_cards)

# --- Albums par thème ---
st.subheader("📚 Albums par thème")
for theme in theme_list:
    st.write(f"### {theme}")
    theme_cards = cards[cards["Période / Thème"] == theme]
    owned = theme_cards[theme_cards["ID"].isin(st.session_state.collection)]
    missing = theme_cards[~theme_cards["ID"].isin(st.session_state.collection)]
    
    st.write(f"Cartes possédées : {len(owned)}/{len(theme_cards)}")
    st.progress(len(owned)/len(theme_cards))
    
    cols = st.columns(5)
    for idx, (_, card) in enumerate(owned.iterrows()):
        col = cols[idx % 5]
        star = "✨" if card["Rareté"] in ["Rare", "Légendaire"] else ""
        border = "4px solid gold" if card["Rareté"] == "Légendaire" else "2px solid black"
        col.markdown(f"""
        <div style='border:{border}; padding:5px; text-align:center;'>
            <img src="{card['URL Image']}" width="100"><br>
            {star} {card['Nom de l’œuvre']} ({card['Rareté']})
        </div>
        """, unsafe_allow_html=True)
    
    for idx, (_, card) in enumerate(missing.iterrows()):
        col = cols[idx % 5]
        col.image("https://via.placeholder.com/100?text=??", width=100, caption="Carte manquante")
