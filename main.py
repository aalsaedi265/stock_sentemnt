
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt


# Fetch the news data
news_tables = {}

url = "https://finviz.com/quote.ashx?t="
tickers = ['V', 'META', 'MA', 'GOOGL', 'TSLA', 'MSFT', 'AAPL', 'MO']

for ticker in tickers:
    url_ticker = url + ticker
    req = Request(url_ticker, headers={'User-Agent': 'STOCK_SENTEMENT'})
    webpage = urlopen(req).read()

    table = BeautifulSoup(webpage, "html.parser")

    news = table.find(id='news-table')
    news_tables[ticker] = news

# Parse the news data
parsed_data = []

for ticker, news in news_tables.items():
    if news:  # Ensure there is a news table for the ticker
        for row in news.findAll('tr'):
            a_tag = row.find('a')
            if a_tag:
                title = a_tag.text.strip()
                date_data = row.td.text.strip().split(' ')

                date = ""
                time = ""

                if len(date_data) == 1:
                    time = date_data[0].strip()
                elif len(date_data) >= 2:
                    date = date_data[0].strip()
                    time = date_data[1].strip()

                # Ensure the date does not contain unwanted characters
                date = date.replace('\r', '').replace('\n', '').strip()
                parsed_data.append([ticker, date, time, title])

# Convert parsed data to DataFrame
df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

# Debug: Print the initial DataFrame
# print("Initial DataFrame:")
# print(df.head())

# Analyze sentiment
vader = SentimentIntensityAnalyzer()
f = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(f)

# Ensure the date column is correctly parsed and exclude NaT
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

# print("\nDataFrame after date parsing:")
# print(df.head())
# print("\nNumber of NaT dates:", df['date'].isna().sum())

# Drop rows with NaT in the date column
df = df.dropna(subset=['date'])

# print("\nDataFrame after dropping NaT dates:")
# print(df.head())

fig, ax = plt.subplots(figsize=(20, 10))

# Group by 'ticker' and 'date', then calculate the mean of 'compound'
mean_df = df.groupby(['ticker', 'date'])['compound'].mean().unstack()

# Plot using the specified axes object, with thicker bars
mean_df.plot(kind='bar', ax=ax, width=1.5)  # Increase the width for thicker bars

# Move the legend (dates) to the right side of the plot
ax.legend(title='Date', bbox_to_anchor=(1.05, 1), loc='upper left')

# Set the label and title
ax.set_xlabel('Ticker')
ax.set_ylabel('Average Sentiment (Compound)')
ax.set_title('Average Sentiment by Ticker and Date')

# Display the plot
plt.tight_layout()  # Adjust layout to make space for the legend on the right
plt.show()