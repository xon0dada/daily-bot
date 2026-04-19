"""
股市模組 - 取得台灣股票資料
1. 個股股價 - 證交所 API
2. 熱門股票 - 證交所 API
3. 股市新聞 - Gemini AI
"""

import requests

# Gemini API Key
GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

# 證交所 API 網址
TWSE_API = "mis.twse.com.tw"

# 熱門股票代碼列表
TOP_STOCKS = [
    "2330",  # 台積電
    "2317",  # 鴻海
    "2303",  # 聯電
    "2454",  # 聯發科
    "2412",  # 中華電
    "2885",  # 元大金
    "2891",  # 中信金
    "2884",  # 第一金
    "2883",  # 兆豐金
    "2002",  # 中鋼
    "1216",  # 統一
    "3008",  # 雲象
    "2382",  # 廣達
    "3034",  # 聯詠
    "3673",  # 緯穎
    "6515",  # 慧聖
    "00679B", # 元大台灣50反1
    "0050",  # 元大台灣50
    "00878", # 國泰永續高股息
    "00940"  # 元大台灣價值高息
]

def get_stock(symbol):
    """
    取得個股股價
    symbol: 股票代碼 (如 2330 是台積電)
    """
    try:
        # 證交所歷史股價 API
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=&stockNo={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers).json()
        
        data = r.get("data", [])
        if data:
            # 取最新一筆資料
            latest = data[-1]
            name = r.get("title", symbol)
            # data 格式: [日期, 成交股數, 成交金額, 開盤價, 最高價, 最低價, 收盤價, 漲跌價差, 成交筆數]
            date, cap, turn, open_price, high, low, close, change, vol = latest
            return f"📈 {name}\n收盤: {close}\n漲跌: {change}\n成交量: {vol}"
        
        return f"📈 {symbol} 無法取得資料"
    except:
        # 如果失敗，嘗試即時報價 API
        try:
            url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{symbol}.tw&json=1&delay=0"
            r = requests.get(url).json()
            if r.get("msgArray"):
                info = r["msgArray"][0]
                return f"📈 {info.get('n', symbol)} {info.get('c', '')}\n目前: {info.get('p', 'N/A')} TWD"
        except:
            pass
        return "📈 股市服務待設定"

def get_top50():
    """
    取得熱門股票排行榜
    用 | 分隔多個股票代碼，一次取得多檔
    """
    try:
        # 用 | 分隔股票代碼
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + "|".join([f"tse_{s}.tw" for s in TOP_STOCKS]) + "&json=1&delay=0"
        r = requests.get(url).json()
        stocks = r.get("msgArray", [])
        
        if not stocks:
            return "📈 無法取得熱門股票資料"
        
        result = "📈 台灣熱門股票 Top 10\n\n"
        for i, s in enumerate(stocks[:10], 1):
            # s 是股票代碼, n 是名稱, z/p 是價格
            price = s.get('z', s.get('p', 'N/A'))
            if price == '-':
                price = s.get('p', 'N/A')
            result += f"{i}. {s.get('c', '')} {s.get('n', '')} - {price}\n"
        return result
    except:
        return "📈 服務異常"

def get_stock_news():
    """
    取得股市新聞
    透過 Gemini AI 取得
    """
    prompt = "請列出 5 條 台灣股市 最新新聞標題，用繁體中文，一行一條"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        if "candidates" in data:
            return "📈 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return "📈 股市新聞服務異常"