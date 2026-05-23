COGNITO ARCHITECTURE v3.1 — AI INTEGRATED RUNTIME + CHAT UI
# Concept & Design: Apáti Balázs / CSAPATI
# ==============================================================================

import streamlit as st
import time
import math
from collections import Counter
from openai import OpenAI

# ==============================================================================
# PAGE CONFIG & CSS
# ==============================================================================
st.set_page_config(page_title="COGNITO ARCHITECTURE v3.1", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050505; color: #e5e5e5; }
.stApp { background: radial-gradient(circle at top left, rgba(0,255,180,0.08), transparent 25%), radial-gradient(circle at bottom right, rgba(255,0,120,0.08), transparent 25%), linear-gradient(180deg, #040404 0%, #090909 100%); }
h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; }
.terminal-box { background: rgba(0,0,0,0.6); border: 1px solid rgba(0,255,180,0.2); border-radius: 12px; padding: 18px; box-shadow: 0 0 25px rgba(0,255,180,0.08), inset 0 0 12px rgba(255,255,255,0.03); }
.metric-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; text-align: center; backdrop-filter: blur(8px); }
.stButton > button { width: 100%; background: linear-gradient(90deg, #00ffb4, #00bfff); color: black; font-weight: bold; border: none; border-radius: 12px; padding: 14px; transition: 0.3s; box-shadow: 0 0 25px rgba(0,255,180,0.3); }
.stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 40px rgba(0,255,180,0.5); }
section[data-testid="stSidebar"] { background: rgba(10,10,10,0.95); border-right: 1px solid rgba(255,255,255,0.05); }
.stTabs [role="tab"] { background: rgba(255,255,255,0.03); border-radius: 10px; margin-right: 5px; }
/* AI Chat Bubble formázás */
.stChatMessage { background-color: rgba(20, 20, 20, 0.8) !important; border: 1px solid rgba(0,255,180,0.3) !important; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# LOCAL METRICS CALCULATOR
# ==============================================================================
def calculate_metrics(text):
    if not text: return 0, 0
    pos_markers = ["stabil", "biztonságos", "siker", "hatékony", "nyereség", "támogatás", "növekedés"]
    neg_markers = ["összeomlás", "válság", "veszteség", "instabil", "hiba", "kockázat", "ellentmondás", "korrupció"]
    contrast_words = ["de", "azonban", "mégis", "viszont", "ellenben", "noha"]
    
    score = 0
    s_lower = text.lower()
    if any(w in s_lower for w in pos_markers) and any(w in s_lower for w in neg_markers): score += 15
    score += sum(3 for w in contrast_words if w in s_lower)
    score += sum(2 for w in neg_markers if w in s_lower)
    
    chars = Counter(text)
    total = len(text)
    entropy = -sum(count/total * math.log2(count/total) for count in chars.values())
    
    return min(score, 100), round(entropy, 2)

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM INIT")
    st.caption("COGNITO RUNTIME v3.1 [AI ACTIVE]")
    st.divider()
    dark_mode = st.toggle("💀 DARK MODE")
    research_mode = st.toggle("🌐 WEB AUDIT")
    st.success("API CONNECTION SECURED")

# ==============================================================================
# MAIN UI
# ==============================================================================
st.title("⬛ COGNITO POST-MONOLITH")
st.caption("Execution Runtime v3.1 | LIVE CHAT UI INTEGRATION")

st.markdown("""
<div class="terminal-box">
A rendszer felkészült. Add meg a vizsgálandó szöveget, a fizikai paramétereket, és a COGNITO motor generál egy átfogó, formázott kognitív jelentést.
</div>
""", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1.6, 1])
with col1:
    st.subheader("I. TOPIC INPUT")
    topic_input = st.text_area("Vizsgálandó szöveg", height=250, placeholder="Másold be a hírt vagy szöveget ide...")
    input_type = st.selectbox("Input Típusa", ["NEWS", "ARTICLE", "POLITICAL SYSTEM", "CONFLICT"])

with col2:
    st.subheader("II. WRITING PHYSICS")
    density = st.select_slider("Density", ["LOW", "MEDIUM", "HIGH"], value="HIGH")
    gravity = st.select_slider("Gravity", ["LIGHT", "CONTROLLED", "HEAVY"], value="HEAVY")
    rhythm = st.selectbox("Rhythm", ["FLAT", "PULSED", "FRACTURED", "CASCADING"])
    output_mode = st.selectbox("Output Mode", ["ANALYTIC NOIR", "STRATEGIC MEMO", "SYSTEMIC COLLAPSE", "INTERNAL ANALYSIS"])

st.divider()
run = st.button("⚡ EXECUTE LIVE AI RUNTIME", use_container_width=True)

# ==============================================================================
# EXECUTION (API CALL)
# ==============================================================================
if run and topic_input:
    
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("🚨 HIBA: Nincs beállítva az OPENAI_API_KEY a Streamlit Secrets-ben!")
        st.stop()
        
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    score, entropy = calculate_metrics(topic_input)

    st.info("🧠 Csatlakozás a kognitív hálózathoz... Mélyelemzés generálása folyamatban...")
    
    try:
        system_prompt = f"""
        Te a COGNITO SYSTEM vagy, egy professzionális, poszt-monolit kognitív elemző motor. 
        Működési szabályaid:
        1. STRUCTURE OVER NARRATIVE: A tényleges struktúrát vizsgálod, nem a felszínt.
        2. CONTRADICTION MUST SURVIVE: Nem oldod fel a paradoxonokat, hanem rájuk mutatsz.
        3. PRESSURE REVEALS STRUCTURE: A rejtett veszteségeket keresed.
        
        Írási fizika paraméterek:
        - Mondatsűrűség (Density): {density}
        - Gravitáció (Súlyosság): {gravity}
        - Ritmus (Rhythm): {rhythm}
        - Kimeneti formátum: {output_mode}
        
        Mért nyomás (Tension Score): {score}, Entrópia: {entropy}.
        
        FELADAT: 
        Készíts egy átfogó, MÉLYSÉGI ELEMZÉST (kb. 300-400 szó)! 
        KÖTELEZŐ formázás: Használj tagolt bekezdéseket, Markdown vastagítást a kulcsszavaknál, és felsorolásokat (bullet points), hogy vizuálisan is olvasható legyen a jelentés. 
        TILOS egyetlen egybefüggő szövegtömbben írnod. Reflektálj a fizikai paraméterekre a stílusoddal!
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Elemezd ezt az {input_type} típusú szöveget:\n\n{topic_input}"}
            ],
            temperature=0.7
        )
        
        ai_output = response.choices[0].message.content
        
        st.success("✅ AI ELEMZÉS SIKERESEN LEFUTOTT")
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("TENSION SCORE", score)
        c2.metric("ENTROPY", entropy)
        c3.metric("AI ENGINE", "ONLINE (GPT-4o)")
        st.divider()

        st.subheader("🧠 LIVE COGNITO AI REPORT")
        
        # ITT VAN A VARÁZSLAT: Chat Message vizualizáció, szép sortörésekkel!
        with st.chat_message("assistant", avatar="⬛"):
            st.markdown(ai_output)
            
        st.divider()
        st.download_button("💾 DOWNLOAD AI REPORT", data=ai_output, file_name="cognito_ai_report.txt", mime="text/plain")

    except Exception as e:
        st.error(f"❌ Rendszerhiba az API kommunikáció során: {e}")

elif run:
    st.error("❌ Nincs input.")
    
