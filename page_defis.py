import streamlit as st

def page_defis(cards):
    st.markdown("<h1 style='text-align:center; color:darkblue;'>🏆 Défis</h1>", unsafe_allow_html=True)

    # --- Initialisation session state ---
    if "points" not in st.session_state:
        st.session_state.points = 0
    if "defis_status" not in st.session_state:
        # True = complété, False = non complété
        st.session_state.defis_status = {
            "pack_du_jour": False,
            "carte_rare": False,
            "connexion": 0,  # points déjà attribués pour la connexion
            "theme_complet": False,
            "collection_legendaire": False,
            "collection_aleatoire": False
        }

    # --- Calcul des défis ---

    # 1️⃣ Pack du jour complet
    if not st.session_state.defis_status["pack_du_jour"] and st.session_state.get("last_pack_opened", False):
        st.session_state.defis_status["pack_du_jour"] = True
        st.session_state.points += 5

    # 2️⃣ Carte rare
    if not st.session_state.defis_status["carte_rare"]:
        last_pack = st.session_state.get("last_pack_cards", [])
        if any(card["Rareté"] in ["Rare", "Légendaire"] for card in last_pack):
            st.session_state.defis_status["carte_rare"] = True
            st.session_state.points += 10

    # 3️⃣ Connexion quotidienne
    days_connected = st.session_state.get("days_connected", 0)
    # Calculer uniquement le bonus non encore attribué
    new_connexion_points = 2 * days_connected - st.session_state.defis_status["connexion"]
    if new_connexion_points > 0:
        st.session_state.points += new_connexion_points
        st.session_state.defis_status["connexion"] += new_connexion_points

    # 4️⃣ Compléter un thème
    theme_list = cards["Période / Thème"].unique()
    for theme in theme_list:
        theme_cards = cards[cards["Période / Thème"] == theme]
        if all(card["ID"] in st.session_state.collection for _, card in theme_cards.iterrows()):
            if not st.session_state.defis_status["theme_complet"]:
                st.session_state.defis_status["theme_complet"] = True
                st.session_state.points += 15

    # 5️⃣ Collection légendaire
    if any(cards[cards["ID"] == cid]["Rareté"].values[0] == "Légendaire" for cid in st.session_state.collection):
        if not st.session_state.defis_status["collection_legendaire"]:
            st.session_state.defis_status["collection_legendaire"] = True
            st.session_state.points += 10

    # 6️⃣ Collection aléatoire
    if all(any(card["ID"] in st.session_state.collection for _, card in cards[cards["Période / Thème"] == theme].iterrows()) for theme in theme_list):
        if not st.session_state.defis_status["collection_aleatoire"]:
            st.session_state.defis_status["collection_aleatoire"] = True
            st.session_state.points += 20

    # --- Affichage des défis ---
    st.subheader(f"🌟 Points totaux : {st.session_state.points}")
    st.write("---")

    def show_defi(title, points, status):
        icon = "✅" if status else "⏳"
        display_text = f"**{icon} {title}** → +{points} points"
        if status and "connexion" not in title.lower():
            display_text += " (complété)"
        st.markdown(display_text)

    show_defi("Pack du jour complet", 5, st.session_state.defis_status["pack_du_jour"])
    show_defi("Carte rare obtenue", 10, st.session_state.defis_status["carte_rare"])
    show_defi("Connexion quotidienne", 2*st.session_state.get("days_connected",0), True)
    show_defi("Compléter un thème", 15, st.session_state.defis_status["theme_complet"])
    show_defi("Collection légendaire", 10, st.session_state.defis_status["collection_legendaire"])
    show_defi("Collection aléatoire", 20, st.session_state.defis_status["collection_aleatoire"])
