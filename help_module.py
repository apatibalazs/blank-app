import streamlit as st

def get_help_text(key):
    data = {
        "BREAK": {
            "title": "BREAK STATE",
            "summary": "Paradigmaromboló mód.",
            "use_case": "Beidegződések széttörése, ideológiai destabilizáció.",
            "warning": "Absztrakt túlterhelés, paradox hurok.",
            "combo": "BREAK + DEEP"
        },
        "FOG": {
            "title": "FOG STATE",
            "summary": "Bizonytalansági mező.",
            "use_case": "Koncepció-tervezés, iránykeresés.",
            "warning": "Alacsony konvergencia, túl tág fókusz.",
            "combo": "FOG + BALANCED"
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
      
