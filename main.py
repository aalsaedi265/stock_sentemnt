
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
    
# stock_data = news_tables['V']
# stock_row = stock_data.find_all('tr')

parsed_data = []

for ticker, news in news_tables.items():
    for row in news.findAll('tr'):
        a_tag= row.find('a')
        if a_tag:
            title = a_tag.text
            date_data = row.td.text.split(' ')
            
            if len(date_data) == 1: time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]
                
        parsed_data.append([ticker, date, time, title])
        
