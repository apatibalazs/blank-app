import streamlit as st

# =============================================================================
# COGNITO HELP MODULE
# MOBILE SAFE VERSION
# =============================================================================

def get_help_text(key):

    data = {

        # =====================================================================
        # STATES
        # =====================================================================

        "FOG": {
            "title": "FOG STATE",
            "summary": "Bizonytalansági mező.",
            "use_case": "Koncepció-tervezés, iránykeresés.",
            "warning": "Alacsony konvergencia.",
            "combo": "FOG + BALANCED"
        },

        "SPARK": {
            "title": "SPARK STATE",
            "summary": "Asszociációs gyújtás.",
            "use_case": "Új kapcsolatok és kreatív ugrások.",
            "warning": "Zajos output.",
            "combo": "SPARK + CREATIVE"
        },

        "CUT": {
            "title": "CUT STATE",
            "summary": "Sebészeti analízis.",
            "use_case": "Redundancia törlése.",
            "warning": "Túlzott redukció.",
            "combo": "CUT + SCIENTIFIC"
        },

        "PRESSURE": {
            "title": "PRESSURE STATE",
            "summary": "Kognitív stresszteszt.",
            "use_case": "Premisszák nyomás alá helyezése.",
            "warning": "Magas rendszerfeszültség.",
            "combo": "PRESSURE + DEEP"
        },

        "COLLISION": {
            "title": "COLLISION STATE",
            "summary": "Valósági ütköztetés.",
            "use_case": "Absztrakciók földelése.",
            "warning": "Disszonancia veszélye.",
            "combo": "COLLISION + SCIENTIFIC"
        },

        "BREAK": {
            "title": "BREAK STATE",
            "summary": "Paradigmaromboló mód.",
            "use_case": "Stabil narratívák széttörése.",
            "warning": "Paradox hurok.",
            "combo": "BREAK + DEEP"
        },

        "ALCHEMY": {
            "title": "ALCHEMY STATE",
            "summary": "Transzmutációs szintézis.",
            "use_case": "Új fogalmi struktúrák.",
            "warning": "Jelentés-instabilitás.",
            "combo": "ALCHEMY + COLLISION"
        },

        # =====================================================================
        # MODES
        # =====================================================================

        "QUICK": {
            "title": "QUICK MODE",
            "summary": "Gyors lineáris futás.",
            "use_case": "Rapid diagnózis.",
            "warning": "Felületi elemzés.",
            "combo": "QUICK + CUT"
        },

        "BALANCED": {
            "title": "BALANCED MODE",
            "summary": "Standard operáció.",
            "use_case": "Általános futások.",
            "warning": "Közepes intenzitás.",
            "combo": "BALANCED + FOG"
        },

        "DEEP": {
            "title": "DEEP MODE",
            "summary": "Rekurzív mélyelemzés.",
            "use_case": "Komplex konfliktusok.",
            "warning": "Mentális túlterhelés.",
            "combo": "DEEP + BREAK"
        },

        "CREATIVE": {
            "title": "CREATIVE MODE",
            "summary": "Divergens gondolkodás.",
            "use_case": "Fogalomalkotás.",
            "warning": "Elszakadás a realitástól.",
            "combo": "CREATIVE + SPARK"
        },

        "SCIENTIFIC": {
            "title": "SCIENTIFIC MODE",
            "summary": "Evidence-first mód.",
            "use_case": "Forenzikus elemzés.",
            "warning": "Rigiditás.",
            "combo": "SCIENTIFIC + COLLISION"
        }

    }

    return data.get(key)


# =============================================================================
# HELP DISPLAY
# =============================================================================

def show_help(key):

    data = get_help_text(key)

    if not data:
        return

    with st.expander("ⓘ Súgó", expanded=False):

        st.markdown(f"### {data['title']}")

        st.markdown(
            f"**Mire való:** {data['summary']}"
        )

        st.markdown(
            f"**Használd:** {data['use_case']}"
        )

        st.markdown(
            f"**Kockázat:** :red[{data['warning']}]"
        )

        st.markdown(
            f"**Ajánlott kombináció:** `{data['combo']}`"
        )


# =============================================================================
# SELECTBOX + HELP
# =============================================================================

def help_selectbox(label, options, index=0, key=None):

    value = st.selectbox(
        label,
        options=options,
        index=index,
        key=key
    )

    show_help(value)

    return value


# =============================================================================
# TOGGLE + HELP
# =============================================================================

def help_toggle(label, value=False, key=None):

    val = st.toggle(
        label,
        value=value,
        key=key
    )

    show_help(label)

    return val
