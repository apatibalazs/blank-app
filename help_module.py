import streamlit as st

def get_help_text(key):
    data = {
        "FOG": {
            "title": "FOG STATE",
            "summary": "Bizonytalansági mező.",
            "use_case": "Koncepció-tervezés, iránykeresés.",
            "warning": "Alacsony konvergencia, túl tág fókusz.",
            "combo": "FOG + BALANCED"
        },
        "SPARK": {
            "title": "SPARK STATE",
            "summary": "Asszociációs szikra.",
            "use_case": "Új összefüggések keresése.",
            "warning": "Zajos, divergens kimenet.",
            "combo": "SPARK + CREATIVE"
        },
        "CUT": {
            "title": "CUT STATE",
            "summary": "Sebészeti analízis.",
            "use_case": "Redundancia eltávolítása.",
            "warning": "Túlzottan szikár kimenet.",
            "combo": "CUT + SCIENTIFIC"
        },
        "PRESSURE": {
            "title": "PRESSURE STATE",
            "summary": "Stresszteszt.",
            "use_case": "Premisszák kényszerített evolúciója.",
            "warning": "Magas rendszerfeszültség.",
            "combo": "PRESSURE + DEEP"
        },
        "COLLISION": {
            "title": "COLLISION STATE",
            "summary": "Valósági ütköztetés.",
            "use_case": "Tények és elméletek ütköztetése.",
            "warning": "Kognitív disszonancia veszélye.",
            "combo": "COLLISION + SCIENTIFIC"
        },
        "BREAK": {
            "title": "BREAK STATE",
            "summary": "Paradigmaromboló mód.",
            "use_case": "Beidegződések széttörése.",
            "warning": "Absztrakt túlterhelés.",
            "combo": "BREAK + DEEP"
        },
        "ALCHEMY": {
            "title": "ALCHEMY STATE",
            "summary": "Transzmutációs szintézis.",
            "use_case": "Komplex szintézis.",
            "warning": "Jelentés-instabilitás.",
            "combo": "ALCHEMY + COLLISION"
        }
    }
    return data.get(key)

def show_help(key):
    data = get_help_text(key)
    if not data:
        return
    with st.popover("ⓘ Súgó"):
        st.markdown(f"### {data['title']}")
        st.markdown(f"**Mire való:** {data['summary']}")
        st.markdown(f"**Használd:** {data['use_case']}")
        st.markdown(f"**Kockázat:** :red[{data['warning']}]")
        st.markdown(f"**Ajánlott:** {data['combo']}")
