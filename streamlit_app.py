import streamlit as st
import time
import random
from datetime import datetime

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="COGNITO ARCHITECTURE v1.3",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SIDEBAR - GLOBAL SWITCHES (INIT MODULE)
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM INIT")
    st.caption("COGNITO SYSTEM ARCHITECTURE v1.3")
    
    st.divider()
    
    core_active = st.checkbox("COGNITO CORE", value=True, disabled=True)
    workflow_active = st.checkbox("WORKFLOW", value=True, disabled=True)
    writing_active = st.checkbox("WRITING ENGINE", value=True, disabled=True)
    
    st.divider()
    st.markdown("### 🧬 OPTIONAL LAYERS")
    adv_modules = st.checkbox("ADVANCED MODULES")
    research_mode = st.checkbox("RESEARCH MODE")
    dark_mode = st.checkbox("DARK MODE (Destabilization)")

# ==============================================================================
# MAIN UI - HEADER
# ==============================================================================
st.title("⬛ COGNITO POST-MONOLITH")
st.caption("Execution Framework v1.3 | Concept & Design: Apáti Balázs / CSAPATI")

st.markdown("""
> *A rendszer a tényleges struktúrát vizsgálja, nem a deklarált önleírást. 
> Következmény nélküli gondolkodás: INVALID.*
""")

st.divider()

# ==============================================================================
# INPUT SECTION
# ==============================================================================
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("I. TOPIC & INPUT")
    topic_input = st.text_area(
        "Vizsgálandó terület / Input", 
        height=150, 
        placeholder="Adja meg az elemzendő témát, hírt, konfliktust..."
    )
    
    input_type = st.selectbox("Input Típusa", [
        "ARTICLE", "NEWS", "IMAGE", "INTERVIEW", "IDEA", 
        "PERSONAL EXPERIENCE", "THEORY", "CONFLICT", "SYSTEM"
    ])

with col2:
    st.subheader("II. WRITING ENGINE SETTINGS")
    density = st.select_slider("Mondatsűrűség (Density)", options=["LOW", "MEDIUM", "HIGH"], value="MEDIUM")
    gravity = st.select_slider("Gravitáció (Gravity)", options=["LIGHT", "CONTROLLED", "HEAVY"], value="CONTROLLED")
    rhythm = st.selectbox("Ritmusrendszer (Rhythm)", ["FLAT", "PULSED", "FRACTURED", "CASCADING"])
    output_mode = st.selectbox("Kimeneti Mód (Platform Mode)", [
        "STRATEGIC MEMO", "OP-ED", "LONG ESSAY", "PAMPHLET", 
        "COMMENT", "ANALYTIC NOIR", "INTERNAL ANALYSIS"
    ])

st.divider()

run_button = st.button("⚡ EXECUTE COGNITO WORKFLOW", use_container_width=True, type="primary")

