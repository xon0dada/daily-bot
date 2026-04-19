import requests

GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

TWSE_API = "mis.twse.com.tw"
TOP_STOCKS = ["2330", "2317", "2303", "2454", "2412", "2885", "2891", "2884", "2883", "2002", "1216", "3008", "2382", "3034", "3673", "6515", "00679B", "0050", "00878", "00940"] 

def get_stock(symbol):
    try:
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=&stockNo={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers).json()
        data = r.get("data", [])
        if data:
            latest = data[-1]
            name = r.get("title", symbol)
            date, cap, turn, open_price, high, low, close, change, vol = latest
            return f"📈 {name}\n收盤: {close}\n漲跌: {change}\n成交量: {vol}"
        return f"📈 {symbol} 無法取得資料"
    except:
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
    try:
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + "|".join([f"tse_{s}.tw" for s in TOP_STOCKS]) + "&json=1&delay=0"
        r = requests.get(url).json()
        stocks = r.get("msgArray", [])
        if not stocks:
            return "📈 無法取得熱門股票資料"
        result = "📈 台灣熱門股票 Top 10\n\n"
        for i, s in enumerate(stocks[:10], 1):
            price = s.get('z', s.get('p', 'N/A'))
            if price == '-':
                price = s.get('p', 'N/A')
            result += f"{i}. {s.get('c', '')} {s.get('n', '')} - {price}\n"
        return result
    except:
        return "📈 服務異常"

def get_stock_news():
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