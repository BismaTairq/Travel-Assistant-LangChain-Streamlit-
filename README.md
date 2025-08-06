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

### Prompt Strategies & Agent Logic

## Prompt Strategy

* Flight queries are passed through an LLM prompt chain to extract structured search criteria like origin, destination, dates, alliance, refundable, layovers, and max price.

* Policy queries are passed directly to the RetrievalQA chain powered by FAISS + HuggingFace embeddings on visa_rules.md.

Tool-Based Agent Logic

* The system uses a LangChain conversational-react-description agent.

* Agent receives natural language input and routes it to the appropriate tool:

    * FlightSearch: Parses and filters flights from flights.json.

    * PolicyQA: Runs vector search + LLM completion over embedded policy text.

* ConversationBufferMemory is used to maintain context in chat.


## Sample Chat Prompts

* "Show me all round trips to Tokyo with Star Alliance in August."
  <img width="726" height="422" alt="image" src="https://github.com/user-attachments/assets/107fb7a2-ada5-46c6-91de-7b1a2417080c" />

* "Find me a flight from Dubai to Tokyo with Turkish Airlines."
  <img width="690" height="513" alt="image" src="https://github.com/user-attachments/assets/636deaa4-9e94-41a3-9c8b-65dada41be33" />

* "Are there any refundable flights from Los Angeles to Tokyo in September?"
  <img width="704" height="428" alt="image" src="https://github.com/user-attachments/assets/5b1b5646-d71e-4664-bee1-cca887cc679a" />

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