# ==============================================================================
# RUNTIME ENGINE (SIMULATED PIPELINE)
# ==============================================================================
if run_button and topic_input:
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    workflow_steps = [
        "STEP 1 → INPUT MAPPING",
        "STEP 2 → REALITY RESOLUTION LOCK",
        "STEP 3 → CONTRADICTION SCAN",
        "STEP 4 → PRESSURE TEST",
        "STEP 5 → CONSEQUENCE MAP",
        "STEP 5B → ACTION VECTOR",
        "STEP 6 → OUTPUT GENERATION",
        "STEP 7 → VALIDATION & GRAVITY CHECK",
        "STEP 8 → SELF-GRAVITY INTERRUPTION"
    ]
    
    # Progress Simulation
    for i, step_name in enumerate(workflow_steps):
        status_text.info(f"🔄 {step_name} ...")
        time.sleep(0.5) # Szimulált kognitív terhelés
        progress_bar.progress((i + 1) / len(workflow_steps))
        
    status_text.success("✅ WORKFLOW EXECUTION COMPLETE")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

    # ==============================================================================
    # OUTPUT DISPLAY (TABS)
    # ==============================================================================
    st.header("🔍 ANALYSIS OUTPUT")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ MAPPING & CONTRADICTION", 
        "💥 PRESSURE & CONSEQUENCE", 
        "⚙️ ENGINE VALIDATION",
        "📝 FINAL TEXT"
    ])
    
    with tab1:
        st.markdown("### STEP 1: INPUT MAPPING")
        st.write(f"**Téma:** {topic_input[:50]}...")
        st.write("**Felszíni narratíva:** A jelenség lineáris, egyértelmű ok-okozati láncként van keretezve.")
        st.write("**Rejtett konfliktus:** Az erőforrások és a szimbolikus tőke újraosztása.")
        
        st.markdown("### STEP 3: CONTRADICTION SCAN")
        st.warning("**IGAZSÁG A:** A rendszer stabilitást sugároz.")
        st.warning("**IGAZSÁG B:** A mikroszintű viselkedések krízist jeleznek.")
        st.error("**RULE ENFORCED:** A rendszer nem oldhatja fel túl gyorsan a paradoxont. (Premature Synthesis elkerülve)")

    with tab2:
        st.markdown("### STEP 4: PRESSURE TEST")
        st.info("**Vakfolt:** A modell feltételezi az emberi racionalitást extrém nyomás alatt is.")
        st.info("**Saját hipotézis támadása:** Ha az ellenfél szemszögéből nézzük, a jelenlegi struktúra nem hiba, hanem funkció.")
        
        st.markdown("### STEP 5: CONSEQUENCE MAP & ACTION VECTOR")
        st.write("1. **Mi törik el?** A formális intézményi bizalom.")
        st.write("2. **Ki fizeti meg az árát?** A periférián lévő szereplők.")
        st.success("**LEGKISEBB VALÓS LÉPÉS (Action Vector):** A redundáns információcsatornák azonnali leválasztása 24 órán belül.")

    with tab3:
        st.markdown("### STEP 7-8: VALIDATION & GRAVITY")
        st.checkbox("Túl korán látható a konklúzió?", value=False, disabled=True)
        st.checkbox("Megmaradt a feszültség?", value=True, disabled=True)
        st.checkbox("Van valódi következmény?", value=True, disabled=True)
        
        if dark_mode:
            st.error("💀 DARK MODE ACTIVE: Ontológiai audit lefuttatva. Destabilizáció modellezve.")
        if adv_modules:
            st.info("🧬 ADVANCED MODULES: Dual-Truth fenntartva. Szimbolikus Stressz Teszt lezárva.")

    with tab4:
        st.markdown("### 🖋️ COGNITO WRITING ENGINE OUTPUT")
        st.caption(f"Physics: {density} Density | {gravity} Gravity | {rhythm} Rhythm | Format: {output_mode}")
        
        # Generált minta szöveg a paraméterek alapján
        final_text = f"""
        A felszín {topic_input[:30].lower()} körül forog, de a valódi tét sosem ez. 
        A struktúra nyomás alatt mindig megmutatja a törésvonalait. 
        
        Két inkompatibilis igazság működik egyszerre. Egyrészt fenn kell tartani a folyamatosság illúzióját. Másrészt a rendszer mélyrétegeiben a következmények már elkezdtek beszivárogni. Ahol nincs veszteség, ott a döntés érvénytelen.
        
        A legkisebb valós lépés nem a narratíva megváltoztatása. A legkisebb valós lépés a struktúra elvágása.
        """
        
        st.code(final_text, language="text")
        
        st.download_button(
            label="💾 KOGNITÍV JELENTÉS LETÖLTÉSE (.TXT)",
            data=final_text,
            file_name=f"post_monolith_report_{int(time.time())}.txt",
            mime="text/plain",
            use_container_width=True
        )

elif run_button and not topic_input:
    st.error("❌ Hiba: Kérlek, adj meg egy vizsgálandó témát az induláshoz!")
