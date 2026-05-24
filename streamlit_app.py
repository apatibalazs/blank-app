import streamlit as st
import time, json, math, re, logging
from collections import Counter
from openai import OpenAI
from help_module import show_help

# 1. Konfiguráció és Hibakeresés
logging.basicConfig(level=logging.INFO)
st.set_page_config(page_title="COGNITO ENGINE v3.5.1 × 9.4", layout="wide", initial_sidebar_state="expanded")

# 2. Költség Kalkuláció
PRICE_PER_1M_INPUT, PRICE_PER_1M_OUTPUT = 5.0, 15.0
def update_cost(usage_obj):
    if usage_obj:
        in_t, out_t = usage_obj.prompt_tokens, usage_obj.completion_tokens
        st.session_state.total_in_tokens += in_t
        st.session_state.total_out_tokens += out_t
        st.session_state.total_usd += (in_t / 1000000) * PRICE_PER_1M_INPUT + (out_t / 1000000) * PRICE_PER_1M_OUTPUT

# 3. Pattern Engine
class PatternEngine:
    def __init__(self):
        self.inversion_bridges = r'\b(de|azonban|mégis|viszont|ellenben|noha|ugyanakkor)\b'
    def scan(self, text):
        if not text: return {"entropy": 0, "patterns": [], "sentences": []}
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        patterns = [{"sentence_id": i+1, "text": s} for i, s in enumerate(sentences) if re.search(self.inversion_bridges, s.lower())]
        entropy = -sum(c/len(text) * math.log2(c/len(text)) for c in Counter(text).values() if c > 0)
        return {"entropy": round(entropy, 2), "patterns": patterns, "sentences": sentences}

# 4. Memory Compiler
class MemoryCompiler:
    def __init__(self, client): self.client = client
    def compile_state(self, user_input, pattern_data):
        json_schema = '{"tensions": {"POWER_VS_LEGITIMACY": 0.0, "ORDER_VS_ADAPTATION": 0.0, "CENTRALIZATION_VS_RESILIENCE": 0.0, "ABSTRACTION_VS_REALITY": 0.0, "EFFICIENCY_VS_STABILITY": 0.0, "IDENTITY_VS_INTEGRATION": 0.0, "TRANSPARENCY_VS_CONTROL": 0.0}, "reality_anchors": []}'
        prompt = f"COGNITO MEMORY COMPILER. 7D vektor JSON-t írj. Inverziók: {json.dumps(pattern_data['patterns'])}. SÉMA: {json_schema}"
        try:
            res = self.client.chat.completions.create(model="gpt-4o", response_format={"type": "json_object"}, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_input}], temperature=0.1)
            return json.loads(res.choices[0].message.content), res.usage
        except Exception as e:
            logging.error(f"MemoryCompiler error: {e}")
            return None, None

# 5. State Machine
class StateMachine:
    def __init__(self, decay_rate=0.8): self.decay_rate = decay_rate
    def update(self, history, new_json, raw_entropy):
        if not new_json: return history
        tensions = new_json.get("tensions", {})
        state = {"tensions": {}, "deltas": {}, "entropy": raw_entropy}
        for k in ["POWER_VS_LEGITIMACY", "ORDER_VS_ADAPTATION", "CENTRALIZATION_VS_RESILIENCE", "ABSTRACTION_VS_REALITY", "EFFICIENCY_VS_STABILITY", "IDENTITY_VS_INTEGRATION", "TRANSPARENCY_VS_CONTROL"]:
            old_val = history[-1]["tensions"].get(k, 0.0) if history else 0.0
            new_val = max(float(tensions.get(k, 0)), old_val * self.decay_rate)
            state["tensions"][k], state["deltas"][k] = round(new_val, 2), round(new_val - old_val, 2)
        history.append(state)
        return history

# 6. Writing Engine
class WritingEngine:
    def generate_prompt(self, state, mode, web, out_fmt, switches, pat):
        return f"COGNITO ENGINE 3.5.1 PRO. STATE: {state} | MODE: {mode}. RULE: Instability must be generated before decision."

# 7. Inicializálás
if "state_history" not in st.session_state: st.session_state.state_history = []
if "total_usd" not in st.session_state: st.session_state.total_usd = 0.0
if "total_in_tokens" not in st.session_state: st.session_state.total_in_tokens = 0
if "total_out_tokens" not in st.session_state: st.session_state.total_out_tokens = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pat_eng = PatternEngine()
comp = MemoryCompiler(client)
st_mach = StateMachine()
write_eng = WritingEngine()

# 8. Sidebar
with st.sidebar:
    st.markdown("### ⚙️ INIT MODULE 9.4")
    run_state = st.selectbox("STATE", ["FOG", "SPARK", "CUT", "PRESSURE", "COLLISION", "BREAK", "ALCHEMY"], index=5)
    show_help(run_state)
    audio_val = st.audio_input("🎤 HANG INPUT")
    if st.button("🗑️ PURGE MEMORY"): st.session_state.clear(), st.rerun()

# 9. Fő Futtatási Ciklus
if txt := st.chat_input("Új input a reaktornak..."):
    st.chat_message("user").markdown(txt)
    pat_data = pat_eng.scan(txt)
    new_json, comp_use = comp.compile_state(txt, pat_data)
    update_cost(comp_use)
    st.session_state.state_history = st_mach.update(st.session_state.state_history, new_json, pat_data['entropy'])
    prompt = write_eng.generate_prompt(run_state, "BALANCED", "AUTO", "FULL TEXT", {}, pat_data)
    
    with st.chat_message("assistant"):
        try:
            resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": txt}])
            st.markdown(resp.choices[0].message.content)
        except Exception as e:
            st.error(f"REACTOR FAILURE: {e}")
