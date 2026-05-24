import streamlit as st
import time, json, math, re, logging
from collections import Counter
from openai import OpenAI
from help_module import show_help

logging.basicConfig(level=logging.INFO)
st.set_page_config(page_title="COGNITO ENGINE v3.5.1 × 9.4", layout="wide", initial_sidebar_state="expanded")

PRICE_PER_1M_INPUT, PRICE_PER_1M_OUTPUT = 5.0, 15.0

def update_cost(usage_obj):
    if usage_obj:
        in_t, out_t = usage_obj.prompt_tokens, usage_obj.completion_tokens
        st.session_state.total_in_tokens += in_t
        st.session_state.total_out_tokens += out_t
        st.session_state.total_usd += (in_t / 1000000) * PRICE_PER_1M_INPUT + (out_t / 1000000) * PRICE_PER_1M_OUTPUT

class PatternEngine:
    def __init__(self):
        self.pos_markers = ["stabil", "biztonság", "siker", "hatékony", "nyereség", "növekedés", "fejlődés"]
        self.neg_markers = ["összeomlás", "válság", "veszteség", "instabil", "hiba", "kockázat", "káosz"]
        self.inversion_bridges = r'\b(de|azonban|mégis|viszont|ellenben|noha|ugyanakkor)\b'
    def scan(self, text):
        if not text: return {"entropy": 0, "patterns": [], "sentences": []}
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        patterns, total = [], len(text)
        entropy = -sum(c/total * math.log2(c/total) for c in Counter(text).values())
        for i, s in enumerate(sentences):
            if re.search(self.inversion_bridges, s.lower()):
                parts = re.split(self.inversion_bridges, s.lower())
                if len(parts) >= 3:
                    patterns.append({"sentence_id": i+1, "text": s, "diagnostic": "STRUCTURAL_INVERSION"})
        return {"entropy": round(entropy, 2), "patterns": patterns, "sentences": sentences}

class MemoryCompiler:
    def __init__(self, client): self.client = client
    def compile_state(self, user_input, pattern_data):
        prompt = f"COGNITO MEMORY COMPILER. 7D vektor JSON-t írj. Inverziók: {json.dumps(pattern_data['patterns'])}. SÉMA: {{\"tensions\": {{\"TENGELY_NEVE\": float(0-1)}}, \"reality_anchors\": [{\"entity\": \"string\", \"fact\": \"string\"}]}}"
        try:
            res = self.client.chat.completions.create(model="gpt-4o", response_format={"type": "json_object"}, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_input}], temperature=0.1)
            return json.loads(res.choices[0].message.content), res.usage
        except Exception as e:
            logging.error(f"MemoryCompiler error: {e}")
            return None, None

class StateMachine:
    def __init__(self, decay_rate=0.8): self.decay_rate = decay_rate
    def evaluate_collapse_topology(self, tensions, anchors_count):
        if tensions.get("ABSTRACTION_VS_REALITY", 0) > 0.75 and anchors_count == 0: return {"status": "CRITICAL", "type": "NARRATIVE_DISCONNECT", "desc": "Nincs kapcsolat a valósággal."}
        if tensions.get("ORDER_VS_ADAPTATION", 0) > 0.7 and tensions.get("EFFICIENCY_VS_STABILITY", 0) > 0.7: return {"status": "CRITICAL", "type": "RIGIDITY_DEATH_SPIRAL", "desc": "Merevedési halálspirál."}
        if tensions.get("POWER_VS_LEGITIMACY", 0) > 0.7 and tensions.get("TRANSPARENCY_VS_CONTROL", 0) > 0.7: return {"status": "CRITICAL", "type": "LEGITIMACY_CRISIS", "desc": "Kontroll maximalizálása felemészti a legitimitást."}
        if sum(tensions.values()) / 7 > 0.55: return {"status": "WARNING", "type": "PRESSURE_ACCUMULATION", "desc": "A rendszernyomás emelkedik."}
        return {"status": "STABLE", "type": "NOMINAL", "desc": "A kognitív erőtér kiegyenlített."}
    def update(self, history, new_json, raw_entropy):
        if not new_json: return history
        tensions, anchors = new_json.get("tensions", {}), new_json.get("reality_anchors", [])
        state = {"tensions": {}, "deltas": {}, "anchors": (history[-1].get("anchors", []) + anchors if history else anchors), "entropy": raw_entropy}
        for k in ["POWER_VS_LEGITIMACY", "ORDER_VS_ADAPTATION", "CENTRALIZATION_VS_RESILIENCE", "ABSTRACTION_VS_REALITY", "EFFICIENCY_VS_STABILITY", "IDENTITY_VS_INTEGRATION", "TRANSPARENCY_VS_CONTROL"]:
            old_val = history[-1]["tensions"].get(k, 0.0) if history else 0.0
            new_val = max(float(tensions.get(k, 0)), old_val * self.decay_rate)
            state["tensions"][k], state["deltas"][k] = round(new_val, 2), round(new_val - old_val, 2)
        state["topology"] = self.evaluate_collapse_topology(state["tensions"], len(anchors))
        history.append(state)
        return history

