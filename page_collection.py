import streamlit as st

def page_collection(cards):
    st.markdown("<h1 style='text-align:center; color:darkblue;'>🎴 Ma collection</h1>", unsafe_allow_html=True)

    # --- CSS pour hover et effets holo ---
    st.markdown("""
    <style>
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 10px;
    }
    .card:hover {
        transform: scale(1.08);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
    }
    .missing-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-radius: 10px;
    }
    .missing-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(150, 150, 150, 0.5);
    }
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

    rarity_colors = {
        "Commun": "lightgray",
        "Peu commun": "#6495ED",
        "Rare": "#800080",
        "Légendaire": "#FFD700"
    }

    theme_list = cards["Période / Thème"].unique()
    
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
                holo_class = "holo" if rarity == "Légendaire" else "card"
                col.markdown(f"""
                <div class='{holo_class}' style='border:{border}; padding:8px; text-align:center; background:white;'>
                    <img src="{card['URL Image']}" width="100" style="display:block; margin:auto; border-radius:8px;"><br>
                    <b style='color:{color}; font-size:12px;'>{star} {card['Nom de l’œuvre']} ({rarity})</b>
                </div>
                """, unsafe_allow_html=True)
            else:
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
