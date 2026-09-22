# LifeLens AI

A local Python + Streamlit health-awareness and learning app.

## Features
- Health-awareness explanations
- Simple / Student / Detailed explanation levels
- English / Tamil output
- Medical-topic study packs
- MCQs and flashcards
- Educational urgency/warning-sign checker
- Local SQLite history
- Ollama local AI

## Setup

1. Install Python 3.10+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Ollama from the official Ollama website.
4. Download the model:

```bash
ollama pull llama3.2:3b
```

5. Start the app:

```bash
streamlit run app.py
```

## Safety
This is an educational prototype. It does not diagnose illness or prescribe treatment.
For serious or rapidly worsening symptoms, contact a qualified healthcare professional
or your local emergency service.
