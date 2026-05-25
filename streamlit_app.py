# =============================================================================
# COGNITO ENGINE v3.5.1 × 9.4
# FULL STREAMLIT APP
# BLOCK 1 / 2
# =============================================================================
import fitz
import base64
from PIL import Image
import streamlit as st
import time
import json
import math
import re

from collections import Counter
from openai import OpenAI

from help_module import help_selectbox, help_toggle


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="COGNITO ENGINE v3.5.1 × 9.4",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# STYLE
# =============================================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #030711;
    color: #e5e5e5;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            #0a1128 0%,
            #010308 100%
        );
}

h1, h2, h3 {

    font-family: 'Orbitron', sans-serif !important;

    letter-spacing: 1.5px;

    text-shadow:
        0 0 10px rgba(0,255,180,0.3);
}

.stChatMessage,
.hud-box {

    background:
        rgba(10, 15, 30, 0.5) !important;

    backdrop-filter:
        blur(12px) !important;

    -webkit-backdrop-filter:
        blur(12px) !important;

    border:
        1px solid rgba(0, 255, 180, 0.25) !important;

    border-radius:
        12px !important;

    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.5),
        inset 0 0 15px rgba(0, 255, 180, 0.05) !important;
}

.collapse-alert {

    background:
        rgba(255,0,60,0.1);

    border:
        1px solid #ff003c;

    border-radius:
        8px;

    padding:
        15px;

    margin-bottom:
        15px;

    box-shadow:
        0 0 20px rgba(255,0,60,0.4),
        inset 0 0 10px rgba(255,0,60,0.1);

    font-family:
        'Orbitron', sans-serif;

    color:
        #ff003c;

    text-shadow:
        0 0 8px #ff003c;
}

.cost-box {

    background:
        rgba(255, 170, 0, 0.1);

    border:
        1px solid rgba(255, 170, 0, 0.4);

    border-radius:
        8px;

    padding:
        12px;

    text-align:
        center;

    font-family:
        'Orbitron', sans-serif;

    color:
        #ffaa00;

    box-shadow:
        0 0 15px rgba(255, 170, 0, 0.2);
}

.copyright {

    font-size:
        11px;

    color:
        #00ffb4;

    text-align:
        center;

    margin-top:
        40px;

    padding:
        12px;

    border:
        1px solid rgba(0, 255, 180, 0.25);

    border-radius:
        8px;

    background:
        rgba(0, 0, 0, 0.6);

    box-shadow:
        0 0 10px rgba(0,255,180,0.1);
}

.stButton > button {

    background:
        linear-gradient(
            90deg,
            #00ffb4,
            #00bfff
        ) !important;

    color:
        #000 !important;

    font-weight:
        bold;

    font-family:
        'Orbitron', sans-serif;

    border:
        none;

    border-radius:
        8px;

    box-shadow:
        0 0 15px rgba(0, 255, 180, 0.4) !important;

    transition:
        all 0.3s ease !important;
}

.stButton > button:hover {

    box-shadow:
        0 0 25px rgba(0, 255, 180, 0.8) !important;

    transform:
        scale(1.02) !important;
}

