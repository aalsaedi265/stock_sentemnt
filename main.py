
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# 'news-table'
news_tables= {}

url = "https://finviz.com/quote.ashx?t="
tickers =['V','META', 'MA', 'GOOGL', 'TSLA','MSFT', 'AAPL', 'MO']

for ticker in tickers:
    url_ticker = url + ticker
    req = Request(url_ticker, headers={'User-Agent': 'STOCK_SENTEMENT'})
    webpage = urlopen(req).read()
    
    table = BeautifulSoup(webpage, "html.parser")
    
    news = table.find(id='news-table')
    news_tables[ticker] = news
    
