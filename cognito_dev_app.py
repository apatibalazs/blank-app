# cognito_dev_app.py
import streamlit as st
import sys
import os

# Core modulok importálása
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.kernel import FernPipeline

st.set_page_config(
    page_title="Cognito Dev • Fern Pipeline",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Cognito Engine — Fejlesztői Verzió")
st.markdown("**Fern Pipeline tesztelés** | Core 1-5 réteg")

# Session state inicializálás
if "dev_pipeline" not in st.session_state:
    st.session_state.dev_pipeline = FernPipeline()
    st.session_state.history = []

pipeline = st.session_state.dev_pipeline

# Oldalsó panel
with st.sidebar:
    st.header("Kísérleti vezérlők")
    
    dna_option = st.selectbox(
        "DNA Stílus",
        ["default", "shaw", "noir", "mystic", "brutal", "paradox"]
    )
    
    if st.button("DNA Stílus Alkalmazása"):
        pipeline.set_dna_style({dna_option: 1.0})
        st.success(f"Stílus: {dna_option}")

    st.divider()
    if st.button("🔄 Teljes Reset"):
        st.session_state.dev_pipeline = FernPipeline()
        st.session_state.history = []
        st.rerun()

# Fő tartalom
input_text = st.text_area(
    "Add meg a bemenetet / gondolatot",
    height=150,
    value="Mi a szabadság és a kényszer valódi kapcsolata?",
    help="Írj hosszabb, elgondolkodtató szöveget is."
)

if st.button("🚀 Futtasd a Fern Pipeline-t", type="primary", use_container_width=True):
    with st.spinner("Kognitív ciklus fut... (Grounding → Attention → Tension)"):
        result = pipeline.run_cycle(input_text)
        
        st.session_state.history.append({
            "input": input_text[:100] + "..." if len(input_text) > 100 else input_text,
            "result": result
        })
        
        st.success("Ciklus lefutott!")

        # Eredmények
        col1, col2 = st.columns(2)
        with col1:
            st.metric("∇τ Feszültség", f"{result.get('tension_gradient', 0):.3f}")
            st.metric("Entrópia", f"{result.get('entropy_level', 0):.3f}")
        with col2:
            st.metric("Ciklus", result.get("cycle", 0))
            st.metric("Fókuszpontok", len(result.get("focus_concepts", [])))

        st.subheader("Fókuszpontok")
        st.write(result.get("focus_concepts", []))

        st.subheader("Feszültség injekciók")
        injections = result.get("injections", [])
        if injections:
            for inj in injections:
                st.info(f"**{inj.get('type')}**: {inj.get('source')} ↔ {inj.get('opposite', '???')}")
        else:
            st.caption("Nincs jelentős injekció ezen a cikluson.")

# Előzmények
if st.session_state.history:
    st.divider()
    st.subheader("Ciklus előzmények")
    for i, entry in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"Ciklus {entry['result'].get('cycle')} — {entry['input'][:60]}..."):
            st.json(entry['result'], expanded=False)

st.caption("Cognito Dev App • Csak tesztelésre • Ne írd felül a fő appot!")
