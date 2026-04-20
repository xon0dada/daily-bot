"""
Daily Bot - 記帳模組
"""

import json
import os
from datetime import datetime

DATA_FILE = "ledger.json"

CATEGORIES = ["🍔 餐飲", "🚗 交通", "🛒 購物", "🎬 娛樂", "🏥 醫療", "🏠 房租", "💰 投資", "📱 電話", "💡 電費", "💻 3C", "👕 服飾", "✈️ 旅遊", "📚 學習", "🐱 寵物", "📦 其他"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"income": [], "expense": [], "balance": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_income(amount, note=""):
    data = load_data()
    record = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "amount": amount, "note": note}
    data["income"].append(record)
    data["balance"] += amount
    save_data(data)
    return f"💰 收入 +{amount} 元\n餘額: {data['balance']} 元"

def add_expense(amount, category="📦 其他", note="-"):
    data = load_data()
    record = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "amount": amount, "category": category, "note": note}
    data["expense"].append(record)
    data["balance"] -= amount
    save_data(data)
    return f"💸 支出 -{amount} 元 ({category})\n餘額: {data['balance']} 元"

def get_balance():
    data = load_data()
    income = sum(r["amount"] for r in data["income"])
    expense = sum(r["amount"] for r in data["expense"])
    return f"💵 餘額\n\n收入: +{income} 元\n支出: -{expense} 元\n─────────\n餘額: {data['balance']} 元"

def get_records(limit=10):
    data = load_data()
    all_records = []
    for r in data["income"]:
        all_records.append({"type": "💰", "date": r["date"][-5:], "amount": r["amount"], "note": r.get("note", "")})
    for r in data["expense"]:
        all_records.append({"type": "💸", "date": r["date"][-5:], "amount": r["amount"], "category": r.get("category", "")})
    all_records.sort(key=lambda x: x["date"], reverse=True)
    result = "📝 記錄\n\n"
    for r in all_records[:limit]:
        result += f"{r['type']} {r['date']} {r['amount']} 元"
        if r.get("category"):
            result += f" {r['category']}"
        result += "\n"
    return result if all_records else "還沒記錄～"

def get_categories():
    return "📂 分類\n\n" + "\n".join(CATEGORIES)

def clear_records():
    save_data({"income": [], "expense": [], "balance": 0})
    return "🗑️ 已清除"