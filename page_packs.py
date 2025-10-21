import streamlit as st
import time
from datetime import datetime

def page_packs(cards):
    st.markdown("<h1 style='text-align:center; color:darkblue;'>📦 Ouvre ton pack d'art !</h1>", unsafe_allow_html=True)

    # --- Couleurs selon rareté ---
    rarity_colors = {
        "Commun": "lightgray",
        "Peu commun": "#6495ED",
        "Rare": "#800080",
        "Légendaire": "#FFD700"
    }

    # --- Mise à jour du compteur de jours ---
    today = datetime.today().date()
    if st.session_state.last_day != today:
        st.session_state.days_connected += 1
        st.session_state.last_day = today

    st.markdown(f"<p style='text-align:center;'>Jours de connexion : <b>{st.session_state.days_connected}</b></p>", unsafe_allow_html=True)

    # --- Fonction d'ouverture d'un pack ---
    def open_pack(pack_cards):
        placeholder = st.empty()
        for _, card in pack_cards.iterrows():
            if card["ID"] not in st.session_state.collection:
                st.session_state.collection.append(card["ID"])
            color = rarity_colors.get(card["Rareté"], "black")
            star = "✨" if card["Rareté"] in ["Rare", "Légendaire"] else ""
            placeholder.markdown(f"""
            <div style='border:2px solid {color}; padding:10px; text-align:center; margin:10px auto; border-radius:12px; width:80%; max-width:300px;'>
                <img src="{card['URL Image']}" width="200"><br>
                <b style='color:{color}; font-size:18px;'>{star} {card['Nom de l’œuvre']} ({card['Rareté']}) - {card['Artiste']}</b>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.6)

    # --- Choix du pack ---
    theme_list = cards["Période / Thème"].unique()
    chosen_theme = st.selectbox("🎨 Choisis ton pack du jour :", theme_list)

    # --- Bouton pour ouvrir le pack du jour ---
    if st.button("Ouvrir le pack", use_container_width=True):
        theme_cards = cards[cards["Période / Thème"] == chosen_theme]
        n_samples = min(5, len(theme_cards))  # Evite l'erreur si moins de 5 cartes
        pack_cards = theme_cards.sample(n_samples)
        st.subheader(f"📦 Pack {chosen_theme} ouvert !")
        open_pack(pack_cards)

    # --- Pack mystère toutes les 7 connexions ---
    if st.session_state.days_connected % 7 == 0:
        st.success("🎁 Pack mystère débloqué !")
        n_samples_mystery = min(5, len(cards))
        mystery_cards = cards.sample(n_samples_mystery)
        open_pack(mystery_cards)