</style>
""", unsafe_allow_html=True)


# =============================================================================
# COST TRACKING
# =============================================================================

PRICE_PER_1M_INPUT = 5.0
PRICE_PER_1M_OUTPUT = 15.0


def update_cost(usage_obj):

    if usage_obj:

        in_t = usage_obj.prompt_tokens
        out_t = usage_obj.completion_tokens

        st.session_state.total_in_tokens += in_t
        st.session_state.total_out_tokens += out_t

        st.session_state.total_usd += (
            (in_t / 1000000) * PRICE_PER_1M_INPUT
            +
            (out_t / 1000000) * PRICE_PER_1M_OUTPUT
        )


# =============================================================================
# PATTERN ENGINE
# =============================================================================

class PatternEngine:

    def __init__(self):

        self.pos_markers = [
            "stabil",
            "biztonság",
            "siker",
            "hatékony",
            "nyereség",
            "növekedés",
            "fejlődés"
        ]

        self.neg_markers = [
            "összeomlás",
            "válság",
            "veszteség",
            "instabil",
            "hiba",
            "kockázat",
            "káosz"
        ]

        self.inversion_bridges = (
            r'\b(de|azonban|mégis|viszont|ellenben|noha|ugyanakkor)\b'
        )

    def check_polarity(self, text_chunk):

        low = text_chunk.lower()

        has_pos = any(
            w in low
            for w in self.pos_markers
        )

        has_neg = any(
            w in low
            for w in self.neg_markers
        )

        if has_pos and not has_neg:
            return 1

        if has_neg and not has_pos:
            return -1

        return 0

    def scan(self, text):

        if not text:

            return {
                "entropy": 0,
                "patterns": [],
                "sentences": []
            }

        sentences = re.split(
            r'(?<=[.!?]) +',
            text.strip()
        )

        patterns = []

        total = len(text)

        entropy = -sum(
            c / total * math.log2(c / total)
            for c in Counter(text).values()
        )

        for i, s in enumerate(sentences):

            if re.search(
                self.inversion_bridges,
                s.lower()
            ):

                parts = re.split(
                    self.inversion_bridges,
                    s.lower()
                )

                if len(parts) >= 3:

                    p_l = self.check_polarity(parts[0])

                    p_r = self.check_polarity(parts[2])

                    if (
                        (p_l == 1 and p_r == -1)
                        or
                        (p_l == -1 and p_r == 1)
                    ):

                        patterns.append({
                            "sentence_id": i + 1,
                            "text": s,
                            "diagnostic": "STRUCTURAL_INVERSION"
                        })

        return {
            "entropy": round(entropy, 2),
            "patterns": patterns,
            "sentences": sentences
        }


# =============================================================================
# TENSIONS
# =============================================================================

TENSION_KEYS = [

    "POWER_VS_LEGITIMACY",

    "ORDER_VS_ADAPTATION",

    "CENTRALIZATION_VS_RESILIENCE",

    "ABSTRACTION_VS_REALITY",

    "EFFICIENCY_VS_STABILITY",

    "IDENTITY_VS_INTEGRATION",

    "TRANSPARENCY_VS_CONTROL"
]


# =============================================================================
# MEMORY COMPILER
# =============================================================================

class MemoryCompiler:

    def __init__(self, client):

        self.client = client

    def compile_state(
        self,
        user_input,
        pattern_data
    ):

        prompt = f"""
COGNITO MEMORY COMPILER.

7D vektor JSON-t írj.

Inverziók:
{json.dumps(pattern_data['patterns'])}

