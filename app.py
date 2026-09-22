import streamlit as st
import sqlite3
from datetime import datetime
import os

try:
    import ollama
except ImportError:
    ollama = None

DB = "lifelens.db"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        category TEXT,
        user_text TEXT,
        response TEXT
    )""")
    con.commit()
    con.close()

def save_history(category, user_text, response):
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO history(created_at, category, user_text, response) VALUES(?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), category, user_text, response)
    )
    con.commit()
    con.close()

def ask_local_ai(prompt, model="llama3.2:3b"):
    if ollama is None:
        return "Ollama Python package is not installed. Run: pip install ollama"
    try:
        result = ollama.chat(model=model, messages=[
            {"role": "system", "content":
             "You are an educational health-awareness assistant. "
             "Do not diagnose or prescribe. Give general educational information. "
             "If symptoms could be urgent, clearly advise contacting a qualified "
             "medical professional or local emergency service. Keep answers simple."},
            {"role": "user", "content": prompt}
        ])
        return result["message"]["content"]
    except Exception as e:
        return f"Could not connect to the local AI model. Make sure Ollama is running and the model is installed.\n\nError: {e}"

def explain_level(level):
    return {
        "Simple": "Explain in very simple language with a short example.",
        "Student": "Explain at college-student level using headings and key points.",
        "Detailed": "Give a detailed educational explanation with definitions, causes, prevention and when professional help may be needed."
    }[level]

init_db()

st.set_page_config(page_title="LifeLens AI", page_icon="🔎", layout="wide")

st.title("🔎 LifeLens AI")
st.caption("Local AI • Health Awareness • Learning • Voice-ready explanations")

with st.sidebar:
    st.header("⚙️ Settings")
    level = st.selectbox("Explanation level", ["Simple", "Student", "Detailed"])
    language = st.selectbox("Language", ["English", "Tamil"])
    model = st.text_input("Ollama model", "llama3.2:3b")
    st.divider()
    st.info("LifeLens AI provides educational information, not a medical diagnosis.")

tabs = st.tabs(["🩺 Health Awareness", "📚 Learn", "🚨 Urgency Check", "🕘 History"])

with tabs[0]:
    st.subheader("Describe what you want to understand")
    text = st.text_area(
        "Symptoms or health topic",
        placeholder="Example: What is dehydration and what are common warning signs?",
        height=140
    )
    if st.button("🔎 Explain", type="primary", key="health"):
        if text.strip():
            prompt = f"""
{explain_level(level)}
Answer in {language}.
Topic/user description: {text}
Start with a brief educational explanation. Do not diagnose.
"""
            with st.spinner("Thinking locally..."):
                answer = ask_local_ai(prompt, model)
            st.markdown(answer)
            save_history("Health Awareness", text, answer)

with tabs[1]:
    st.subheader("Turn any medical topic into study material")
    topic = st.text_input("Topic", placeholder="Example: Diabetes")
    if st.button("📖 Create Study Pack", key="learn"):
        if topic.strip():
            prompt = f"""
Create a student-friendly study pack about "{topic}" in {language}.
{explain_level(level)}
Include:
1. Simple definition
2. 5 key points
3. Common misconceptions
4. 5 short MCQs with answers
5. 3 flashcards
Keep it educational and avoid diagnosis or treatment instructions.
"""
            with st.spinner("Creating your study pack..."):
                answer = ask_local_ai(prompt, model)
            st.markdown(answer)
            save_history("Study Pack", topic, answer)

with tabs[2]:
    st.subheader("🚨 Urgency Check")
    st.warning("This is only an educational safety check. It cannot determine whether you have an emergency.")
    symptoms = st.text_area(
        "Describe the situation",
        placeholder="Example: I suddenly have severe chest pain and difficulty breathing.",
        height=120,
        key="urgency"
    )
    if st.button("Check for warning signs", key="urgent"):
        if symptoms.strip():
            prompt = f"""
Review this description only for general emergency warning-sign education:
{symptoms}

Do not diagnose. If the description contains signs that can be associated with
a medical emergency, clearly say that urgent professional medical assessment
may be needed and advise contacting local emergency services or a qualified
health professional. Otherwise provide general safety information.
Answer in {language}.
"""
            with st.spinner("Checking educational warning signs..."):
                answer = ask_local_ai(prompt, model)
            st.markdown(answer)
            save_history("Urgency Check", symptoms, answer)

with tabs[3]:
    st.subheader("🕘 Your local learning history")
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT created_at, category, user_text FROM history ORDER BY id DESC LIMIT 20"
    ).fetchall()
    con.close()
    if rows:
        for created, category, question in rows:
            with st.expander(f"{created} • {category}"):
                st.write(question)
    else:
        st.info("No history yet.")

st.divider()
st.caption("LifeLens AI • Python + Streamlit + Ollama + SQLite")
