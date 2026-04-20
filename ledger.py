"""
記帳模組 - 收支記錄
"""

import requests
import json
import os
from datetime import datetime

# 存檔位置
DATA_FILE = "ledger.json"

def load_data():
    """載入記錄"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"income": [], "expense": [], " balance": 0}

def save_data(data):
    """儲存記錄"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_income(amount, note=""):
    """記錄收入"""
    data = load_data()
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "amount": amount,
        "note": note
    }
    data["income"].append(record)
    data["balance"] += amount
    save_data(data)
    return f"💰 記錄收入：+{amount} 元\n備註：{note}\n餘額：{data['balance']} 元"

def add_expense(amount, category="", note=""):
    """記錄支出"""
    data = load_data()
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "amount": amount,
        "category": category,
        "note": note
    }
    data["expense"].append(record)
    data["balance"] -= amount
    save_data(data)
    return f"💸 記錄支出：-{amount} 元\n分類：{category}\n備註：{note}\n餘額：{data['balance']} 元"

def get_balance():
    """查看餘額"""
    data = load_data()
    income = sum(r["amount"] for r in data["income"])
    expense = sum(r["amount"] for r in data["expense"])
    
    return f"💵 目前餘額\n\n收入：+{income} 元\n支出：-{expense} 元\n────────\n餘額：{data['balance']} 元"

def get_records(limit=10):
    """查看記錄"""
    data = load_data()
    
    result = "📝 最近記錄\n\n"
    
    # 最近的收入
    for r in data["income"][-limit:]:
        result += f"💰 {r['date']} +{r['amount']} 元\n"
        if r.get("note"):
            result += f"   📝 {r['note']}\n"
    
    # 最近的支出
    for r in data["expense"][-limit:]:
        result += f"💸 {r['date']} -{r['amount']} 元"
        if r.get("category"):
            result += f" ({r['category']})"
        result += "\n"
        if r.get("note"):
            result += f"   📝 {r['note']}\n"
    
    if not data["income"] and not data["expense"]:
        result += "還沒有記錄～"
    
    return result

def clear_records():
    """清除所有記錄"""
    data = {"income": [], "expense": [], "balance": 0}
    save_data(data)
    return "🗑️ 已清除所有記錄"

def get_summary():
    """收支摘要"""
    data = load_data()
    
    # 按分類統計支出
    expense_by_cat = {}
    for r in data["expense"]:
        cat = r.get("category", "其他")
        expense_by_cat[cat] = expense_by_cat.get(cat, 0) + r["amount"]
    
    result = "📊 支出分類\n\n"
    for cat, amount in sorted(expense_by_cat.items(), key=lambda x: -x[1]):
        result += f"{cat}: {amount} 元\n"
    
    result += f"\n💵 總支出：{sum(r['amount'] for r in data['expense'])} 元"
    
    return result