SÉMA:
{{
    "tensions":
    {{
        "TENGELY_NEVE": float(0-1)
    }},

    "reality_anchors":
    [
        {{
            "entity": "string",
            "fact": "string"
        }}
    ]
}}
"""

        try:

            res = self.client.chat.completions.create(

                model="gpt-4o",

                response_format={
                    "type": "json_object"
                },

                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],

                temperature=0.1
            )

            return (
                json.loads(
                    res.choices[0].message.content
                ),
                res.usage
            )

        except Exception as e:

            st.error(
                f"Memory Compiler Error: {e}"
            )

            return None, None
            # =============================================================================
# STATE MACHINE
# =============================================================================

class StateMachine:

    def __init__(self, decay_rate=0.8):

        self.decay_rate = decay_rate

    def evaluate_collapse_topology(
        self,
        tensions,
        anchors_count
    ):

        if (
            tensions.get(
                "ABSTRACTION_VS_REALITY",
                0
            ) > 0.75
            and
            anchors_count == 0
        ):

            return {
                "status": "CRITICAL",
                "type": "NARRATIVE_DISCONNECT",
                "desc": "Nincs kapcsolat a valósággal."
            }

        if (
            tensions.get(
                "ORDER_VS_ADAPTATION",
                0
            ) > 0.7
            and
            tensions.get(
                "EFFICIENCY_VS_STABILITY",
                0
            ) > 0.7
        ):

            return {
                "status": "CRITICAL",
                "type": "RIGIDITY_DEATH_SPIRAL",
                "desc": "Merevedési halálspirál."
            }

        if (
            tensions.get(
                "POWER_VS_LEGITIMACY",
                0
            ) > 0.7
            and
            tensions.get(
                "TRANSPARENCY_VS_CONTROL",
                0
            ) > 0.7
        ):

            return {
                "status": "CRITICAL",
                "type": "LEGITIMACY_CRISIS",
                "desc": "Kontroll maximalizálása felemészti a legitimitást."
            }

        if (
            tensions
            and
            sum(tensions.values()) / len(TENSION_KEYS) > 0.55
        ):

            return {
                "status": "WARNING",
                "type": "PRESSURE_ACCUMULATION",
                "desc": "A rendszernyomás emelkedik."
            }

        return {
            "status": "STABLE",
            "type": "NOMINAL",
            "desc": "A kognitív erőtér kiegyenlített."
        }

    def update(
        self,
        history,
        new_json,
        raw_entropy
    ):

        if not new_json:
            return history

        tensions = new_json.get(
            "tensions",
            {}
        )

        anchors = new_json.get(
            "reality_anchors",
            []
        )

        state = {

            "tensions": {},

            "deltas": {},

            "anchors":
                history[-1].get(
                    "anchors",
                    []
                ) + anchors
                if history else anchors,

            "entropy": raw_entropy
        }

        for k in TENSION_KEYS:

            old_val = (
                history[-1]["tensions"].get(k, 0.0)
                if history else 0.0
            )

            new_val = max(
                float(tensions.get(k, 0)),
                old_val * self.decay_rate
            )

            state["tensions"][k] = round(
                new_val,
                2
            )

            state["deltas"][k] = round(
                new_val - old_val,
                2
            )

        state["topology"] = (
            self.evaluate_collapse_topology(
                state["tensions"],
                len(anchors)
            )
        )

        history.append(state)

        return history


# =============================================================================
# WRITING ENGINE
# =============================================================================

class WritingEngine:

    @staticmethod
    def generate_prompt(
        state,
        mode,
        web,
        out_fmt,
        switches,
        cur_state,
        pat
    ):

        sw_txt = "\n".join([
            f"{k}={v}"
            for k, v in switches.items()
        ])

        tensions_json = json.dumps(
            cur_state.get("tensions", {}),
            ensure_ascii=False,
            indent=2
        )

        patterns_json = json.dumps(
            pat.get("patterns", []),
            ensure_ascii=False,
            indent=2
        )

        return f"""
COGNITO ENGINE 3.5.1 PRO × 9.4
OMNI RUNTIME SYSTEM

[ACTIVE PROFILE]

STATE: {state}
MODE: {mode}
WEB: {web}
OUTPUT FORMAT: {out_fmt}

[SWITCHES]

{sw_txt}

[HUD CONTEXT]

ENTROPY:
{pat.get('entropy')}

TOPOLOGY:
{cur_state.get('topology', {}).get('type')}

TOPOLOGY DESCRIPTION:
{cur_state.get('topology', {}).get('desc')}

[TENSION FIELD]

{tensions_json}

[STRUCTURAL INVERSIONS]

{patterns_json}

====================================================================

CORE DIRECTIVES

- Ne legyél chatbot.
- Ne legyél asszisztens.
- Ne írj általános AI-szöveget.
- Kerüld a steril összefoglalást.
- Kerüld a LinkedIn-ritmust.
- Kerüld az üres publicisztikai paneleket.
- Kerüld az általános filozófiai ködöt.

====================================================================

OPERATING RULES

1. Minden állítás legyen konkrét.

2. Minden absztrakció után jöjjön konkrét példa.

3. Minden konfliktusnak legyen emberi ára.

4. A rendszer nevezze meg:
   - ki veszít,
   - hogyan veszít,
   - milyen mechanizmus miatt.

5. Ne simítsd el az ellentmondásokat.

6. Ne zárd le túl gyorsan a gondolatot.

7. Kerüld az AI-szagú átvezetéseket.

====================================================================

WRITING STYLE

- Sűrű.
- Analitikus.
- Kíméletlenül konkrét.
- Ritmusában enyhén aszimmetrikus.
- Kerülje a túl steril folyékonyságot.

====================================================================

OUTPUT STRUCTURE

