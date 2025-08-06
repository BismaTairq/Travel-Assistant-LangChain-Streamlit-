# Travel Assistant (LangChain + Streamlit)

Welcome to the **AI-Powered Travel Assistant** — your intelligent companion for planning smarter, faster, and visa-compliant journeys.
**Chat naturally.** Ask about flights, travel rules, or visa policies.
**Powered by:** LangChain · OpenAI · FAISS · Streamlit
---
## Features at a Glance
**Smart Flight Search**
Use natural language like *"Find me a flight to Tokyo in August"* and get instant filtered options.

**Visa & Refund Policy Answers (RAG)**
Ask things like *"Can I cancel my ticket?"*

**LLM Tool Routing via LangChain Agent**
Automatically picks the right tool to handle your query: flight or policy.

**Streamlit Web UI**
Simple, clean chat interface. Just type and go.
---

## Project Structure

```
travel-assistant/
├── main.py               # Backend: LangChain agent, flight + policy logic
├── app.py                # Frontend: Streamlit chatbot UI
├── .env                  # Your OpenAI API key
├── data/
│   ├── flights.json      # Mock flight listings
│   └── visa_rules.md     # Visa/refund markdown policies
```

---

## Setup Instructions

### 1. Create environment & install packages

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your OpenAI API key
```
# .env file
OPENAI_API_KEY=sk-...
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

---

## Sample Chat Prompts

### Flights:

* "Show me all round trips to Tokyo with Star Alliance in August."
* "Find me a flight from Dubai to Tokyo with Turkish Airlines."
* "Are there any refundable flights from Lahore to Berlin in September?"

### Visa & Refund:

* "Do I need a visa for Spain as a Pakistani citizen?"
* "Can UAE citizens visit Japan without a visa?"
* "How long does it take to process a flight refund?"
---

## Requirements

```
openai
langchain
faiss-cpu
sentence-transformers
streamlit
python-dotenv
```

---

## License

MIT License. Use it, build on it, and fly smarter.
