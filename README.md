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