RUN STATUS:
FRAME:
PARADOX:
MODEL SET:
INTERFERENCE:
REALITY COLLISION:
DECISION:
ELIMINATED PATHS:
LOSS:
CONSEQUENCE:
NEXT MOVE:

WRITING OUTPUT:
(Ez legyen a valódi végső szöveg.)

RESIDUAL TENSION:

====================================================================

MINDEN UTASÍTÁST MAGYARUL HAJTS VÉGRE.
"""


# =============================================================================
# SESSION STATE
# =============================================================================

for key in [

    "state_history",

    "chat_messages",

    "last_audio",

    "total_in_tokens",

    "total_out_tokens",

    "total_usd"
]:

    if key not in st.session_state:

        st.session_state[key] = (

            []
            if "messages" in key or "history" in key
            else (
                None
                if "audio" in key
                else 0
            )
        )


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    st.markdown(
        "### ⚙️ INIT MODULE 9.4"
    )

    run_state = help_selectbox(
        "STATE",
        [
            "FOG",
            "SPARK",
            "CUT",
            "PRESSURE",
            "COLLISION",
            "BREAK",
            "ALCHEMY"
        ],
        index=5,
        key="state"
    )

    run_mode = help_selectbox(
        "MODE",
        [
            "QUICK",
            "BALANCED",
            "DEEP",
            "CREATIVE",
            "SCIENTIFIC"
        ],
        index=2,
        key="mode"
    )

    web_mode = help_selectbox(
        "WEB",
        [
            "OFF",
            "AUTO",
            "ON"
        ],
        index=1,
        key="web"
    )

    out_format = help_selectbox(
        "OUTPUT FORMAT",
        [
            "POLITICAL PAMPHLET",
            "STRATEGIC MEMO",
            "PRODUCT DESCRIPTION",
            "FULL TEXT"
        ],
        index=3,
        key="output"
    )

    st.markdown(
        "### 🎛️ GLOBAL SWITCHES"
    )

    switches = {

        k: help_toggle(
            k,
            value=True,
            key=f"toggle_{k}"
        )

        for k in [
            "ENGINE_MODE",
            "OPEN_SYSTEM",
            "DECISION_MODE",
            "VALIDATION_MODE",
            "ANTI_CLOSURE",
            "LOSS_TRACKING"
        ]
    }

    st.divider()

    st.markdown(
        "### 💸 RUNTIME COST"
    )

    st.markdown(
        f"""
<div class='cost-box'>

TOTAL:
<b>${st.session_state.total_usd:.4f}</b>

<br>

<span style='font-size:10px;color:#ccc;'>

IN:
{st.session_state.total_in_tokens}

|

OUT:
{st.session_state.total_out_tokens}

</span>

</div>
""",
        unsafe_allow_html=True
    )

    if st.button("🗑️ PURGE MEMORY"):

        st.session_state.state_history = []

        st.session_state.chat_messages = []

        st.session_state.total_usd = 0.0

        st.rerun()

    st.markdown(
        """
<div class='copyright'>

Concept & Design:

<br>

<b>Apáti Balázs / CSAPATI</b>

<br>

<span style='color:white;'>

COGNITO ENGINE v3.5.1 PRO × 9.4

</span>

</div>
""",
        unsafe_allow_html=True
    )


# =============================================================================
# LOGO & OPENAI
# =============================================================================

try:

    st.image(
        "logo.png",
        use_container_width=True
    )

except:

    try:

        st.image(
            "logo.jpg",
            use_container_width=True
        )

    except:

        st.markdown(
            "<h1 style='text-align:center;'>⬛ COGNITO ENGINE PRO</h1>",
            unsafe_allow_html=True
        )

if "OPENAI_API_KEY" not in st.secrets:

    st.error("API KEY MISSING!")

    st.stop()

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

pat_eng = PatternEngine()

comp = MemoryCompiler(client)

st_mach = StateMachine()
# =============================================================================
# HUD
# =============================================================================

if st.session_state.state_history:

    st.markdown(
        "### 📡 COGNITIVE HUD",
        unsafe_allow_html=True
    )

    cur = st.session_state.state_history[-1]

    if cur['topology']['status'] == "CRITICAL":

        st.markdown(
            f"""
