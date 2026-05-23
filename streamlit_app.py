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

# ==============================================================================
# ENUMS
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

# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class Contradiction:
    sentence_index: int
    text: str
    severity: int
    contradiction_type: str

# ==============================================================================
# NLP / CONTRADICTION ENGINE
# ==============================================================================

class ContradictionRegistry:
    def __init__(self):
        self.positive_markers = [
            "stabil", "biztonságos", "növekedés", "fejlődés", 
            "siker", "hatékony", "nyereség", "támogatás", "pozitív"
        ]
        self.negative_markers = [
            "összeomlás", "válság", "veszteség", "instabil", 
            "hiba", "kockázat", "lassú", "hiteltelen", "ellentmondás"
        ]
        self.contrast_words = [
            "de", "azonban", "mégis", "viszont", "ellenben", "noha", "bár"
        ]

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
                contradictions.append(
                    Contradiction(i + 1, sentence, 80, "POS_NEG_COLLISION")
                )
                tension_score += 8
            elif has_contrast:
                contradictions.append(
                    Contradiction(i + 1, sentence, 50, "RHETORICAL_TENSION")
                )
                tension_score += 5

        return {
            "contradictions": contradictions,
            "tension_score": tension_score,
            "sentence_count": len(sentences)
        }

# ==============================================================================
# DECISION ENGINE
# ==============================================================================

class DecisionEngine:
    def evaluate(self, options, tension_score):
        evaluated = []
        for option in options:
            score = (
                option["priority"] * 10
                + option["entropy_gain"]
                + option["reversibility"]
                - option["risk"]
                - option["cost"]
                - option["political_damage"]
                - tension_score
            )
            evaluated.append({
                "name": option["name"],
                "score": round(score, 2),
                "loss_bearer": option["loss_bearer"],
                "responsibility": option["responsibility"],
                "raw": option
            })
        evaluated.sort(key=lambda x: x["score"], reverse=True)
        return evaluated

# ==============================================================================
# WRITING ENGINE
# ==============================================================================

class CognitoWritingEngine:
    def __init__(self, mode):
        self.mode = mode
        self.tilt_keywords = ["A kérdés tehát", "Valójában", "Kulcsfontosságú"]

    def generate(self, winner, tension_score):
        option = winner["raw"]
        
        if self.mode == WritingMode.FORENSIC:
            text = (
                f"=== FORENSIC REPORT ===\n\n"
                f"Kiválasztott stratégia: {winner['name']}\n"
                f"Döntési Hozam (Score): {winner['score']}\n"
                f"Kockázati Faktor: {option['risk']}\n"
                f"Rendszer Költség: {option['cost']}\n"
                f"Entrópia Nyereség: {option['entropy_gain']}\n"
                f"Detektált Strukturális Nyomás: {tension_score}\n\n"
                f"Veszteségviselő: {winner['loss_bearer']}"
            )
        elif self.mode == WritingMode.ANALYTIC_NOIR:
            text = (
                f"A rendszer döntött. Nem azért, mert ez a tökéletes megoldás, "
                f"hanem mert a többi opció gyorsabban omlott volna össze a feszültség alatt. "
                f"Kiválasztott ág: {winner['name']}. "
                f"A járulékos veszteséget viseli: {winner['loss_bearer']}."
            )
        elif self.mode == WritingMode.COMPRESSED:
            text = f"[{winner['name']}] | SCORE:{winner['score']} | TENSION:{tension_score} | LOSS:{winner['loss_bearer']}"
        else:
            text = (
                f"STRATÉGIAI JELENTÉS\n\n"
                f"Kiválasztott opció: {winner['name']}\n"
                f"Sikerességi mutató: {winner['score']}\n"
                f"Felelősségi szint: {winner['responsibility']}\n"
            )

        for keyword in self.tilt_keywords:
            if keyword in text:
                return f"[TILT DETECTED - FORCED SMOOTHING REJECTED] -> {keyword}"
        return text

# ==============================================================================
# MAIN RUNTIME
# ==============================================================================

class CognitoRuntime:
    def __init__(self):
        self.nlp = ContradictionRegistry()
        self.decision_engine = DecisionEngine()

    def auto_route(self, text, tension_score):
        if "összeomlás" in text.lower() or tension_score > 10:
            return ExecutionMode.DEEP
        if tension_score >= 5:
            return ExecutionMode.FULL
        return ExecutionMode.QUICK

    def run(self, text, options, writing_mode):
        nlp_result = self.nlp.scan(text)
        tension_score = nlp_result["tension_score"]
        mode = self.auto_route(text, tension_score)
        decisions = self.decision_engine.evaluate(options, tension_score)
        winner = decisions[0]
        writer = CognitoWritingEngine(writing_mode)
        final_report = writer.generate(winner, tension_score)

        return {
            "mode": mode,
            "tension_score": tension_score,
            "contradictions": nlp_result["contradictions"],
            "decisions": decisions,
            "report": final_report
        }

# ==============================================================================
# UI - FRONTEND
# ==============================================================================

