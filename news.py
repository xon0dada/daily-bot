API_KEY = "48b077995ba8419f8f4da5256744b3fd"

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=tw&apiKey={API_KEY}"
        r = requests.get(url).json()
        articles = r.get("articles", [])[:5]
        if not articles:
            return "📰 目前無法取得新聞"
        news = "📰 台灣新聞\n\n"
        for i, a in enumerate(articles, 1):
            news += f"{i}. {a.get('title', '無標題')}\n"
        return news
    except:
        return "📰 新聞服務待設定"