<div class='collapse-alert'>
⚠️ <b>TOPOLOGICAL COLLAPSE:</b>
{cur['topology']['type']}
<br>
{cur['topology']['desc']}
</div>
""",
            unsafe_allow_html=True
        )

    c1, c2 = st.columns([2.5, 1])

    with c1:

        with st.expander(
            "VECTOR FIELD (7D GRAVITY)",
            expanded=True
        ):

            for k in TENSION_KEYS:

                color = (
                    "🔵"
                    if cur['tensions'][k] > 0.7
                    else "⚪"
                )

                st.write(
                    f"{color} **{k}:** {cur['tensions'][k]:.2f}"
                )

    with c2:

        st.metric(
            "ENTROPY",
            f"{cur['entropy']:.2f}"
        )


# ============================================================================

# ============================================================
# COGNITO RUNTIME SHELL v7
# REAL FRONTEND / BACKEND BRIDGE
# CHATGPT-LIKE CYBERPUNK INTERFACE
# ============================================================

import streamlit as st
import streamlit.components.v1 as components

import json
import hashlib
import fitz

# ============================================================
# SESSION STATE
# ============================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "runtime_prompt" not in st.session_state:
    st.session_state.runtime_prompt = ""

if "runtime_uploaded_text" not in st.session_state:
    st.session_state.runtime_uploaded_text = ""

if "runtime_audio_text" not in st.session_state:
    st.session_state.runtime_audio_text = ""

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
GLOBAL
========================================================= */

html,
body,
[data-testid="stAppViewContainer"] {

    background:
        radial-gradient(
            circle at top,
            #08111f 0%,
            #040816 60%,
            #02030a 100%
        );

    color:white;
}

/* =========================================================
CHAT MESSAGE
========================================================= */

[data-testid="stChatMessage"] {

    background:
        rgba(12,18,28,0.74);

    border:
        1px solid rgba(0,255,255,0.12);

    border-radius:20px;

    padding:16px;

    margin-bottom:18px;

    backdrop-filter:blur(14px);

    box-shadow:
        0 0 24px rgba(0,255,255,0.04);
}

/* =========================================================
HIDE DEFAULT STREAMLIT INPUTS
========================================================= */

[data-testid="stChatInput"] {
    display:none;
}

.stButton {
    display:none;
}

/* =========================================================
FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {

    position:fixed;

    bottom:95px;

    left:20px;

    width:1px;

    height:1px;

    opacity:0;

    z-index:-999;
}

/* =========================================================
AUDIO INPUT
========================================================= */

[data-testid="stAudioInput"] {

    position:fixed;

    bottom:95px;

    left:20px;

    width:1px;

    height:1px;

    opacity:0;

    z-index:-999;
}

/* =========================================================
COMPOSER WRAP
========================================================= */

.cog-shell-wrap {

    position:fixed;

    bottom:18px;

    left:50%;

    transform:translateX(-50%);

    width:min(920px,96vw);

    z-index:999999;
}

/* =========================================================
COMPOSER
========================================================= */

.cog-shell {

    display:flex;

    align-items:center;

    gap:10px;

    background:
        rgba(10,16,28,0.92);

    border:
        1px solid rgba(0,255,255,0.12);

    border-radius:24px;

    padding:12px;

    backdrop-filter:blur(18px);

    box-shadow:
        0 0 34px rgba(0,255,255,0.08);
}

/* =========================================================
ICON BUTTONS
========================================================= */

.cog-btn {

    width:44px;

    height:44px;

    border-radius:14px;

    border:
        1px solid rgba(0,255,255,0.14);

    background:
        rgba(0,255,255,0.05);

    color:white;

    font-size:18px;

    cursor:pointer;

    transition:0.2s;
}

.cog-btn:hover {

    background:
        rgba(0,255,255,0.14);

    box-shadow:
        0 0 12px rgba(0,255,255,0.18);
}

/* =========================================================
INPUT
========================================================= */

.cog-input {

    flex:1;

    border:none;

    outline:none;

    border-radius:18px;

    background:
        rgba(18,24,38,0.96);

    border:
        1px solid rgba(0,255,255,0.10);

    color:white;

    font-size:16px;

    padding:14px 16px;
}

/* =========================================================
SEND BUTTON
========================================================= */

.cog-send {

    width:52px;

    height:52px;

    border:none;

    border-radius:18px;

    background:
        linear-gradient(
            135deg,
            #00f5a0,
            #00bbff
        );

    color:black;

    font-size:24px;

    font-weight:bold;

    cursor:pointer;

    transition:0.2s;
}

.cog-send:hover {

    transform:scale(1.05);

    box-shadow:
        0 0 20px rgba(0,255,255,0.28);
}

/* =========================================================
COPY BUTTON
========================================================= */

.cog-copy {

    background:
        rgba(0,255,255,0.08);

    border:
        1px solid rgba(0,255,255,0.16);

    color:white;

    border-radius:10px;

    padding:6px 10px;

    cursor:pointer;
}

/* =========================================================
BOTTOM SPACE
========================================================= */

.cog-bottom-space {

    height:140px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HIDDEN REAL FILE INPUT
# ============================================================

uploaded_file = st.file_uploader(
    "hidden upload",
    type=["txt", "pdf", "png", "jpg", "jpeg"],
    key="hidden_runtime_upload"
)

# ============================================================
# HIDDEN REAL AUDIO INPUT
# ============================================================

audio_file = st.audio_input(
    "hidden audio",
    key="hidden_runtime_audio"
)

# ============================================================
# FILE PROCESSING
# ============================================================

if uploaded_file is not None:

    current_file_id = (
        f"{uploaded_file.name}_{uploaded_file.size}"
    )

    if (
        st.session_state.last_uploaded_file
        != current_file_id
    ):

        st.session_state.last_uploaded_file = (
            current_file_id
        )

        file_name = uploaded_file.name.lower()

        parsed_text = ""

        try:

            # TXT
            if file_name.endswith(".txt"):

                parsed_text = (
                    uploaded_file.read().decode(
                        "utf-8",
                        errors="ignore"
                    )
                )

            # PDF
            elif file_name.endswith(".pdf"):

                pdf_bytes = uploaded_file.read()

                pdf = fitz.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                )

                pages = []

                for page in pdf:

                    pages.append(
                        page.get_text()
                    )

                parsed_text = (
                    "\n".join(pages)
                )

            # IMAGE
            elif (
                file_name.endswith(".png")
                or file_name.endswith(".jpg")
                or file_name.endswith(".jpeg")
            ):

                st.image(
                    uploaded_file,
                    use_container_width=True
                )

                parsed_text = (
                    "[IMAGE INPUT DETECTED]"
                )

            st.session_state.runtime_uploaded_text = (
                parsed_text
            )

            st.toast(
                "📎 File processed"
            )

        except Exception as e:

            st.error(
                f"FILE ERROR: {e}"
            )

else:

    st.session_state.last_uploaded_file = None

# ============================================================
# AUDIO PROCESSING
# ============================================================

if audio_file is not None:

    audio_bytes = audio_file.getvalue()

    current_audio_hash = hashlib.md5(
        audio_bytes
    ).hexdigest()

    if (
        st.session_state.last_audio_hash
        != current_audio_hash
    ):

        st.session_state.last_audio_hash = (
            current_audio_hash
        )

        with st.spinner(
            "🎧 Audio processing..."
        ):

            transcript = (
                client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            )

            st.session_state.runtime_audio_text = (
                transcript.text
            )

            st.toast(
                "🎤 Voice processed"
            )

else:

    st.session_state.last_audio_hash = None

# ============================================================
# CHAT HISTORY
# ============================================================

for msg in st.session_state.chat_messages:

    with st.chat_message(
        msg["role"],
        avatar="👤" if msg["role"] == "user" else "◼️"
    ):

        st.markdown(
            msg["content"]
        )

        # COPY
        if msg["role"] == "assistant":

            safe_json = json.dumps(
                msg["content"]
            )

            copy_html = f"""
            <div style="
            display:flex;
            justify-content:flex-end;
            margin-top:10px;
            ">
            <button
            class="cog-copy"
            onclick='
            navigator.clipboard.writeText({safe_json});
            this.innerText="✅";
            setTimeout(() => {{
                this.innerText="📋";
            }},1200);
            '
            >
            📋
            </button>
            </div>
            """

            components.html(
                copy_html,
                height=42
            )

# ============================================================
# REAL INPUT BRIDGE
# ============================================================

runtime_input = st.text_input(
    "hidden runtime bridge",
    key="hidden_runtime_bridge",
    label_visibility="collapsed"
)

# ============================================================
# FRONTEND RUNTIME SHELL
# ============================================================

components.html("""
<div class="cog-shell-wrap">

