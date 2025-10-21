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

    # Style CSS global avec effet holographique ✨
    st.markdown("""
    <style>
    /* Effet général des cartes */
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 10px;
    }
    .card:hover {
        transform: scale(1.08);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
    }

    /* Effet des cartes manquantes */
    .missing-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-radius: 10px;
    }
    .missing-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(150, 150, 150, 0.5);
    }

    /* 💫 Animation holographique pour les cartes Légendaires */
    @keyframes holoGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .holo {
        background: linear-gradient(135deg,
            #ff0080, #ff8c00, #40e0d0, #8000ff, #ff0080);
        background-size: 400% 400%;
        animation: holoGradient 4s ease infinite;
        color: white !important;
        text-shadow: 0 0 3px black;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for theme in theme_list:
        st.write(f"### {theme}")
        theme_cards = cards[cards["Période / Thème"] == theme]
        owned = theme_cards[theme_cards["ID"].isin(st.session_state.collection)]
        missing = theme_cards[~theme_cards["ID"].isin(st.session_state.collection)]
        
        st.write(f"Cartes possédées : {len(owned)}/{len(theme_cards)}")
        st.progress(len(owned)/len(theme_cards))
        
        cols = st.columns(5)

        def display_card(col, card=None, owned=False):
            if owned:
                rarity = card["Rareté"]
                star = "✨" if rarity in ["Rare", "Légendaire"] else ""
                border = "4px solid gold" if rarity == "Légendaire" else "2px solid black"
                color = rarity_colors.get(rarity, "black")

                # Si carte légendaire → ajoute classe holo ✨
                holo_class = "holo" if rarity == "Légendaire" else "card"

                col.markdown(f"""
                <div class='{holo_class}' style='border:{border}; padding:8px; text-align:center; background:white;'>
                    <img src="{card['URL Image']}" width="100"
                        style="display:block; margin:auto; border-radius:8px;"><br>
                    <b style='color:{color}; font-size:12px;'>{star} {card['Nom de l’œuvre']} ({rarity})</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Carte manquante
                col.markdown(f"""
                <div class='missing-card' style='border:2px dashed gray; padding:20px; text-align:center;
                            width:100px; height:140px; display:flex; flex-direction:column;
                            justify-content:center; align-items:center; border-radius:8px; background-color:#f0f0f0;'>
                    <span style='font-size:22px; color:gray;'>??</span>
                    <span style='font-size:11px; color:gray;'>Carte manquante</span>
                </div>
                """, unsafe_allow_html=True)

        # Affichage des cartes possédées
        for idx, (_, card) in enumerate(owned.iterrows()):
            col = cols[idx % 5]
            display_card(col, card=card, owned=True)
        
        # Affichage des cartes manquantes
        for idx, (_, card) in enumerate(missing.iterrows()):
            col = cols[idx % 5]
            display_card(col, owned=False)

# ------------------- PAGE 3 : Défis -------------------
elif page == "🏆 Défis":
    st.subheader("Défis artistiques")
    st.write("""
    Ici, tu pourras ajouter :
    - Quizz sur l'histoire de l'art 🎨  
    - Défis créatifs 💡  
    - Mini-jeux autour des cartes 📦  
    """)