runtime = CognitoRuntime()

st.title("⚡ COGNITO FUSION MONOLITH")
st.caption("Advanced Strategic Cognitive Runtime Dashboard v4.0")

left, right = st.columns([1.2, 1])

# --- LEFT PANEL ---
with left:
    st.subheader("INPUT DATA")
    text_input = st.text_area(
        "Vizsgálandó esemény vagy szöveg",
        height=180,
        placeholder="Másold be ide a vizsgálandó témát, hírt vagy helyzetet..."
    )
    
    writing_mode = st.selectbox("Kimeneti stílus (Writing Mode)", [wm for wm in WritingMode])
    
    st.divider()
    st.subheader("OPTION MATRIX")
    option_count = st.slider("Hány lehetséges forgatókönyvet vizsgáljunk?", 1, 4, 2)
    
    options = []
    for i in range(option_count):
        with st.expander(f"Forgatókönyv / Opció {i + 1} paraméterei", expanded=(i==0)):
            name = st.text_input(f"Opció {i+1} neve", value=f"Stratégia {i+1}")
            c1, c2 = st.columns(2)
            with c1:
                priority = st.slider(f"Prioritás", 1, 10, 5, key=f"p_{i}")
                entropy_gain = st.slider(f"Entrópia Nyereség", 0, 100, 50, key=f"e_{i}")
                reversibility = st.slider(f"Visszafordíthatóság", 0, 100, 50, key=f"rev_{i}")
            with c2:
                risk = st.slider(f"Kockázat", 0, 100, 20, key=f"r_{i}")
                cost = st.slider(f"Költség", 0, 100, 20, key=f"c_{i}")
                political_damage = st.slider(f"Politikai/PR Kár", 0, 100, 10, key=f"pol_{i}")
            
            loss_bearer = st.text_input(f"Veszteségviselő", value="Társadalom / Rendszer", key=f"lb_{i}")
            responsibility = st.text_input(f"Felelősségi szint", value="Core Layer", key=f"resp_{i}")
            
            options.append({
                "name": name, "priority": priority, "risk": risk, "cost": cost,
                "entropy_gain": entropy_gain, "reversibility": reversibility,
                "political_damage": political_damage, "loss_bearer": loss_bearer,
                "responsibility": responsibility
            })

    run_button = st.button("🚀 INITIATE COGNITO RUNTIME", use_container_width=True, type="primary")

# --- RIGHT PANEL ---
with right:
    st.subheader("SYSTEM STATE")
    
    if run_button and text_input:
        
        # Látványos betöltő képernyő (Progress bar)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        step = 100 // len(SystemState)
        current_prog = 0
        
        for state in SystemState:
            current_prog += step
            progress_bar.progress(min(current_prog, 100))
            status_text.info(f"⚙️ PROCESSING: {state.value}...")
            time.sleep(0.4) # Késleltetés a drámai hatásért
            
        status_text.success("✅ RUNTIME COMPLETE")
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        # Eredmények kiszámítása
        result = runtime.run(text_input, options, writing_mode)

        # Fő metrikák
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("EXECUTION MODE", result['mode'].name)
        col_m2.metric("TENSION SCORE", result["tension_score"])
        
        if result["tension_score"] > 15:
            st.error("⚠️ MAGAS STRUKTURÁLIS FESZÜLTSÉG DETEKTÁLVA")

        st.divider()

        # Ellentmondások
        st.subheader("DETECTED CONTRADICTIONS")
        if result["contradictions"]:
            for contradiction in result["contradictions"]:
                st.warning(
                    f"**[{contradiction.contradiction_type}]** - "
                    f"Mondat #{contradiction.sentence_index}\n\n"
                    f"*{contradiction.text}*"
                )
        else:
            st.success("Nem detektált nyelvi rendszerfeszültséget.")

        st.divider()

        # Döntési mátrix
        st.subheader("DECISION MATRIX OUTCOME")
        for idx, decision in enumerate(result["decisions"]):
            if idx == 0:
                st.success(f"🏆 WINNER: **{decision['name']}** (Score: {decision['score']})")
                st.caption(f"Veszteségviselő: {decision['loss_bearer']}")
            else:
                st.error(f"❌ ELIMINATED: **{decision['name']}** (Score: {decision['score']})")

        st.divider()

        # Végső jelentés és Letöltés gomb
        st.subheader("FINAL OUTPUT")
        st.code(result["report"], language="text")
        
        st.download_button(
            label="💾 JELENTÉS LETÖLTÉSE (.TXT)",
            data=result["report"],
            file_name=f"cognito_report_{int(time.time())}.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:
        st.info("A rendszer várakozik az adatokra. Töltsd ki a bal oldalt, majd nyomj a RUN gombra!")

# ==============================================================================
# FOOTER
# ==============================================================================
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "COGNITO FUSION MONOLITH v4.0 ADVANCED | "
    "Experimental Cognitive Runtime Interface"
    "</div>", 
    unsafe_allow_html=True
)
