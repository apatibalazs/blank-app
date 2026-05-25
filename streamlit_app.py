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
        (

# ========================================================= 
# ============================================================
# INIT MODULE
# RUNTIME INPUT SYSTEM
# COGNITO RUNTIME SHELL v22
# FINAL AUDITED MOBILE STABLE
# ============================================================

import streamlit as st
import streamlit.components.v1 as components

import json

from openai import OpenAI

# ============================================================
# ENGINE INITIALIZATION
# ============================================================

if "engine_initialized" not in st.session_state:

    st.session_state.client = OpenAI(
        api_key=st.secrets.get(
            "OPENAI_API_KEY",
            ""
        )
    )

    st.session_state.pat_eng = (
        PatternEngine()
    )

    st.session_state.comp = (
        MemoryCompiler(
            st.session_state.client
        )
    )

    st.session_state.st_mach = (
        StateMachine()
    )

    st.session_state.engine_initialized = True

# ============================================================
# SESSION STATE
# ============================================================

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

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
            #081320 0%,
            #030712 60%,
            #01040a 100%
        );

    color:white;
}

/* =========================================================
HIDE STREAMLIT INPUTS
========================================================= */

[data-testid="stTextInput"],
[data-testid="stChatInput"],
.stButton {

    opacity:0 !important;

    height:0 !important;

    overflow:hidden !important;
}

/* =========================================================
KEEP SUBMIT ACTIVE
========================================================= */

button[kind="secondaryFormSubmit"],
[data-testid="stFormSubmitButton"] {

    position:absolute !important;

    left:-9999px !important;

    width:1px !important;

    height:1px !important;

    opacity:0.01 !important;
}

/* =========================================================
KEEP FORM IN DOM
========================================================= */

div[data-testid="stForm"] {

    position:absolute !important;

    opacity:0 !important;

    height:0 !important;

    overflow:hidden !important;

    z-index:-1 !important;
}

/* =========================================================
CHAT MESSAGE
========================================================= */

