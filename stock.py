"""
股市模組 - 取得台灣股票資料
使用證交所官方 OpenAPI: https://openapi.twse.com.tw
"""

import requests

# 證交所 OpenAPI 網址
TWSE_OPENAPI = "https://openapi.twse.com.tw/v1"

# Gemini API Key
GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

# 熱門股票代碼列表
TOP_STOCKS = [
    "2330", "2317", "2303", "2454", "2412", "2885", "2891", "2884", 
    "2883", "2002", "1216", "3008", "2382", "3034", "3673", "6515",
    "0050", "00878", "00940", "00679B"
]

def get_stock(symbol):
    """
    取得個股股價
    使用證交所官網 API (較即時)
    """
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
    """
    取得熱門股票排行榜
    使用證交所即時 API
    """
    try:
        # 用 | 分隔股票代碼，一次取得多檔報價
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
            name = s.get('n', '')
            code = s.get('c', '')
            result += f"{i}. {code} {name} - {price}\n"
        
        return result
    except:
        return "📈 服務異常"

def get_market_index():
    """
    取得大盤指數
    使用證交所 OpenAPI
    """
    try:
        url = f"{TWSE_OPENAPI}/exchangeReport/MI_INDEX?response=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers).json()
        # 處理回應資料
        return f"📊 大盤指數資料取得成功"
    except Exception as e:
        return f"📊 無法取得大盤資料"

def get_valuation(symbol="2330"):
    """
    取得個股本益比、殖利率、股價淨值比
    使用證交所 OpenAPI: /exchangeReport/BWIBBU_ALL
    """
    try:
        # 需要篩選特定股票
        url = f"{TWSE_OPENAPI}/exchangeReport/BWIBBU_ALL?response=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10).json()
        
        # 找出特定股票
        data = r.get("data", [])
        for row in data:
            if row[0] == symbol:
                # 格式: [代號, 名稱, 本益比, 殖利率, 股價淨值比, ...]
                name = row[1]
                pe = row[2]
                dividend = row[3]
                pb = row[4]
                return f"📈 {symbol} {name}\n本益比: {pe}\n殖利率: {dividend}%\n股價淨值比: {pb}"
        
        return f"📈 {symbol} 無法取得評價資料"
    except Exception as e:
        return f"📈 服務異常: {str(e)[:30]}"

def get_etf_ranking():
    """
    取得 ETF 排行
    使用證交所 OpenAPI: /ETFReport/ETFRank
    """
    try:
        url = f"{TWSE_OPENAPI}/ETFReport/ETFRank?response=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10).json()
        
        data = r.get("data", [])
        result = "📊 ETF 排行 Top 5\n\n"
        
        for i, row in enumerate(data[:5], 1):
            # 格式根據 API 回應
            result += f"{i}. {row}\n"
        
        return result if result != "📊 ETF 排行 Top 5\n\n" else "📊 無法取得ETF排行"
    except Exception as e:
        return "📊 ETF 排行服務異常"

def get_stock_news():
    """
    取得股市新聞
    使用 Gemini AI
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