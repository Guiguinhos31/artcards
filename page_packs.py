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
    today_date = datetime.today().date()
    if st.session_state.last_day != today_date:
        st.session_state.days_connected += 1
        st.session_state.last_day = today_date

    st.markdown(f"<p style='text-align:center;'>Jours de connexion : <b>{st.session_state.days_connected}</b></p>", unsafe_allow_html=True)

    # --- Initialiser session_state pour le suivi pack ---
    if "last_pack_date" not in st.session_state:
        st.session_state.last_pack_date = None

    # --- Fonction d'ouverture d'un pack ---
    def open_pack(pack_cards):
        placeholder = st.empty()

        # 1️⃣ Pack fermé
        placeholder.image("pack_ferme.png", width=400)
        time.sleep(1.5)
        placeholder.empty()
        time.sleep(0.3)

        # 2️⃣ Cartes qui apparaissent une par une
        for _, card in pack_cards.iterrows():
            if card["ID"] not in st.session_state.collection:
                st.session_state.collection.append(card["ID"])

            color = rarity_colors.get(card["Rareté"], "black")
            star = "✨" if card["Rareté"] in ["Rare", "Légendaire"] else ""

            # Affichage carte + texte
            placeholder.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; text-align:center; margin:30px auto;">
                <img src="{card['URL Image']}" width="350" style="border:4px solid {color}; border-radius:12px;">
                <p style="color:{color}; font-size:18px; margin-top:10px;">
                    {star} {card['Nom de l’œuvre']} ({card['Rareté']}) - {card['Artiste']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(1.0)  # visible 1 seconde
            placeholder.empty()  # disparition avant la suivante

        # 3️⃣ Mise à jour pour les défis
        st.session_state.last_pack_opened = True
        st.session_state.last_pack_cards = pack_cards.to_dict('records')

    # --- Choix du pack ---
    theme_list = cards["Période / Thème"].unique()
    theme_list_with_random = ["Aléatoire"] + list(theme_list)
    chosen_theme = st.selectbox("🎨 Choisis ton pack du jour :", theme_list_with_random)

    pack_cards = None  # initialisation pour éviter UnboundLocalError

    # --- Bouton pour ouvrir le pack ---
    if st.button("Ouvrir le pack", use_container_width=True):
        if st.session_state.get("last_pack_date", None) == today_date:
            st.markdown(f"""
            <div style="
                border: 2px solid #FF4500; 
                border-radius: 12px; 
                background-color: #FFF5F0; 
                padding: 15px; 
                text-align:center;
                max-width:400px; 
                margin:auto;">
                <h3 style="color:#FF4500;">⛔ Oups !</h3>
                <p>Tu as déjà ouvert ton pack aujourd'hui.<br>
                Reviens demain pour découvrir de nouvelles œuvres !</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            if chosen_theme == "Aléatoire":
                n_samples = min(5, len(cards))
                pack_cards = cards.sample(n_samples)
            else:
                theme_cards = cards[cards["Période / Thème"] == chosen_theme]
                n_samples = min(5, len(theme_cards))
                pack_cards = theme_cards.sample(n_samples)

            if pack_cards is not None:
                st.subheader(f"📦 Pack {chosen_theme} ouvert !")
                open_pack(pack_cards)
                st.session_state.last_pack_date = today_date

    # --- Pack mystère toutes les 7 connexions ---
    if st.session_state.days_connected % 7 == 0:
        st.success("🎁 Pack mystère débloqué !")
        n_samples_mystery = min(5, len(cards))
        mystery_cards = cards.sample(n_samples_mystery)
        open_pack(mystery_cards)
