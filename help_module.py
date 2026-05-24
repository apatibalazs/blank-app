import streamlit as st

# =============================================================================
# COGNITO HELP MODULE
# Reactor Console Companion System
# =============================================================================

def get_help_text(key):

    data = {

        # =====================================================================
        # STATES
        # =====================================================================

        "FOG": {
            "title": "FOG STATE",
            "summary": "Bizonytalansági mező.",
            "use_case": "Koncepció-tervezés, korai iránykeresés.",
            "warning": "Alacsony konvergencia, diffúz fókusz.",
            "combo": "FOG + BALANCED"
        },

        "SPARK": {
            "title": "SPARK STATE",
            "summary": "Asszociációs gyújtás.",
            "use_case": "Új kapcsolatok, kreatív ugrások.",
            "warning": "Zajos vagy széteső output.",
            "combo": "SPARK + CREATIVE"
        },

        "CUT": {
            "title": "CUT STATE",
            "summary": "Sebészeti analízis.",
            "use_case": "Redundancia eltávolítása, érvek kiélezése.",
            "warning": "Túlzott redukció, száraz output.",
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
            "use_case": "Absztrakciók földelése konkrét következményekre.",
            "warning": "Disszonancia és túlkemény konklúziók.",
            "combo": "COLLISION + SCIENTIFIC"
        },

        "BREAK": {
            "title": "BREAK STATE",
            "summary": "Paradigmaromboló mód.",
            "use_case": "Beidegződések és stabil narratívák széttörése.",
            "warning": "Absztrakt túlterhelés, paradox hurok.",
            "combo": "BREAK + DEEP"
        },

        "ALCHEMY": {
            "title": "ALCHEMY STATE",
            "summary": "Transzmutációs szintézis.",
            "use_case": "Új fogalmi hálózatok és nyelvi struktúrák építése.",
            "warning": "Jelentés-instabilitás.",
            "combo": "ALCHEMY + COLLISION"
        },

        # =====================================================================
        # MODES
        # =====================================================================

        "QUICK": {
            "title": "QUICK MODE",
            "summary": "Gyors lineáris futás.",
            "use_case": "Rapid diagnózis és rövid elemzés.",
            "warning": "Felületi következtetések.",
            "combo": "QUICK + CUT"
        },

        "BALANCED": {
            "title": "BALANCED MODE",
            "summary": "Általános operációs egyensúly.",
            "use_case": "Standard Cognito futások.",
            "warning": "Közepes intenzitás.",
            "combo": "BALANCED + FOG"
        },

        "DEEP": {
            "title": "DEEP MODE",
            "summary": "Rekurzív mélyelemzés.",
            "use_case": "Esszék, stratégiai gondolkodás, komplex konfliktusok.",
            "warning": "Token- és mentális túlterhelés.",
            "combo": "DEEP + BREAK"
        },

        "CREATIVE": {
            "title": "CREATIVE MODE",
            "summary": "Divergens gondolkodás.",
            "use_case": "Fogalomalkotás és kreatív struktúrák.",
            "warning": "Elszakadás a realitástól.",
            "combo": "CREATIVE + SPARK"
        },

        "SCIENTIFIC": {
            "title": "SCIENTIFIC MODE",
            "summary": "Evidence-first logikai keret.",
            "use_case": "Forenzikus és adatvezérelt elemzés.",
            "warning": "Túlzott rigiditás.",
            "combo": "SCIENTIFIC + COLLISION"
        },

        # =====================================================================
        # WEB
        # =====================================================================

        "OFF": {
            "title": "WEB OFF",
            "summary": "Külső adatok tiltva.",
            "use_case": "Zárt konceptuális futások.",
            "warning": "Reality anchor hiány.",
            "combo": "OFF + ALCHEMY"
        },

        "AUTO": {
            "title": "WEB AUTO",
            "summary": "Adaptív webhasználat.",
            "use_case": "Általános operáció.",
            "warning": "Inkonzisztens forráshasználat.",
            "combo": "AUTO + BALANCED"
        },

        "ON": {
            "title": "WEB ON",
            "summary": "Kényszerített külső validáció.",
            "use_case": "Aktuálpolitika, piaci vagy valós idejű rendszerek.",
            "warning": "Információs zaj.",
            "combo": "ON + SCIENTIFIC"
        },

        # =====================================================================
        # SWITCHES
        # =====================================================================

        "ENGINE_MODE": {
            "title": "ENGINE MODE",
            "summary": "A Cognito reaktor aktiválása.",
            "use_case": "Teljes runtime működés.",
            "warning": "Instabil output generálódhat.",
            "combo": "ENGINE_MODE + OPEN_SYSTEM"
        },

        "OPEN_SYSTEM": {
            "title": "OPEN SYSTEM",
            "summary": "A paradoxonok nyitva tartása.",
            "use_case": "Korai lezárás megakadályozása.",
            "warning": "Végtelen destabilizáció.",
            "combo": "OPEN_SYSTEM + BREAK"
        },

        "DECISION_MODE": {
            "title": "DECISION MODE",
            "summary": "Kényszerített konklúzió.",
            "use_case": "Döntési helyzetek.",
            "warning": "Alternatívák eliminációja.",
            "combo": "DECISION_MODE + PRESSURE"
        },

        "VALIDATION_MODE": {
            "title": "VALIDATION MODE",
            "summary": "Önellenőrzés és logikai audit.",
            "use_case": "Konzisztencia-vizsgálat.",
            "warning": "Lassabb futás.",
            "combo": "VALIDATION_MODE + SCIENTIFIC"
        },

        "ANTI_CLOSURE": {
            "title": "ANTI-CLOSURE",
            "summary": "Lezárásellenes mechanizmus.",
            "use_case": "Nyitott feszültségek fenntartása.",
            "warning": "Paradox túlburjánzás.",
            "combo": "ANTI_CLOSURE + BREAK"
        },

        "LOSS_TRACKING": {
            "title": "LOSS TRACKING",
            "summary": "Eliminált utak követése.",
            "use_case": "Döntési veszteségek dokumentálása.",
            "warning": "Magas mentális súly.",
            "combo": "LOSS_TRACKING + DECISION_MODE"
        }

    }

    return data.get(key)


# =============================================================================
# POPUP HELP RENDER
# =============================================================================

def show_help(key):

    data = get_help_text(key)

    if not data:
        return

    with st.popover("ⓘ"):
        st.markdown(f"### {data['title']}")
        st.markdown(f"**Mire való:** {data['summary']}")
        st.markdown(f"**Használd:** {data['use_case']}")
        st.markdown(f"**Kockázat:** :red[{data['warning']}]")
        st.markdown(f"**Ajánlott kombó:** `{data['combo']}`")


# =============================================================================
# SELECTBOX + HELP WRAPPER
# =============================================================================

def help_selectbox(label, options, index=0, key=None):

    col1, col2 = st.columns([4, 1])

    with col1:
        value = st.selectbox(
            label,
            options=options,
            index=index,
            key=key
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        show_help(value)

    return value


# =============================================================================
# TOGGLE + HELP WRAPPER
# =============================================================================

def help_toggle(label, value=False, key=None):

    col1, col2 = st.columns([4, 1])

    with col1:
        val = st.toggle(
            label,
            value=value,
            key=key
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        show_help(label)

    return val
