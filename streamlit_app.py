import streamlit as st
import enum
import re
import time
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict

# ==============================================================================
# PAGE CONFIG
# ==============================================================================

st.set_page_config(
    page_title="COGNITO FUSION MONOLITH",
    layout="wide"
)

# ==============================================================================
# ENUMS
# ==============================================================================

class ExecutionMode(enum.Enum):
    QUICK = "QUICK MODE"
    FULL = "FULL MODE"
    DEEP = "DEEP MODE"


class SystemState(enum.Enum):
    FOG = "FOG"
    SPARK = "SPARK"
    PRESSURE = "PRESSURE"
    CUT = "CUT"
    LOCK = "LOCK"


class Density(enum.Enum):
    LOW = "LOW"
    HIGH = "HIGH"


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
            "stabil",
            "biztonságos",
            "növekedés",
            "fejlődés",
            "siker",
            "hatékony",
            "nyereség"
        ]

        self.negative_markers = [
            "összeomlás",
            "válság",
            "veszteség",
            "instabil",
            "hiba",
            "kockázat",
            "lassú"
        ]

        self.contrast_words = [
            "de",
            "azonban",
            "mégis",
            "viszont",
            "ellenben",
            "noha"
        ]

    # --------------------------------------------------------------------------

    def scan(self, text):

        sentences = re.split(
            r'(?<=[.!?]) +',
            text.strip()
        )

        contradictions = []

        tension_score = 0

        for i, sentence in enumerate(sentences):

            sentence_lower = sentence.lower()

            has_pos = any(
                w in sentence_lower
                for w in self.positive_markers
            )

            has_neg = any(
                w in sentence_lower
                for w in self.negative_markers
            )

            has_contrast = any(
                w in sentence_lower
                for w in self.contrast_words
            )

            if has_pos and has_neg:

                contradictions.append(
                    Contradiction(
                        sentence_index=i + 1,
                        text=sentence,
                        severity=80,
                        contradiction_type="POS_NEG_COLLISION"
                    )
                )

                tension_score += 8

            elif has_contrast:

                contradictions.append(
                    Contradiction(
                        sentence_index=i + 1,
                        text=sentence,
                        severity=50,
                        contradiction_type="RHETORICAL_TENSION"
                    )
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

        evaluated.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return evaluated

# ==============================================================================
# WRITING ENGINE
# ==============================================================================

class CognitoWritingEngine:

    def __init__(self, mode):

        self.mode = mode

        self.tilt_keywords = [
            "A kérdés tehát",
            "Valójában",
            "Kulcsfontosságú",
            "Fontos látni"
        ]

    # --------------------------------------------------------------------------

    def generate(self, winner, tension_score):

        option = winner["raw"]

        if self.mode == WritingMode.FORENSIC:

            text = (
                f"FORENSIC REPORT\n\n"
                f"Kiválasztott stratégia: {winner['name']}\n"
                f"Pontszám: {winner['score']}\n"
                f"Kockázat: {option['risk']}\n"
                f"Költség: {option['cost']}\n"
                f"Entrópia nyereség: {option['entropy_gain']}\n"
                f"Konfliktus nyomás: {tension_score}\n"
            )

        elif self.mode == WritingMode.ANALYTIC_NOIR:

            text = (
                f"A rendszer választott. "
                f"Nem azért, mert ez jó megoldás. "
                f"Hanem mert a többi gyorsabban omlott volna össze. "
                f"Kiválasztott ág: {winner['name']}. "
                f"A veszteséget viseli: "
                f"{winner['loss_bearer']}."
            )

        elif self.mode == WritingMode.COMPRESSED:

            text = (
                f"{winner['name']} | "
                f"SCORE={winner['score']} | "
                f"TENSION={tension_score}"
            )

        else:

            text = (
                f"STRATÉGIAI JELENTÉS\n\n"
                f"Kiválasztott opció: {winner['name']}\n"
                f"Pontszám: {winner['score']}\n"
                f"Felelősségi szint: "
                f"{winner['responsibility']}\n"
            )

        for keyword in self.tilt_keywords:

            if keyword in text:
                return f"[TILT DETECTED] -> {keyword}"

        return text

# ==============================================================================
# MEMORY LAYER
# ==============================================================================

class PersistenceLayer:

    def __init__(self):

        self.memory_path = Path("cognito_memory")

        self.memory_path.mkdir(exist_ok=True)

    # --------------------------------------------------------------------------

    def save_run(self, payload):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            self.memory_path
            / f"run_{timestamp}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=2
            )

# ==============================================================================
# MAIN RUNTIME
# ==============================================================================