class WritingEngine:
    @staticmethod
    def generate_prompt(state, mode, web, out_fmt, switches, cur_state, pat):
        sw_txt = "\n".join([f"{k}={v}" for k, v in switches.items()])
        return f"""COGNITO ENGINE 3.5.1 PRO × 9.4 — OMNI RUNTIME SYSTEM
STATE: {state} | MODE: {mode} | WEB: {web} | OUTPUT FORMAT: {out_fmt}
SWITCHES: {sw_txt}
CORE LAW: A system that fully explains itself has already lost its precision.
PRIMARY OBJECTIVE: Decision under constraint where the world does not re-stabilize after choice.
SYSTEM RULE: Instability must be generated before decision. Decision must destroy alternatives.
MODULE CONSTRAINTS: 
- FRACTURE: Break all user assumptions immediately. 
- INTERFERENCE: Inject noise to test decision resilience. 
- CONCEPT REACTOR: Force fusion of disparate domains.
- VALIDATION: Every output must carry a truth-value tag.
OUTPUT CONTRACT: [RUN STATUS], [FRAME], [PARADOX], [DECISION], [LOSS], [WRITING OUTPUT], [RESIDUAL TENSION]."""

for key in ["state_history", "chat_messages", "last_audio", "total_in_tokens", "total_out_tokens", "total_usd"]:
    if key not in st.session_state: st.session_state[key] = [] if "messages" in key or "history" in key else 0

with st.sidebar:
    st.markdown("### ⚙️ INIT MODULE 9.4")
    col1, col2 = st.columns([4, 1])
    with col1:
        run_state = st.selectbox("STATE", ["FOG", "SPARK", "CUT", "PRESSURE", "COLLISION", "BREAK", "ALCHEMY"], index=5)
    with col2:
        st.write("###") 
        show_help(run_state)
    run_mode = st.selectbox("MODE", ["QUICK", "BALANCED", "DEEP", "CREATIVE", "SCIENTIFIC"], index=2)
    web_mode = st.radio("WEB", ["OFF", "AUTO", "ON"], index=1)
    out_format = st.radio("OUTPUT FORMAT", ["POLITICAL PAMPHLET", "STRATEGIC MEMO", "PRODUCT DESCRIPTION", "FULL TEXT"], index=3)
    switches = {k: st.toggle(k, value=True) for k in ["ENGINE_MODE", "OPEN_SYSTEM", "DECISION_MODE", "VALIDATION_MODE", "ANTI_CLOSURE", "LOSS_TRACKING"]}
    st.divider()
    st.markdown(f"TOTAL: ${st.session_state.total_usd:.4f} | IN: {st.session_state.total_in_tokens} | OUT: {st.session_state.total_out_tokens}")
    if st.button("🗑️ PURGE MEMORY"): st.session_state.clear(), st.rerun()

if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    pat_eng, comp, st_mach = PatternEngine(), MemoryCompiler(client), StateMachine()
    if st.session_state.state_history:
        cur = st.session_state.state_history[-1]
        with st.expander("VECTOR FIELD (7D GRAVITY)", expanded=True):
            cols = st.columns(3)
            for i, (k, v) in enumerate(cur['tensions'].items()):
                cols[i%3].metric(k, v, delta=f"{cur['deltas'][k]:+.2f}")
    if txt := st.chat_input("Új input a reaktornak..."):
        st.session_state.chat_messages.append({"role": "user", "content": txt})
        with st.chat_message("user"): st.markdown(txt)
        pat_data = pat_eng.scan(txt)
        new_json, comp_use = comp.compile_state(txt, pat_data)
        update_cost(comp_use)
        st.session_state.state_history = st_mach.update(st.session_state.state_history, new_json, pat_data['entropy'])
        prompt = WritingEngine.generate_prompt(run_state, run_mode, web_mode, out_format, switches, st.session_state.state_history[-1], pat_data)
        with st.chat_message("assistant"):
            try:
                resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": txt}])
                out = resp.choices[0].message.content
                st.markdown(out)
                st.session_state.chat_messages.append({"role": "assistant", "content": out})
            except Exception as e:
                st.error(f"REACTOR FAILURE: {e}")
            st.rerun()
                                                
