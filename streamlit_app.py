# ==============================================================================
# COGNITO ARCHITECTURE v5.0 — TOPOLOGICAL RUNTIME & HYBRID COGNITION
# Concept, Architecture & Design: Apáti Balázs / CSAPATI
# All Rights Reserved.
# ==============================================================================

import streamlit as st
import time
import json
import math
import re
from collections import Counter
from openai import OpenAI

# ==============================================================================
# PAGE CONFIG & CYBERPUNK CSS
# ==============================================================================
st.set_page_config(page_title="COGNITO v5.0 | Topological Runtime", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050505; color: #e5e5e5; }
.stApp { background: linear-gradient(180deg, #040404 0%, #090909 100%); }
h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; }
.terminal-box { background: rgba(0,0,0,0.6); border: 1px solid rgba(0,255,180,0.2); border-radius: 12px; padding: 18px; margin-bottom: 15px;}
.metric-box { background: rgba(20,20,20,0.8); border-left: 3px solid #00ffb4; padding: 10px; margin-bottom: 5px; font-family: monospace; font-size: 12px;}
.collapse-alert { background: rgba(255,0,0,0.1); border-left: 3px solid #ff003c; padding: 15px; margin-bottom: 15px; border-radius: 4px; font-family: 'Orbitron', sans-serif; color: #ff003c; }
.stButton > button { width: 100%; background: linear-gradient(90deg, #00ffb4, #00bfff); color: black; font-weight: bold; border: none; border-radius: 12px; }
.stChatMessage { background-color: rgba(20, 20, 20, 0.8) !important; border: 1px solid rgba(0,255,180,0.15) !important; border-radius: 12px; }
.copyright { font-size: 10px; color: #555; text-align: center; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# I. PATTERN ENGINE (Structural Polarity Inversions)
# ==============================================================================
class PatternEngine:
    def __init__(self):
        self.pos_markers = ["stabil", "biztonság", "siker", "hatékony", "nyereség", "növekedés", "fejlődés", "bizalom", "támogatás"]
        self.neg_markers = ["összeomlás", "válság", "veszteség", "instabil", "hiba", "kockázat", "korrupció", "káosz", "csökkenés"]
        self.inversion_bridges = r'\b(de|azonban|mégis|viszont|ellenben|noha|ugyanakkor)\b'

    def check_polarity(self, text_chunk):
        chunk_low = text_chunk.lower()
        has_pos = any(w in chunk_low for w in self.pos_markers)
        has_neg = any(w in chunk_low for w in self.neg_markers)
        if has_pos and not has_neg: return 1
        if has_neg and not has_pos: return -1
        return 0

    def scan(self, text):
        if not text: return {"entropy": 0, "patterns": [], "sentences": []}
        
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        patterns = []
        
        # Matematikai Entrópia számolás (Fizikai zajszint)
        chars = Counter(text)
        total = len(text)
        entropy = -sum(count/total * math.log2(count/total) for count in chars.values())
        
        for i, s in enumerate(sentences):
            # Ha van benne polaritást fordító híd
            if re.search(self.inversion_bridges, s.lower()):
                parts = re.split(self.inversion_bridges, s.lower())
                if len(parts) >= 3:
                    left_chunk, right_chunk = parts[0], parts[2]
                    p_left = self.check_polarity(left_chunk)
                    p_right = self.check_polarity(right_chunk)
                    
                    # Ha a híd két oldala polaritásban kioltja egymást -> STRUCTURAL INVERSION
                    if (p_left == 1 and p_right == -1) or (p_left == -1 and p_right == 1):
                        patterns.append({
                            "sentence_id": i+1, 
                            "text": s, 
                            "diagnostic": "STRUCTURAL_INVERSION (Polarity Clash)"
                        })

        return {"entropy": round(entropy, 2), "patterns": patterns, "sentences": sentences}

# ==============================================================================
# II. MEMORY COMPILER (LLM Translation to Canon Ontology)
# ==============================================================================
TENSION_KEYS = ["POWER_VS_LEGITIMACY", "ORDER_VS_ADAPTATION", "CENTRALIZATION_VS_RESILIENCE", "ABSTRACTION_VS_REALITY", "EFFICIENCY_VS_STABILITY", "IDENTITY_VS_INTEGRATION", "TRANSPARENCY_VS_CONTROL"]

class MemoryCompiler:
    def __init__(self, client):
        self.client = client
        
    def compile_state(self, user_input, pattern_data):
        system_prompt = f"""
        COGNITO MEMORY COMPILER. 
        Feladatod a nyers input 7-dimenziós gravitációs vektortérré alakítása.
        Kizárólag JSON formátumban válaszolj!
        Pattern Engine által detektált inverziók: {json.dumps(pattern_data['patterns'])}
        
        SÉMA:
        {{
            "tensions": {{
                "POWER_VS_LEGITIMACY": float, "ORDER_VS_ADAPTATION": float, 
                "CENTRALIZATION_VS_RESILIENCE": float, "ABSTRACTION_VS_REALITY": float, 
                "EFFICIENCY_VS_STABILITY": float, "IDENTITY_VS_INTEGRATION": float, 
                "TRANSPARENCY_VS_CONTROL": float
            }},
            "reality_anchors": [ {{"entity": "string", "fact": "string"}} ]
        }}
        """
        try:
            res = self.client.chat.completions.create(
                model="gpt-4o", response_format={"type": "json_object"},
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
                temperature=0.1
            )
            return json.loads(res.choices[0].message.content)
        except: return None

# ==============================================================================
# III. TOPOLOGICAL STATE MACHINE (Configuration Collapse Engine)
# ==============================================================================
class StateMachine:
    def __init__(self, decay_rate=0.8):
        self.decay_rate = decay_rate
        
    def evaluate_collapse_topology(self, tensions, deltas, anchors_count):
        """A buta átlagolás helyett konfigurációs mintázatokat keres."""
        
        # 1. NARRATIVE DISCONNECT (A rendszer retorikája elszakadt a valóságtól)
        if tensions.get("ABSTRACTION_VS_REALITY", 0) > 0.75 and anchors_count == 0:
            return {"status": "CRITICAL", "type": "NARRATIVE_DISCONNECT", "desc": "A rendszer elvesztette a kapcsolatot a verifikálható valósággal. Magas absztrakciós zaj."}
            
        # 2. RIGIDITY DEATH SPIRAL (Túl optimalizált, túlszabályozott, képtelen adaptálódni)
        if tensions.get("ORDER_VS_ADAPTATION", 0) > 0.7 and tensions.get("EFFICIENCY_VS_STABILITY", 0) > 0.7:
            return {"status": "CRITICAL", "type": "RIGIDITY_DEATH_SPIRAL", "desc": "Merevedési halálspirál. A rendszer a stabilitást védi a végsőkig, megbénítva a belső folyamatokat."}
            
        # 3. LEGITIMACY CRISIS (A hatalom nő, de a transzparencia csökken)
        if tensions.get("POWER_VS_LEGITIMACY", 0) > 0.7 and tensions.get("TRANSPARENCY_VS_CONTROL", 0) > 0.7:
            return {"status": "CRITICAL", "type": "LEGITIMACY_CRISIS", "desc": "A kontroll és a hatalom maximalizálása felemészti a belső legitimitást."}
            
        # Ha a feszültségek magasak, de nincs konfigurációs összeomlás
        avg_t = sum(tensions.values()) / len(TENSION_KEYS)
        if avg_t > 0.55:
            return {"status": "WARNING", "type": "PRESSURE_ACCUMULATION", "desc": "A rendszernyomás emelkedik, de a topológia egyelőre stabil."}
            
        return {"status": "STABLE", "type": "NOMINAL", "desc": "A kognitív erőtér kiegyenlített."}
        
    def update(self, history, new_json, raw_entropy):
        if not new_json: return history
        tensions = new_json.get("tensions", {})
        anchors = new_json.get("reality_anchors", [])
        
        if not history:
            state = {"tensions": {k: float(tensions.get(k, 0)) for k in TENSION_KEYS}, "deltas": {k: 0.0 for k in TENSION_KEYS}, "anchors": anchors, "entropy": raw_entropy}
        else:
            last = history[-1]
            state = {"tensions": {}, "deltas": {}, "anchors": last.get("anchors", []) + anchors, "entropy": raw_entropy}
            for k in TENSION_KEYS:
                old_val = last["tensions"].get(k, 0.0)
                new_val = max(float(tensions.get(k, 0)), old_val * self.decay_rate)
                state["tensions"][k] = round(new_val, 2)
                state["deltas"][k] = round(new_val - old_val, 2)
                
        # Topológiai kiértékelés
        state["topology"] = self.evaluate_collapse_topology(state["tensions"], state["deltas"], len(anchors))
        history.append(state)
        return history

# ==============================================================================
# IV. WRITING ENGINE (Translation to Final Output)
# ==============================================================================
class WritingEngine:
    @staticmethod
    def generate_prompt(density, gravity, rhythm, output_mode, current_state, pattern_data):
        formatting_rules = ""
        if rhythm == "FRACTURED": formatting_rules = "Használj sok rövid, tördelt mondatot. Minden gondolatot új sorban kezdj, dupla sorközzel."
        elif rhythm == "CASCADING": formatting_rules = "A mondatok logikailag egymásba folyjanak, használj nyíllal (->) jelölt ok-okozati felsorolásokat."
        
        return f"""
        Te a COGNITO WRITING ENGINE vagy. Feladatod a kognitív állapot szöveges dekódolása.
        
        ÍRÁSI FIZIKA:
        Sűrűség: {density} | Gravitáció: {gravity} | Mód: {output_mode}
        Ritmus/Formázás: {formatting_rules}
        
        BELSŐ ÁLLAPOTGÉP DIAGNÓZIS (TOPOLOGY):
        - Státusz: {current_state['topology']['status']}
        - Típus: {current_state['topology']['type']}
        - Leírás: {current_state['topology']['desc']}
        
        KOGNITÍV METRIKÁK:
        - Rendszer Entrópia: {pattern_data['entropy']}
        - Legmagasabb Feszültség-vektorok: {json.dumps({k:v for k,v in current_state['tensions'].items() if v > 0.5})}
        - Pattern Engine Inverziók: {json.dumps(pattern_data['patterns'])}
        
        UTASÍTÁS:
        Írj magyar nyelvű, professzionális elemzést az utolsó inputról. Építsd be a szövegbe a belső állapotgép diagnózisát ({current_state['topology']['type']}). Ha a státusz CRITICAL, a stílusod legyen kíméletlen és fatalista. Ne magyarázd a kódot, csak viselkedj elemzőként.
        """

# ==============================================================================
# V. APP & UI RUNTIME
# ==============================================================================
if "state_history" not in st.session_state: st.session_state.state_history = []
if "chat_messages" not in st.session_state: st.session_state.chat_messages = []
if "last_audio" not in st.session_state: st.session_state.last_audio = None

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM INIT v5.0")
    density = st.select_slider("Density", ["LOW", "MEDIUM", "HIGH"], value="HIGH")
    gravity = st.select_slider("Gravity", ["LIGHT", "CONTROLLED", "HEAVY"], value="HEAVY")
    rhythm = st.selectbox("Rhythm", ["FLAT", "PULSED", "FRACTURED", "CASCADING"])
    output_mode = st.selectbox("Output Mode", ["ANALYTIC NOIR", "STRATEGIC MEMO", "SYSTEMIC COLLAPSE"])
    if st.button("🗑️ PURGE MEMORY"):
        st.session_state.state_history, st.session_state.chat_messages = [], []
        st.rerun()
    st.markdown("<div class='copyright'>Concept & Design: Apáti Balázs / CSAPATI<br>Cognito Architecture v5.0</div>", unsafe_allow_html=True)

st.title("⬛ COGNITO POST-MONOLITH")
st.caption("v5.0 | Topological Runtime | Pattern Engine | Architect: Apáti Balázs / CSAPATI")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("🚨 HIBA: OPENAI_API_KEY hiányzik a Secrets-ből!")
    st.stop()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pattern_engine, compiler, state_machine = PatternEngine(), MemoryCompiler(client), StateMachine()

# HUD
if st.session_state.state_history:
    st.markdown("### 📡 COGNITIVE HUD")
    cur = st.session_state.state_history[-1]
    
    if cur['topology']['status'] == "CRITICAL":
        st.markdown(f"<div class='collapse-alert'>⚠️ TOPOLOGICAL COLLAPSE DETECTED: {cur['topology']['type']}<br><span style='font-size:12px;color:#ccc;'>{cur['topology']['desc']}</span></div>", unsafe_allow_html=True)
    elif cur['topology']['status'] == "WARNING":
        st.warning(f"⚡ {cur['topology']['type']}: {cur['topology']['desc']}")
        
    c1, c2 = st.columns([2.5, 1])
    with c1:
        with st.expander("VECTOR FIELD (7D GRAVITY)", expanded=True):
            for k in TENSION_KEYS:
                color = "🔴" if cur['tensions'][k] > 0.7 else "⚪"
                st.write(f"{color} **{k}:** {cur['tensions'][k]:.2f} (Δ {cur['deltas'][k]:+.2f})")
    with c2:
        st.metric("ENTROPY", f"{cur['entropy']:.2f}")
        st.metric("REALITY ANCHORS", len(cur['anchors']))
    st.divider()

user_query = None
is_initial = False

if not st.session_state.chat_messages:
    topic_input = st.text_area("RENDSZER-INPUT (Nyers szöveg)", height=150)
    if st.button("⚡ EXECUTE COGNITIVE PIPELINE") and topic_input:
        user_query, is_initial = topic_input, True
else:
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="⬛" if msg["role"] == "assistant" else "👤"): st.markdown(msg["content"])
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if txt := st.chat_input("Új input vagy direktíva..."): user_query = txt
    with col2:
        if audio := st.audio_input("🎤 Voice"):
            if st.session_state.last_audio != audio.name:
                st.session_state.last_audio = audio.name
                user_query = client.audio.transcriptions.create(model="whisper-1", file=audio).text

if user_query:
    if not is_initial:
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="👤"): st.markdown(user_query)

    with st.status("⚙️ Kognitív Architektúra Fut...", expanded=True) as status:
        st.write("1. Pattern Engine: Mondattani inverziók és Entrópia mérése...")
        pattern_data = pattern_engine.scan(user_query)
        
        st.write("2. Memory Compiler: 7D Gravitációs Vektorok generálása...")
        new_json = compiler.compile_state(user_query, pattern_data)
        
        st.write("3. State Machine: Topológiai Analízis...")
        st.session_state.state_history = state_machine.update(st.session_state.state_history, new_json, pattern_data['entropy'])
        
        status.update(label="✅ Állapot frissítve. Dekódolás...", state="complete", expanded=False)
    
    prompt = WritingEngine.generate_prompt(density, gravity, rhythm, output_mode, st.session_state.state_history[-1], pattern_data)
    
    with st.chat_message("assistant", avatar="⬛"):
        resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_query}])
        out = resp.choices[0].message.content
        st.markdown(out)
        st.session_state.chat_messages.append({"role": "assistant", "content": out})
        
    if is_initial: st.rerun()
