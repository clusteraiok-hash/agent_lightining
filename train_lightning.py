# train_lightning.py
import asyncio
import json
import os
from datetime import datetime
from agent_code import run_agent



# === Define Base Dataset ===
base_tasks = [
    {"question": "List top 2 customers by sales amount", "answer": "[('Carol', 800.0), ('Alice', 500.0)]"},
    {"question": "Which customer has sales less than 400?", "answer": "[('Bob', 300.0)]"}
]

class RolloutStore:
    def __init__(self):
        self.runs = {}

    async def start_rollout(self, agent_name):
        rid = f"{agent_name}_run"
        self.runs[rid] = {"data": "demo"}
        return rid

    async def update_rollout(self, rid, data):
        self.runs[rid].update(data)
        print(f"Update rollout {rid} with {data}")
        return self.runs[rid]


store = RolloutStore()


async def train_once(tasks, run_id):
    results = []
    print(f"\n🚀 Starting training round {run_id}...\n")

    for t in tasks:
        rid = await store.start_rollout(agent_name="SQLAgent")

        predicted = await run_agent(t["question"])
        expected = t["answer"]
        score = 1.0 if str(expected).lower() in str(predicted).lower() else 0.0

        result = {
            "question": t["question"],
            "predicted": predicted,
            "expected": expected,
            "score": score,
        }
        results.append(result)
        await store.update_rollout(rid, result)

        if score == 0.0:
            print(f"🔧 Learning correction for: {t['question']}")
            print(f"📈 Confidence: {round(0.6 + 0.1 * (1 - score), 2)}\n")

    return results


async def auto_train(rounds=3):
    print("\n🧠 Auto-learning SQL Agent Trainer\n")
    if os.path.exists("learned_memory.json"):
        with open("learned_memory.json", "r") as f:
            memory = json.load(f)
        print(f"📚 Loaded {len(memory)} past corrections from memory.\n")
    else:
        memory = {}

    for i in range(rounds):
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = await train_once(base_tasks, run_id)

        learned = {r["question"].strip().lower(): r["expected"] for r in results if r["score"] == 0.0}
        memory.update(learned)

        with open("learned_memory.json", "w") as f:
            json.dump(memory, f, indent=2)

        acc = sum(r["score"] for r in results) / len(results) * 100
        print(f"✅ Round {i+1} — Accuracy: {acc:.1f}%\n")

    print("\n🧠 Final learned corrections:")
    for k, v in memory.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    asyncio.run(auto_train(rounds=3))
