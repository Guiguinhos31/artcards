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
            "connexion": False,
            "theme_complet": False,
            "collection_legendaire": False,
            "collection_aleatoire": False
        }

    # --- Calcul des défis ---

    # 1️⃣ Pack du jour complet
    if st.session_state.defis_status["pack_du_jour"] == False:
        if st.session_state.get("last_pack_opened", False):
            st.session_state.defis_status["pack_du_jour"] = True
            st.session_state.points += 5

    # 2️⃣ Carte rare
    if st.session_state.defis_status["carte_rare"] == False:
        last_pack = st.session_state.get("last_pack_cards", [])
        if any(card["Rareté"] in ["Rare", "Légendaire"] for card in last_pack):
            st.session_state.defis_status["carte_rare"] = True
            st.session_state.points += 10

    # 3️⃣ Connexion quotidienne
    st.session_state.points += 2 * st.session_state.get("days_connected", 0)

    # 4️⃣ Compléter un thème
    theme_list = cards["Période / Thème"].unique()
    for theme in theme_list:
        theme_cards = cards[cards["Période / Thème"] == theme]
        if all(card["ID"] in st.session_state.collection for _, card in theme_cards.iterrows()):
            if st.session_state.defis_status["theme_complet"] == False:
                st.session_state.defis_status["theme_complet"] = True
                st.session_state.points += 15

    # 5️⃣ Collection légendaire
    if any(cards[cards["ID"] == cid]["Rareté"].values[0] == "Légendaire" for cid in st.session_state.collection):
        if st.session_state.defis_status["collection_legendaire"] == False:
            st.session_state.defis_status["collection_legendaire"] = True
            st.session_state.points += 10

    # 6️⃣ Collection aléatoire
    if all(any(card["ID"] in st.session_state.collection for _, card in cards[cards["Période / Thème"] == theme].iterrows()) for theme in theme_list):
        if st.session_state.defis_status["collection_aleatoire"] == False:
            st.session_state.defis_status["collection_aleatoire"] = True
            st.session_state.points += 20

    # --- Affichage des défis ---
    st.subheader(f"🌟 Points totaux : {st.session_state.points}")
    st.write("---")

    def show_defi(title, points, status):
        icon = "✅" if status else "⏳"
        st.markdown(f"**{icon} {title}** → +{points} points" if not status else f"**{icon} {title}** → +{points} points (complété)")

    show_defi("Pack du jour complet", 5, st.session_state.defis_status["pack_du_jour"])
    show_defi("Carte rare obtenue", 10, st.session_state.defis_status["carte_rare"])
    show_defi("Connexion quotidienne", 2*st.session_state.get("days_connected",0), True)
    show_defi("Compléter un thème", 15, st.session_state.defis_status["theme_complet"])
    show_defi("Collection légendaire", 10, st.session_state.defis_status["collection_legendaire"])
    show_defi("Collection aléatoire", 20, st.session_state.defis_status["collection_aleatoire"])
