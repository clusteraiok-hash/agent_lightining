import json
import os
from datetime import datetime

METRICS_FILE = "metrics.json"


def load_metrics():
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r") as f:
            return json.load(f)
    return []


def save_metrics(data):
    with open(METRICS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_run(agent_name, results):
    metrics = load_metrics()
    correct = sum(1 for r in results if r["score"] >= 1.0)
    total = len(results)
    accuracy = (correct / total) * 100 if total > 0 else 0

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics.append({
        "run_id": run_id,
        "agent": agent_name,
        "accuracy": accuracy,
        "results": results
    })
    save_metrics(metrics)

    # Print summary
    print(f"✅ Saved run {run_id} — Accuracy: {accuracy:.1f}%    \n")

    print("📊 Accuracy Trend (recent runs):")
    for i, m in enumerate(metrics[-5:], start=1):
        bar = "█" * int(m["accuracy"] / 10)
        print(f"{i:02d}. {m['run_id']} | {bar:<20} | {m['accuracy']:.1f}%")

    # Compare trend
    if len(metrics) >= 2:
        diff = metrics[-1]["accuracy"] - metrics[-2]["accuracy"]
        if diff > 0:
            print(f"\n🟢 Improvement: +{diff:.1f}% since last run.")
        elif diff < 0:
            print(f"\n🔴 Decline: {diff:.1f}% since last run.")
        else:
            print("\n⚪ No change since last run.")
