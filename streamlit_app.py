# ==============================================================================
# COGNITO ARCHITECTURE v5.1 — TOPOLOGICAL RUNTIME + COST TRACKER
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
st.set_page_config(page_title="COGNITO v5.1 | Cost Tracking", layout="wide", initial_sidebar_state="expanded")

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
.cost-box { background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 8px; padding: 10px; text-align: center; font-family: 'Orbitron', sans-serif; color: #ffd700; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 0. COST CALCULATOR (Token Taxióra)
# ==============================================================================
# GPT-4o árazás (példa: 5$ / 1M input, 15$ / 1M output)
PRICE_PER_1M_INPUT = 5.0
PRICE_PER_1M_OUTPUT = 15.0

def update_cost(usage_obj):
    if usage_obj:
        in_t = usage_obj.prompt_tokens
        out_t = usage_obj.completion_tokens
        st.session_state.total_in_tokens += in_t
        st.session_state.total_out_tokens += out_t
        cost = (in_t / 1000000) * PRICE_PER_1M_INPUT + (out_t / 1000000) * PRICE_PER_1M_OUTPUT
        st.session_state.total_usd += cost

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
        chars = Counter(text)
        total = len(text)
        entropy = -sum(count/total * math.log2(count/total) for count in chars.values())
        
        for i, s in enumerate(sentences):
            if re.search(self.inversion_bridges, s.lower()):
                parts = re.split(self.inversion_bridges, s.lower())
                if len(parts) >= 3:
                    p_left = self.check_polarity(parts[0])
                    p_right = self.check_polarity(parts[2])
                    if (p_left == 1 and p_right == -1) or (p_left == -1 and p_right == 1):
                        patterns.append({"sentence_id": i+1, "text": s, "diagnostic": "STRUCTURAL_INVERSION"})
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
        Feladatod a nyers input 7-dimenziós gravitációs vektortérré alakítása. Kizárólag JSON-t írj.
        Pattern Engine inverziók: {json.dumps(pattern_data['patterns'])}
        SÉMA: {{"tensions": {{"TENGELY_NEVE": float(0-1)}}, "reality_anchors": [{{"entity": "string", "fact": "string"}}]}}
        """
        try:
            res = self.client.chat.completions.create(
                model="gpt-4o", response_format={"type": "json_object"},
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
                temperature=0.1
            )
            # Most már visszaadjuk a felhasznált token adatokat (usage) is!
            return json.loads(res.choices[0].message.content), res.usage
        except: return None, None

# ==============================================================================
# III. TOPOLOGICAL STATE MACHINE (Configuration Collapse Engine)
# ==============================================================================
class StateMachine:
    def __init__(self, decay_rate=0.8):
        self.decay_rate = decay_rate
        
    def evaluate_collapse_topology(self, tensions, deltas, anchors_count):
        if tensions.get("ABSTRACTION_VS_REALITY", 0) > 0.75 and anchors_count == 0:
            return {"status": "CRITICAL", "type": "NARRATIVE_DISCONNECT", "desc": "Nincs kapcsolat a verifikálható valósággal."}
        if tensions.get("ORDER_VS_ADAPTATION", 0) > 0.7 and tensions.get("EFFICIENCY_VS_STABILITY", 0) > 0.7:
            return {"status": "CRITICAL", "type": "RIGIDITY_DEATH_SPIRAL", "desc": "Merevedési halálspirál."}
        if tensions.get("POWER_VS_LEGITIMACY", 0) > 0.7 and tensions.get("TRANSPARENCY_VS_CONTROL", 0) > 0.7:
            return {"status": "CRITICAL", "type": "LEGITIMACY_CRISIS", "desc": "Kontroll maximalizálása felemészti a legitimitást."}
        avg_t = sum(tensions.values()) / len(TENSION_KEYS)
        if avg_t > 0.55: return {"status": "WARNING", "type": "PRESSURE_ACCUMULATION", "desc": "A rendszernyomás emelkedik."}
        return {"status": "STABLE", "type": "NOMINAL", "desc": "A kognitív erőtér kiegyenlített."}
        
    def update(self, history, new_json, raw_entropy):
        if not new_json: return history
        tensions, anchors = new_json.get("tensions", {}), new_json.get("reality_anchors", [])
        
        if not history:
            state = {"tensions": {k: float(tensions.get(k, 0)) for k in TENSION_KEYS}, "deltas": {k: 0.0 for k in TENSION_KEYS}, "anchors": anchors, "entropy": raw_entropy}
        else:
            last = history[-1]
            state = {"tensions": {}, "deltas": {}, "anchors": last.get("anchors", []) + anchors, "entropy": raw_entropy}
            for k in TENSION_KEYS:
                old_val = last["tensions"].get(k, 0.0)
                new_val = max(float(tensions.get(k, 0)), old_val * self.decay_rate)
                state["tensions"][k] = round(new_val, 2), state["deltas"][k] = round(new_val - old_val, 2)
                
        state["topology"] = self.evaluate_collapse_topology(state["tensions"], state["deltas"], len(anchors))
        history.append(state)
        return history

# ==============================================================================
# IV. WRITING ENGINE (Translation to Final Output)
# ==============================================================================
class WritingEngine:
    @staticmethod
    def generate_prompt(density, gravity, rhythm, output_mode, current_state, pattern_data):
        return f"""
        COGNITO WRITING ENGINE. 
        Fizika: Sűrűség: {density} | Gravitáció: {gravity} | Mód: {output_mode} | Ritmus: {rhythm}
        Topológia: {current_state['topology']['type']}
        Írj magyar elemzést. Építsd be a diagnózist a logikádba. Ha CRITICAL, legyél kíméletlen.
        """

# ==============================================================================
# V. APP & UI RUNTIME (MUNKAMENET VÁLTOZÓK)
# ==============================================================================
if "state_history" not in st.session_state: st.session_state.state_history = []
if "chat_messages" not in st.session_state: st.session_state.chat_messages = []
if "last_audio" not in st.session_state: st.session_state.last_audio = None
# --- Új változók a taxiórához ---
if "total_in_tokens" not in st.session_state: st.session_state.total_in_tokens = 0
if "total_out_tokens" not in st.session_state: st.session_state.total_out_tokens = 0
if "total_usd" not in st.session_state: st.session_state.total_usd = 0.0

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM INIT v5.1")
    density = st.select_slider("Density", ["LOW", "MEDIUM", "HIGH"], value="HIGH")
    gravity = st.select_slider("Gravity", ["LIGHT", "CONTROLLED", "HEAVY"], value="HEAVY")
    rhythm = st.selectbox("Rhythm", ["FLAT", "PULSED", "FRACTURED", "CASCADING"])
    output_mode = st.selectbox("Output Mode", ["ANALYTIC NOIR", "STRATEGIC MEMO", "SYSTEMIC COLLAPSE"])
    
    st.divider()
    # Ide kerül a vizuális TAXIÓRA
    st.markdown("### 💸 SESSION RUNTIME COST")
    st.markdown(f"""
    <div class='cost-box'>
        TOTAL COST: <b>${st.session_state.total_usd:.4f}</b><br>
        <span style='font-size:10px; color:#aaa;'>IN: {st.session_state.total_in_tokens} tokens | OUT: {st.session_state.total_out_tokens} tokens</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ PURGE MEMORY & RESET COST"):
        st.session_state.state_history, st.session_state.chat_messages = [], []
        st.session_state.total_in_tokens = 0
        st.session_state.total_out_tokens = 0
        st.session_state.total_usd = 0.0
        st.rerun()
    st.markdown("<div class='copyright'>Concept & Design: Apáti Balázs / CSAPATI<br>Cognito Architecture v5.1</div>", unsafe_allow_html=True)

st.title("⬛ COGNITO POST-MONOLITH")
st.caption("v5.1 | Topological Runtime + Active Cost Monitoring")

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
        
        st.write("2. Memory Compiler: 7D Vektorok generálása...")
        new_json, comp_usage = compiler.compile_state(user_query, pattern_data)
        
        # TAXIÓRA FRISSÍTÉSE (Belső hívás)
        update_cost(comp_usage)
        
        st.write("3. State Machine: Topológiai Analízis...")
        st.session_state.state_history = state_machine.update(st.session_state.state_history, new_json, pattern_data['entropy'])
        status.update(label="✅ Állapot frissítve. Dekódolás...", state="complete", expanded=False)
    
    prompt = WritingEngine.generate_prompt(density, gravity, rhythm, output_mode, st.session_state.state_history[-1], pattern_data)
    
    with st.chat_message("assistant", avatar="⬛"):
        # Fő válasz generálása
        resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_query}])
        out = resp.choices[0].message.content
        
        # TAXIÓRA FRISSÍTÉSE (Kimeneti hívás)
        update_cost(resp.usage)
        
        st.markdown(out)
        st.session_state.chat_messages.append({"role": "assistant", "content": out})
        
    if is_initial: st.rerun()
    else: st.rerun() # Frissítjük a UI-t, hogy az oldalsávon a dollár érték azonnal megjelenjen
