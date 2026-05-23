import streamlit as st
import enum
import re
import time
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

# ==============================================================================
# PAGE CONFIG
# ==============================================================================

st.set_page_config(
    page_title="COGNITO FUSION MONOLITH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Egyedi stílus a "monolit" érzéshez
st.markdown("""
    <style>
    .stButton>button { border-radius: 0px; font-weight: bold; border: 1px solid #ff4b4b; }
    .stExpander { border-radius: 0px; border-left: 3px solid #ff4b4b; }
    hr { margin-top: 1rem; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# ENUMS & DATA STRUCTURES
# ==============================================================================

class ExecutionMode(enum.Enum):
    QUICK = "QUICK MODE"
    FULL = "FULL MODE"
    DEEP = "DEEP MODE (INTERFERENCE ACTIVE)"

class SystemState(enum.Enum):
    FOG = "FOG (MAPPING)"
    SPARK = "SPARK (DIVERGENCE)"
    PRESSURE = "PRESSURE (TESTING)"
    CUT = "CUT (REDUCTION)"
    LOCK = "LOCK (COMMITMENT)"

class WritingMode(enum.Enum):
    STANDARD = "STANDARD"
    FORENSIC = "FORENSIC"
    ANALYTIC_NOIR = "ANALYTIC_NOIR"
    COMPRESSED = "COMPRESSED"

@dataclass
class Contradiction:
    sentence_index: int
    text: str
    severity: int
    contradiction_type: str

# ==============================================================================
# ENGINES
# ==============================================================================

class ContradictionRegistry:
    def __init__(self):
        self.positive_markers = ["stabil", "biztonságos", "növekedés", "fejlődés", "siker", "hatékony", "nyereség"]
        self.negative_markers = ["összeomlás", "válság", "veszteség", "instabil", "hiba", "kockázat", "lassú"]
        self.contrast_words = ["de", "azonban", "mégis", "viszont", "ellenben", "noha"]

    def scan(self, text):
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        contradictions = []
        tension_score = 0
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            has_pos = any(w in sentence_lower for w in self.positive_markers)
            has_neg = any(w in sentence_lower for w in self.negative_markers)
            has_contrast = any(w in sentence_lower for w in self.contrast_words)

            if has_pos and has_neg:
                contradictions.append(Contradiction(i + 1, sentence, 80, "POS_NEG_COLLISION"))
                tension_score += 8
            elif has_contrast:
                contradictions.append(Contradiction(i + 1, sentence, 50, "RHETORICAL_TENSION"))
                tension_score += 5

        # Garantáljuk, hogy legalább 1 pont legyen, ha van szöveg (hogy a motor mindig reagáljon)
        if len(text) > 10 and tension_score == 0:
            tension_score = 1 

        return {"contradictions": contradictions, "tension_score": tension_score}

class DecisionEngine:
    def evaluate(self, options, tension_score):
        evaluated = []
        for option in options:
            score = (option["priority"] * 10 + option["entropy_gain"] + option["reversibility"] 
                     - option["risk"] - option["cost"] - option["political_damage"] - tension_score)
            evaluated.append({
                "name": option["name"], "score": round(score, 2), 
                "loss_bearer": option["loss_bearer"], "responsibility": option["responsibility"], "raw": option
            })
        evaluated.sort(key=lambda x: x["score"], reverse=True)
        return evaluated

class CognitoWritingEngine:
    def __init__(self, mode):
        self.mode = mode

    def generate(self, winner, tension_score):
        option = winner["raw"]
        
        if self.mode == WritingMode.FORENSIC:
            text = f"=== FORENSIC REPORT ===\nStratégia: {winner['name']}\nScore: {winner['score']}\nTension: {tension_score}\nVeszteségviselő: {winner['loss_bearer']}"
        elif self.mode == WritingMode.ANALYTIC_NOIR:
            text = f"A rendszer döntött. A nyomás elől az egyetlen kiút a(z) {winner['name']} volt. A veszteséget a(z) {winner['loss_bearer']} viseli. Nincs visszaút."
        elif self.mode == WritingMode.COMPRESSED:
            text = f"[{winner['name']}] | S:{winner['score']} | T:{tension_score} | L:{winner['loss_bearer']}"
        else:
            text = f"STRATÉGIAI JELENTÉS\nKiválasztott: {winner['name']}\nMutató: {winner['score']}\nFelelős: {winner['responsibility']}"
        
        return text

class CognitoRuntime:
    def __init__(self):
        self.nlp = ContradictionRegistry()
        self.decision_engine = DecisionEngine()

    def run(self, text, options, writing_mode):
        nlp_result = self.nlp.scan(text)
        tension_score = nlp_result["tension_score"]
        
        if "összeomlás" in text.lower() or tension_score > 10:
            mode = ExecutionMode.DEEP
        elif tension_score >= 5:
            mode = ExecutionMode.FULL
        else:
            mode = ExecutionMode.QUICK

        decisions = self.decision_engine.evaluate(options, tension_score)
        writer = CognitoWritingEngine(writing_mode)
        final_report = writer.generate(decisions[0], tension_score)

        return {
            "mode": mode,
            "tension_score": tension_score,
            "contradictions": nlp_result["contradictions"],
            "decisions": decisions,
            "report": final_report
        }

# ==============================================================================
# UI - FRONTEND (SESSION STATE MEMÓRIÁVAL)
# ==============================================================================

# 1. Memória inicializálása
if 'run_complete' not in st.session_state:
    st.session_state.run_complete = False
if 'runtime_result' not in st.session_state:
    st.session_state.runtime_result = None

runtime = CognitoRuntime()

st.title("⚡ COGNITO FUSION MONOLITH")
st.caption("Advanced Strategic Cognitive Runtime Dashboard v5.0 | Persistent Memory Active")

left, right = st.columns([1.2, 1])

with left:
    st.subheader("INPUT DATA")
    text_input = st.text_area("Vizsgálandó szöveg", height=150, key="input_text")
    writing_mode = st.selectbox("Kimeneti stílus", [wm for wm in WritingMode], key="w_mode")
    
    st.divider()
    option_count = st.slider("Forgatókönyvek száma", 1, 3, 2)
    
    options = []
    for i in range(option_count):
        with st.expander(f"Opció {i + 1} paraméterei", expanded=(i==0)):
            name = st.text_input(f"Név", value=f"Stratégia {i+1}", key=f"n_{i}")
            c1, c2 = st.columns(2)
            with c1:
                p = st.slider("Prioritás", 1, 10, 5, key=f"p_{i}")
                e = st.slider("Entrópia", 0, 100, 50, key=f"e_{i}")
                rev = st.slider("Reverzibilitás", 0, 100, 50, key=f"rev_{i}")
            with c2:
                r = st.slider("Kockázat", 0, 100, 20, key=f"r_{i}")
                c = st.slider("Költség", 0, 100, 20, key=f"c_{i}")
                pol = st.slider("PR Kár", 0, 100, 10, key=f"pol_{i}")
            
            lb = st.text_input("Veszteségviselő", value="Rendszer", key=f"lb_{i}")
            resp = st.text_input("Felelősség", value="Core", key=f"resp_{i}")
            
            options.append({"name": name, "priority": p, "risk": r, "cost": c, "entropy_gain": e, 
                            "reversibility": rev, "political_damage": pol, "loss_bearer": lb, "responsibility": resp})

    # A GOMB megnyomása aktiválja a számítást és elmenti a memóriába
    if st.button("🚀 INITIATE COGNITO RUNTIME", use_container_width=True):
        if text_input.strip() == "":
            st.error("Kérlek írj be valamilyen vizsgálandó szöveget az indításhoz!")
        else:
            # Látványos betöltés
            progress_bar = st.progress(0)
            status_text = st.empty()
            step = 100 // len(SystemState)
            current_prog = 0
            for state in SystemState:
                current_prog += step
                progress_bar.progress(min(current_prog, 100))
                status_text.info(f"⚙️ PROCESSING: {state.value}...")
                time.sleep(0.3)
            
            progress_bar.empty()
            status_text.empty()

            # Futás és Eredmény Mentése a Session State-be
            st.session_state.runtime_result = runtime.run(text_input, options, writing_mode)
            st.session_state.run_complete = True

with right:
    st.subheader("SYSTEM STATE")
    
    # Csak akkor mutatjuk a jobb oldalt, ha van a memóriában lefutott eredmény
    if st.session_state.run_complete and st.session_state.runtime_result is not None:
        res = st.session_state.runtime_result
        
        c1, c2 = st.columns(2)
        c1.metric("MODE", res['mode'].name)
        c2.metric("TENSION", res["tension_score"])
        
        st.divider()
        st.subheader("CONTRADICTIONS")
        if res["contradictions"]:
            for cnt in res["contradictions"]:
                st.warning(f"**[{cnt.contradiction_type}]**\n{cnt.text}")
        else:
            st.success("Szöveges feszültség nem detektálva.")

        st.divider()
        st.subheader("DECISION OUTCOME")
        for idx, dec in enumerate(res["decisions"]):
            if idx == 0:
                st.success(f"🏆 WINNER: {dec['name']} (Score: {dec['score']})")
            else:
                st.error(f"❌ ELIMINATED: {dec['name']} (Score: {dec['score']})")

        st.divider()
        st.subheader("FINAL REPORT")
        st.code(res["report"], language="text")
        
        # Mivel Session State-ből dolgozunk, a letöltés gomb most már nem fogja "elfelejteni" az adatot!
        st.download_button(
            label="💾 JELENTÉS LETÖLTÉSE (.TXT)",
            data=res["report"],
            file_name=f"cognito_report_{int(time.time())}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("A rendszer várakozik. Töltsd ki a bal oldalt és indítsd el a futtatást.")