[data-testid="stChatMessage"] {

    background:
        rgba(10,18,30,0.72);

    border:
        1px solid rgba(0,255,255,0.10);

    border-radius:22px;

    padding:18px;

    margin-bottom:18px;

    backdrop-filter:blur(12px);

    box-shadow:
        0 0 24px rgba(0,255,255,0.04);
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
# HIDDEN FORM
# ============================================================

with st.form(
    key="runtime_form",
    clear_on_submit=True
):

    hidden_prompt = st.text_input(
        "runtime_hidden_input",
        key="runtime_hidden_input",
        label_visibility="collapsed"
    )

    submit_hidden = st.form_submit_button(
        "submit"
    )

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

        # ====================================================
        # COPY BUTTON
        # ====================================================

        if msg["role"] == "assistant":

            safe_text = json.dumps(
                msg["content"]
            )

            components.html(f"""
            <div style="
                display:flex;
                justify-content:flex-end;
                margin-top:10px;
            ">

            <button
                onclick='
                    navigator.clipboard.writeText({safe_text});

                    this.innerText="✅";

                    setTimeout(() => {{
                        this.innerText="📋";
                    }},1200);
                '

                style="
                    background:
                        rgba(0,255,255,0.08);

                    border:
                        1px solid rgba(0,255,255,0.18);

                    color:white;

                    border-radius:10px;

                    padding:6px 10px;

                    cursor:pointer;

                    font-size:13px;
                "
            >
                📋
            </button>

            </div>
            """, height=46)

# ============================================================
# FRONTEND SHELL
# ============================================================

components.html("""

<style>

/* =========================================================
WRAP
========================================================= */

#cog-wrap {

    position:fixed;

    left:50%;

    bottom:10px;

    transform:translateX(-50%);

    width:min(920px,96vw);

    z-index:999999;
}

/* =========================================================
COMPOSER
========================================================= */

#cog-composer {

    width:100%;

    display:flex;

    align-items:center;

    gap:8px;

    padding:10px;

    min-height:76px;

    border-radius:26px;

    background:
        rgba(8,14,24,0.96);

    border:
        1px solid rgba(0,255,255,0.14);

    backdrop-filter:
        blur(18px);

    box-shadow:
        0 0 30px rgba(0,255,255,0.08);

    box-sizing:border-box;
}

/* =========================================================
BUTTONS
========================================================= */

.cog-btn {

    width:50px;

    height:50px;

    border:none;

    border-radius:16px;

    background:
        rgba(0,255,255,0.06);

    border:
        1px solid rgba(0,255,255,0.16);

    color:white;

    font-size:20px;

    cursor:pointer;

    flex-shrink:0;
}

/* =========================================================
TEXTAREA
========================================================= */

#cog-input {

    flex:1;

    min-width:0;

    min-height:54px;

    max-height:160px;

    resize:none;

    border:none;

    outline:none;

    border-radius:18px;

    background:
        rgba(18,24,38,0.96);

    border:
        1px solid rgba(0,255,255,0.10);

    color:white;

    font-size:16px;

    line-height:1.5;

    padding:14px 16px;

    overflow-y:hidden;

    box-sizing:border-box;
}

/* =========================================================
SEND BUTTON
========================================================= */

#send-btn {

    width:58px;

    height:58px;

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

    flex-shrink:0;
}

</style>

<div id="cog-wrap">

    <div id="cog-composer">

        <!-- FILE -->

        <button
            class="cog-btn"
            type="button"
        >
            📎
        </button>

        <!-- MIC -->

        <button
            class="cog-btn"
            id="mic-btn"
            type="button"
        >
            🎤
        </button>

        <!-- TEXTAREA -->

        <textarea
            id="cog-input"
            rows="1"
        ></textarea>

        <!-- SEND -->

        <button
            id="send-btn"
            type="button"
        >
            ➤
        </button>

    </div>

</div>

<div class="cog-bottom-space"></div>

<script>

/* =========================================================
ELEMENTS
========================================================= */

const textarea =
    document.getElementById(
        "cog-input"
    );

/* =========================================================
AUTOSIZE
========================================================= */

function autoResize() {

    textarea.style.height =
        "auto";

    textarea.style.height =
        Math.min(
            textarea.scrollHeight,
            160
        ) + "px";

    if (
        textarea.scrollHeight > 160
    ) {

        textarea.style.overflowY =
            "auto";
    }
    else {

        textarea.style.overflowY =
            "hidden";
    }
}

textarea.addEventListener(
    "input",
    autoResize
);

requestAnimationFrame(
    autoResize
);

/* =========================================================
VOICE
========================================================= */

let recognition = null;

if (
    "webkitSpeechRecognition"
    in window
) {

    recognition =
        new webkitSpeechRecognition();

    recognition.lang = "hu-HU";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.onresult =
        function(event) {

        const text =
            event.results[0][0]
            .transcript;

        textarea.value +=
            " " + text;

        autoResize();
    };
}

document
.getElementById(
    "mic-btn"
)
.onclick = function() {

    if (!recognition) return;

    recognition.start();
};

/* =========================================================
SUBMIT
========================================================= */

function submitPrompt() {

    const text =
        textarea.value.trim();

    if (!text) return;

    const hiddenInput =
        window.parent.document
        .querySelector(
            'input[aria-label="runtime_hidden_input"]'
        );

    if (!hiddenInput) {

        console.error(
            "Hidden input missing"
        );

        return;
    }

    /* =====================================================
    REACT SAFE VALUE SET
    ===================================================== */

    const nativeSetter =
        Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            "value"
        ).set;

    nativeSetter.call(
        hiddenInput,
        text
    );

    hiddenInput.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );

    hiddenInput.dispatchEvent(
        new Event(
            "change",
            {
                bubbles:true
            }
        )
    );

    /* =====================================================
    SUBMIT BUTTON
    ===================================================== */

    const submitBtn =
        window.parent.document
        .querySelector(
            'button[kind="secondaryFormSubmit"]'
        );

    if (submitBtn) {

        setTimeout(() => {

            submitBtn.click();

        }, 80);
    }

    /* =====================================================
    CLEAR
    ===================================================== */

    setTimeout(() => {

        textarea.value = "";

        textarea.style.height =
            "auto";

        requestAnimationFrame(
            autoResize
        );

    }, 600);
}

/* =========================================================
SEND BUTTON
========================================================= */

document
.getElementById(
    "send-btn"
)
.onclick = submitPrompt;

/* =========================================================
ENTER
========================================================= */

textarea.addEventListener(
    "keydown",
    function(e) {

        if (
            e.key === "Enter"
            &&
            !e.shiftKey
        ) {

            e.preventDefault();

            submitPrompt();
        }
    }
);

</script>

""", height=150)

# ============================================================
# EXECUTION ENGINE
# ============================================================

if submit_hidden and hidden_prompt:

    final_input = hidden_prompt

    st.session_state.chat_messages.append({
        "role":"user",
        "content":final_input
    })

    with st.status(
        "⚙️ COGNITO Runtime aktív...",
        expanded=True
    ) as status:

        pat_data = (
            st.session_state
            .pat_eng
            .scan(final_input)
        )

        new_json, comp_use = (
            st.session_state
            .comp
            .compile_state(
                final_input,
                pat_data
            )
        )

        update_cost(
            comp_use
        )

        st.session_state.state_history = (
            st.session_state
            .st_mach
            .update(
                st.session_state.state_history,
                new_json,
                pat_data["entropy"]
            )
        )

        status.update(
            label="✅ Runtime frissítve",
            state="complete"
        )

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

    response = (
        st.session_state
        .client
        .chat
        .completions
        .create(
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

    st.session_state.chat_messages.append({
        "role":"assistant",
        "content":out
    })

    st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "COGNITO ENGINE 17.0 PRO 😎"
)
