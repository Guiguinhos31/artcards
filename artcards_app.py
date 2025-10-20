import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import requests

# --- Charger les cartes ---
try:
    cards = pd.read_csv("cartes50.csv")  # Assure-toi que 'URL Image' contient les liens corrects
except FileNotFoundError:
    st.error("⚠️ Fichier cartes50.csv introuvable.")
    st.stop()

# --- Initialiser session state ---
if "collection" not in st.session_state:
    st.session_state.collection = []
if "last_day" not in st.session_state:
    st.session_state.last_day = datetime.today().date()
if "days_connected" not in st.session_state:
    st.session_state.days_connected = 1

# --- Couleurs selon rareté ---
rarity_colors = {
    "Commun": "lightgray",
    "Peu commun": "#6495ED",
    "Rare": "#800080",
    "Légendaire": "#FFD700"
}

# --- Titre général ---
st.markdown("<h1 style='text-align:center; color: darkblue;'>🎨 ArtCards - Collection d'art 🎨</h1>", unsafe_allow_html=True)

# --- Mise à jour jours de connexion ---
today = datetime.today().date()
if st.session_state.last_day != today:
    st.session_state.days_connected += 1
    st.session_state.last_day = today

# --- Fonction pour ouvrir un pack ---
def open_pack(pack_cards):
    placeholder = st.empty()
    for _, card in pack_cards.iterrows():
        if card["ID"] not in st.session_state.collection:
            st.session_state.collection.append(card["ID"])
        rarity = card["Rareté"]
        star = "✨" if rarity in ["Rare", "Légendaire"] else ""
        color = rarity_colors.get(rarity, "black")
        placeholder.markdown(f"""
        <div style='border:2px solid {color}; padding:10px; text-align:center; margin-bottom:10px;'>
            <img src="{card['URL Image']}" width="200"><br>
            <b style='color:{color}; font-size:18px;'>{star} {card['Nom de l’œuvre']} ({rarity}) - {card['Artiste']}</b>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)

# --- Sidebar pour navigation ---
page = st.sidebar.selectbox("Navigation", ["🎁 Ouverture de pack", "📚 Ma collection", "🏆 Défis"])

# ------------------- PAGE 1 : Ouverture de pack -------------------
if page == "🎁 Ouverture de pack":
    st.subheader(f"Jours de connexion : {st.session_state.days_connected}")
    
    # Pack mystère toutes les 7 connexions
    if st.session_state.days_connected >= 7 and st.session_state.days_connected % 7 == 0:
        mystery_cards = cards.sample(5)
        st.subheader("🎁 Pack Mystère Débloqué !")
        open_pack(mystery_cards)

    # Pack du jour par thème
    theme_list = cards["Période / Thème"].unique()
    chosen_theme = st.selectbox("Choisis ton pack du jour :", theme_list)
    
    if st.button("Ouvrir le pack"):
        pack_cards = cards[cards["Période / Thème"] == chosen_theme].sample(5)
        st.subheader(f"📦 Pack {chosen_theme} ouvert !")
        open_pack(pack_cards)

# ------------------- PAGE 2 : Collection -------------------
elif page == "📚 Ma collection":
    st.subheader("Ma collection d'art")
    theme_list = cards["Période / Thème"].unique()
    
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

# ------------------- PAGE 3 : Défis -------------------
elif page == "🏆 Défis":
    st.subheader("Défis artistiques")
    st.write("""
    Ici, tu pourras ajouter :
    - Quizz sur l'histoire de l'art 🎨  
    - Défis créatifs 💡  
    - Mini-jeux autour des cartes 📦  
    """)
