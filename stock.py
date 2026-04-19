import requests

TWSE_API = "mis.twse.com.tw"
TOP_STOCKS = ["2330", "2317", "2303", "2454", "2412", "2885", "2891", "2884", "2883", "2002", "1216", "3008", "2382", "3034", "3673", "6515", "00679B", "0050", "00878", "00940", "2618", "2409", "3481", "2337", "0056", "2474", "2327", "2362", "2308", "2327", "2377", "1590", "6703", "3231", "4906", "2405", "6223", "3545", "1805", "1707", "1711", "2481", "2449", "2328", "2105", "1710", "2363", "2027", "4958", "2347", "6285"]

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
        result = "📈 台灣熱門股票 Top 20\n\n"
        for i, s in enumerate(stocks[:20], 1):
            price = s.get('z', s.get('p', 'N/A'))
            if price == '-':
                price = s.get('p', 'N/A')
            result += f"{i}. {s.get('c', '')} {s.get('n', '')} - {price}\n"
        return result
    except Exception as e:
        return "📈 服務異常，請稍後再試"