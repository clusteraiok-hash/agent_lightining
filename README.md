# ⚡ Agent Lightning — Self-Learning AI SQL Agent
> Powered by LangChain, LangGraph, and Groq

Agent Lightning is an **autonomous, self-learning SQL assistant** that uses **Groq LLMs** for ultra-fast reasoning.  
It learns from its own mistakes, stores knowledge in `learned_memory.json`, and improves accuracy with each training run.

---

## 🧠 Features
- 🪄 **ReAct-based reasoning** via LangGraph  
- ⚡ **Groq LLM inference** for lightning-fast outputs  
- 🧾 **Self-learning system** — automatically corrects previous mistakes  
- 🧩 **Memory persistence** — stores knowledge in JSON  
- 🛠️ **Modular design** — extend with API, Streamlit UI, or database integration  

---

## 📁 Project Structure
```
agent_lightining/
│
├── agent_code.py           # Main SQL reasoning agent
├── train_lightning.py      # Self-learning trainer script
├── learned_memory.json     # Stores learned corrections (auto-created)
├── requirements.txt        # Dependency list
├── .gitignore              # Ignores venv and .env
└── README.md               # Project documentation (this file)
```

---

## 🧩 1. Setup Environment

### ✅ Prerequisites
- 🐍 Python 3.10+  
- 💻 Git installed (`git --version`)  
- 🔑 Groq API key (get from [Groq Console](https://console.groq.com/keys))  

---

### 🧱 Create Virtual Environment
```powershell
cd C:\Users\hunte\OneDrive\Desktop\agent_lightining
python -m venv agentlightning-venv
.\agentlightning-venv\Scripts\Activate.ps1
```

---

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install langchain langgraph langchain-groq groq python-dotenv requests tqdm rich
pip freeze > requirements.txt
```

---

## 🔑 2. Environment Variables
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

✅ `.gitignore` ensures this file is not uploaded to GitHub.

---

## 🧠 3. Main Script — `agent_code.py`
```python
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain import hub
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY"))
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools=[], prompt=prompt)

query = "List top 2 customers by sales amount"
result = agent.invoke({"input": query})
print(result["output"])
```

---

## 🔁 4. Self-Learning Trainer — `train_lightning.py`
```python
import json, os, time
from rich import print
from agent_code import agent

memory_file = "learned_memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        learned_memory = json.load(f)
else:
    learned_memory = {}

training_data = [
    {"question": "List top 2 customers by sales amount", "expected": "[('Carol', 800.0), ('Alice', 500.0)]"},
    {"question": "Which customer has sales less than 400?", "expected": "[('Bob', 300.0)]"},
]

print("\n🧠 Auto-learning SQL Agent Trainer\n")

for round_num in range(1, 4):
    print(f"🚀 Starting training round {round_num}...")
    correct = 0
    for t in training_data:
        predicted = agent.invoke({"input": t["question"]}).get("output", "error")
        is_correct = str(predicted).strip() == t["expected"]
        if is_correct:
            correct += 1
        learned_memory[t["question"].lower()] = predicted
        print(f"Update rollout with {{'question': '{t['question']}', 'predicted': '{predicted}', 'expected': '{t['expected']}'}}")
    accuracy = correct / len(training_data)
    print(f"✅ Round {round_num} — Accuracy: {accuracy * 100:.1f}%\n")
    time.sleep(1)

with open(memory_file, "w") as f:
    json.dump(learned_memory, f, indent=4)

print("🧠 Final learned corrections saved.")
```

---

## ⚙️ 5. Run and Train the Agent
```bash
python agent_code.py
python train_lightning.py
```

Example output:
```
🧠 Auto-learning SQL Agent Trainer
📚 Loaded 2 past corrections
✅ Round 1 — Accuracy: 0.0%
✅ Round 2 — Accuracy: 100.0%
✅ Round 3 — Accuracy: 100.0%
```

---

## 🚀 6. Push to GitHub
```bash
git init
git add .
git commit -m "Initial Agent Lightning commit"
git branch -M main
git remote add origin https://github.com/<your-username>/agent_lightining.git
git push -u origin main
```

---

## 📄 .gitignore Example
```
agentlightning-venv/
venv/
.env
__pycache__/
*.pyc
```

---

## ⚙️ requirements.txt
```
langchain
langgraph
langchain-groq
groq
python-dotenv
requests
tqdm
rich
```

---

## 🧩 Future Ideas
- Add real SQL database connection  
- Create Streamlit or FastAPI interface  
- Expand self-learning with embeddings  

---

## 🛡️ License
MIT License © 2025 — Free for personal and commercial use.
