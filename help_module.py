import streamlit as st

def get_help_text(key):
    data = {
        "FOG": {"title": "FOG STATE", "summary": "Bizonytalansági mező.", "use_case": "Koncepció-tervezés.", "warning": "Alacsony konvergencia.", "combo": "FOG + BALANCED"},
        "SPARK": {"title": "SPARK STATE", "summary": "Asszociációs szikra.", "use_case": "Új összefüggések.", "warning": "Zajos kimenet.", "combo": "SPARK + CREATIVE"},
        "CUT": {"title": "CUT STATE", "summary": "Sebészeti analízis.", "use_case": "Redundancia törlése.", "warning": "Túlzottan szikár.", "combo": "CUT + SCIENTIFIC"},
        "PRESSURE": {"title": "PRESSURE STATE", "summary": "Stresszteszt.", "use_case": "Premisszák evolúciója.", "warning": "Magas rendszerfeszültség.", "combo": "PRESSURE + DEEP"},
        "COLLISION": {"title": "COLLISION STATE", "summary": "Valósági ütköztetés.", "use_case": "Tények ütköztetése.", "warning": "Disszonancia veszélye.", "combo": "COLLISION + SCIENTIFIC"},
        "BREAK": {"title": "BREAK STATE", "summary": "Paradigmaromboló.", "use_case": "Beidegződések törése.", "warning": "Absztrakt túlterhelés.", "combo": "BREAK + DEEP"},
        "ALCHEMY": {"title": "ALCHEMY STATE", "summary": "Transzmutáció.", "use_case": "Komplex szintézis.", "warning": "Jelentés-instabilitás.", "combo": "ALCHEMY + COLLISION"}
    }
    return data.get(key)

def show_help(key):
    data = get_help_text(key)
    if data:
        # Ez a blokk garantáltan megjelenik az oldalsávban
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### ⓘ {data['title']}")
        st.sidebar.markdown(f"**Mire való:** {data['summary']}")
        st.sidebar.markdown(f"**Használd:** {data['use_case']}")
        st.sidebar.markdown(f"**Kockázat:** :red[{data['warning']}]")
        st.sidebar.markdown(f"**Ajánlott:** {data['combo']}")
        
