# main.py
import json
import os
import re
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema.messages import AIMessage

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

# ------------------------------
# 1. Load Mock Flight Data
# ------------------------------
with open("data/flights.json") as f:
    flights = json.load(f)

# ------------------------------
# 2. Load and Vectorize Visa Policy Docs (RAG)
# ------------------------------
loader = TextLoader("data/visa_rules.md")
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(split_docs, embeddings)
retriever = db.as_retriever()

# ------------------------------
# 3. Initialize Chat Model
# ------------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------------
# 4. Policy QA Chain (RAG)
# ------------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)

# ------------------------------
# 5. LLM-Powered Flight Criteria Extractor
# ------------------------------
extract_prompt = PromptTemplate.from_template("""
Extract the following fields from the flight search request if available:
- from
- to
- departure_date (YYYY-MM-DD or just month/year if exact date not given)
- return_date (optional)
- alliance (e.g., Star Alliance, SkyTeam, OneWorld)
- avoid_overnight (true/false)
- max_price (USD)

Return the result as a JSON object with keys: from, to, departure_date, return_date, alliance, avoid_overnight, max_price.

Input: {query}
""")


def extract_criteria(query) -> dict:
    chain = extract_prompt | llm
    output = chain.invoke({"query": query})

    # Extract string from AIMessage if needed
    if isinstance(output, AIMessage):
        output = output.content
    elif hasattr(output, "content"):
        output = output.content
    try:
        # Remove code block fences like ```json\n...\n```
        cleaned = re.sub(r"^```(?:json)?\n|\n```$", "", output.strip(), flags=re.IGNORECASE)
        parsed = json.loads(cleaned)
        return parsed
    except Exception as e:
        print("❌ Failed to parse criteria:", e)
        return {}


# ------------------------------
# 6. Flight Search Logic
# ------------------------------
def search_flights(query: str) -> str:
    filters = extract_criteria(query)
    results = []
    for f in flights:
        if filters.get("from") and filters["from"].lower() not in f["from"].lower():
            continue
        if filters.get("to") and filters["to"].lower() not in f["to"].lower():
            continue
        if filters.get("departure_date") and not f["departure_date"].startswith(filters["departure_date"][:7]):
            continue
        if filters.get("alliance") and filters["alliance"].lower() != f["alliance"].lower():
            continue
        if filters.get("avoid_overnight") and any("overnight" in l.lower() for l in f.get("layovers", [])):
            continue
        if filters.get("max_price") and f["price_usd"] > float(filters["max_price"]):
            continue
        results.append(f)

    if not results:
        return "No matching flights found."

    return "\n".join([
        f"{r['airline']} | {r['from']} → {r['to']} | {r['departure_date']} | ${r['price_usd']}"
        for r in results
    ])

# ------------------------------
# 7. LangChain Tools
# ------------------------------
tools = [
    Tool(
        name="FlightSearch",
        func=search_flights,
        description="Use this to search for flights using natural queries that include destination, date, airlines, budget, etc."
    ),
    Tool(
        name="PolicyQA",
        func=qa_chain.run,
        description="Use this to answer questions about travel visa or refund policies."
    )
]

# ------------------------------
# 8. Agent Setup
# ------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True
)

# ------------------------------
# 9. Main Loop
# ------------------------------
if __name__ == "__main__":
    print("✈️ Travel Assistant Ready. Type 'exit' to quit.")
    while True:
        q = input("\nYou: ")
        if q.strip().lower() == "exit":
            break
        response = agent.run(q)
        print("Bot:", response)