<div class="cog-shell">

<button
class="cog-btn"
onclick="
window.parent.document
.querySelector('[data-testid=stFileUploader] button')
.click();
"
>
📎
</button>

<button
class="cog-btn"
onclick="
window.parent.document
.querySelector('[data-testid=stAudioInput] button')
.click();
"
>
🎤
</button>

<input
id="cog_runtime_input"
class="cog-input"
placeholder="Írd be a futtatandó témát..."
/>

<button
class="cog-send"
onclick="
const val =
document.getElementById(
'cog_runtime_input'
).value;

const inputs =
window.parent.document
.querySelectorAll('input');

inputs.forEach(el => {

if (
el.getAttribute('aria-label')
=== 'hidden runtime bridge'
) {

const nativeInputValueSetter =
Object.getOwnPropertyDescriptor(
window.HTMLInputElement.prototype,
'value'
).set;

nativeInputValueSetter.call(
el,
val
);

el.dispatchEvent(
new Event(
'input',
{ bubbles:true }
)
);
}
});
"
>
➤
</button>

</div>

</div>

<div class="cog-bottom-space"></div>
""", height=120)

# ============================================================
# EXECUTION ENGINE
# ============================================================

if runtime_input:

    final_input = runtime_input

    # AUDIO MERGE
    if (
        st.session_state.runtime_audio_text
    ):

        final_input += (
            "\n\n[VOICE INPUT]\n\n"
            +
            st.session_state.runtime_audio_text
        )

    # FILE MERGE
    if (
        st.session_state.runtime_uploaded_text
    ):

        final_input += (
            "\n\n[FILE INPUT]\n\n"
            +
            st.session_state.runtime_uploaded_text
        )

    # ========================================================
    # SAVE USER
    # ========================================================

    st.session_state.chat_messages.append({
        "role":"user",
        "content":final_input
    })

    # ========================================================
    # STATUS
    # ========================================================

    with st.status(
        "⚙️ COGNITO Runtime aktív...",
        expanded=True
    ) as status:

        pat_data = pat_eng.scan(
            final_input
        )

        new_json, comp_use = (
            comp.compile_state(
                final_input,
                pat_data
            )
        )

        update_cost(
            comp_use
        )

        st.session_state.state_history = (
            st_mach.update(
                st.session_state.state_history,
                new_json,
                pat_data["entropy"]
            )
        )

        status.update(
            label="✅ Runtime state updated",
            state="complete"
        )

    # ========================================================
    # PROMPT BUILD
    # ========================================================

    final_prompt = (
        WritingEngine.generate_prompt(
            run_state,
            run_mode,
            web_mode,
            out_format,
            switches,
            st.session_state.state_history[-1],
            pat_data
        )
    )

    # ========================================================
    # MODEL
    # ========================================================

    response = (
        client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role":"system",
                    "content":final_prompt
                },
                {
                    "role":"user",
                    "content":final_input
                }
            ]
        )
    )

    out = (
        response
        .choices[0]
        .message.content
    )

    update_cost(
        response.usage
    )

    # ========================================================
    # SAVE ASSISTANT
    # ========================================================

    st.session_state.chat_messages.append({
        "role":"assistant",
        "content":out
    })

    # ========================================================
    # CLEAR
    # ========================================================

    st.session_state.runtime_uploaded_text = ""
    st.session_state.runtime_audio_text = ""
    st.session_state.hidden_runtime_bridge = ""

    st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "COGNITO ENGINE PRO — Runtime Shell v7"
)
