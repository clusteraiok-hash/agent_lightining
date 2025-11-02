# agent_code.py
import os
import json
import sqlite3
from dotenv import load_dotenv

# --- Try import from LangChain (new API) ---
try:
    from langchain.agents import create_agent
    USE_NEW = True
    print("✅ Using create_agent (LangChain modern API)")
except ImportError:
    from langgraph.prebuilt import create_react_agent
    USE_NEW = False
    print("⚠️ Using create_react_agent (deprecated API)")

# --- LangChain + Groq ---
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# --- Memory setup ---
LEARNED_MEMORY_PATH = "learned_memory.json"


def apply_learned_corrections(question: str):
    """Return a learned correction for `question` if available."""
    qkey = question.strip().lower()
    if not os.path.exists(LEARNED_MEMORY_PATH):
        return None
    try:
        with open(LEARNED_MEMORY_PATH, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except Exception as e:
        print(f"⚠️ Could not read learned memory: {e}")
        return None
    return str(memory.get(qkey)) if qkey in memory else None


# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


# --- SQLite DB setup ---
def init_db(db_path=":memory:"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            customer TEXT,
            amount REAL
        );
    """)
    cur.execute("DELETE FROM sales")
    cur.executemany("INSERT INTO sales VALUES (?, ?)", [
        ('Alice', 500.0),
        ('Bob', 300.0),
        ('Carol', 800.0),
    ])
    conn.commit()
    return conn


def execute_sql(sql, conn):
    """Execute a given SQL query and return results."""
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        return f"ERROR: {e}"


# --- Build Agent ---
def build_agent(conn):
    model = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key, temperature=0)

    def run_query(question: str) -> str:
        """
        Execute a SQL query on the in-memory sales database.
        Example: 'List top 2 customers by sales amount'
        """
        sql = "SELECT customer, amount FROM sales ORDER BY amount DESC LIMIT 2;"
        results = execute_sql(sql, conn)
        return str(results)

    if USE_NEW:
        # 🧠 New LangChain API (no prompt argument)
        agent = create_agent(
            model=model,
            tools=[run_query],
        )
    else:
        # ⚠️ Old LangGraph API (deprecated)
        agent = create_react_agent(
            model=model,
            tools=[run_query],
            prompt="You are a helpful SQL assistant. Use run_query to answer SQL questions."
        )

    return agent


# --- Async agent runner ---
async def run_agent(question: str):
    corrected = apply_learned_corrections(question)
    if corrected:
        return corrected

    conn = init_db()
    agent = build_agent(conn)

    try:
        response = await agent.ainvoke({"messages": [HumanMessage(content=question)]})
        messages = response.get("messages", [])
        if messages and hasattr(messages[-1], "content"):
            return messages[-1].content
        return str(response)
    except Exception as e:
        print(f"⚠️ Agent error: {e}")
        return "error"


# --- Main entry point ---
def main():
    conn = init_db()
    agent = build_agent(conn)
    question = "Who are the top 2 customers by sales amount?"
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print("Agent response:", response)


if __name__ == "__main__":
    main()