class CognitoRuntime:

    def __init__(self):

        self.nlp = ContradictionRegistry()

        self.decision_engine = DecisionEngine()

        self.persistence = PersistenceLayer()

    # --------------------------------------------------------------------------

    def auto_route(self, text, tension_score):

        if (
            "összeomlás" in text.lower()
            or tension_score > 10
        ):
            return ExecutionMode.DEEP

        if tension_score >= 5:
            return ExecutionMode.FULL

        return ExecutionMode.QUICK

    # --------------------------------------------------------------------------

    def run(
        self,
        text,
        options,
        writing_mode
    ):

        nlp_result = self.nlp.scan(text)

        tension_score = nlp_result["tension_score"]

        mode = self.auto_route(
            text,
            tension_score
        )

        decisions = self.decision_engine.evaluate(
            options,
            tension_score
        )

        winner = decisions[0]

        writer = CognitoWritingEngine(
            writing_mode
        )

        final_report = writer.generate(
            winner,
            tension_score
        )

        payload = {
            "timestamp": datetime.now().isoformat(),
            "input": text,
            "mode": mode.value,
            "tension_score": tension_score,
            "winner": winner,
            "report": final_report
        }

        self.persistence.save_run(payload)

        return {
            "mode": mode,
            "tension_score": tension_score,
            "contradictions": nlp_result["contradictions"],
            "decisions": decisions,
            "report": final_report
        }

# ==============================================================================
# UI
# ==============================================================================

runtime = CognitoRuntime()

st.title("COGNITO FUSION MONOLITH")
st.caption("Strategic Cognitive Runtime Dashboard")

left, right = st.columns([1.2, 1])

# ==============================================================================
# LEFT PANEL
# ==============================================================================

with left:

    st.subheader("INPUT")

    text_input = st.text_area(
        "Vizsgálandó szöveg",
        height=220,
        placeholder="Írd be a vizsgálandó témát..."
    )

    writing_mode = st.selectbox(
        "Writing Mode",
        [wm for wm in WritingMode]
    )

    st.divider()

    st.subheader("OPTION MATRIX")

    option_count = st.slider(
        "Opciók száma",
        1,
        5,
        2
    )

    options = []

    for i in range(option_count):

        st.markdown(f"### Opció {i + 1}")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                f"Név {i}",
                value=f"Opció {i+1}"
            )

            priority = st.slider(
                f"Priority {i}",
                1,
                10,
                5
            )

            entropy_gain = st.slider(
                f"Entropy Gain {i}",
                0,
                100,
                50
            )

            reversibility = st.slider(
                f"Reversibility {i}",
                0,
                100,
                50
            )

        with col2:

            risk = st.slider(
                f"Risk {i}",
                0,
                100,
                20
            )

            cost = st.slider(
                f"Cost {i}",
                0,
                100,
                20
            )

            political_damage = st.slider(
                f"Political Damage {i}",
                0,
                100,
                10
            )

        loss_bearer = st.text_input(
            f"Loss Bearer {i}",
            value="System"
        )

        responsibility = st.text_input(
            f"Responsibility {i}",
            value="Core Layer"
        )

        options.append({
            "name": name,
            "priority": priority,
            "risk": risk,
            "cost": cost,
            "entropy_gain": entropy_gain,
            "reversibility": reversibility,
            "political_damage": political_damage,
            "loss_bearer": loss_bearer,
            "responsibility": responsibility
        })

    run_button = st.button(
        "RUN COGNITO SYSTEM",
        use_container_width=True
    )

# ==============================================================================
# RIGHT PANEL
# ==============================================================================

with right:

    st.subheader("SYSTEM STATE")

    if run_button and text_input:

        state_placeholder = st.empty()

        for state in SystemState:

            state_placeholder.info(
                f"ACTIVE STATE -> {state.value}"
            )

            time.sleep(0.25)

        result = runtime.run(
            text_input,
            options,
            writing_mode
        )

        st.success(
            f"MODE -> {result['mode'].value}"
        )

        st.metric(
            "TENSION SCORE",
            result["tension_score"]
        )

        st.divider()

        st.subheader("CONTRADICTIONS")

        if result["contradictions"]:

            for contradiction in result["contradictions"]:

                st.warning(
                    f"[{contradiction.contradiction_type}] "
                    f"Sentence #{contradiction.sentence_index}\n\n"
                    f"{contradiction.text}"
                )

        else:

            st.success(
                "Nem detektált rendszerfeszültséget."
            )

        st.divider()

        st.subheader("DECISION MATRIX")

        for idx, decision in enumerate(
            result["decisions"]
        ):

            if idx == 0:

                st.success(
                    f"WINNER -> {decision['name']} | "
                    f"SCORE = {decision['score']}"
                )

            else:

                st.error(
                    f"ELIMINATED -> {decision['name']} | "
                    f"SCORE = {decision['score']}"
                )

            st.caption(
                f"Loss bearer: {decision['loss_bearer']} | "
                f"Responsibility: {decision['responsibility']}"
            )

        st.divider()

        st.subheader("FINAL REPORT")

        st.code(
            result["report"],
            language="text"
        )

    else:

        st.info(
            "A rendszer várakozik futtatásra."
        )

        st.markdown(
            """
            ### Runtime komponensek

            - NLP Contradiction Engine
            - Pressure Mapping
            - Multi-Axis Decision System
            - Strategic Elimination Logic
            - State Machine
            - Writing Engine
            - Memory Layer
            """
        )

# ==============================================================================
# FOOTER
# ==============================================================================

st.divider()

st.caption(
    "COGNITO FUSION MONOLITH v3.0 | "
    "Experimental Cognitive Runtime Interface"
)import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
