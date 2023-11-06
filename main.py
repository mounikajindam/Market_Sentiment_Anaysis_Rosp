from ctypes import windll
import os
from matplotlib.ft2font import BOLD
import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import tkinter as tk
from ctypes import windll
from tabulate import tabulate
from jinja2 import *
import webbrowser

windll.shcore.SetProcessDpiAwareness(1)
pd.option_context('display.max_rows', None, 'display.max_columns', None)

root = tk.Tk()
root.title('Tiny Insights')
root.eval('tk::PlaceWindow . center')
root.geometry('400x300')

lbl = tk.Label(root, text="Enter a ticker symbol")
lbl.pack()

lbl1 = tk.Label(root, text="[ALL CAPS]")
lbl1.pack()

en = tk.Entry()
en.pack()
ticker = ''


def msft():
    global ticker
    ticker = en.get()
    root.destroy()


bt = tk.Button(text='Enter', command=msft)
bt.pack()

lbl3 = tk.Label(text="Stay patient and trust the journey.")
lbl3.pack()

root.mainloop()

#ticker = input("Enter a TICKER symbol (case-sensitive): ")

url = "https://financialmodelingprep.com/financial-summary/" + ticker
request = requests.get(url)
# print(request.text)

parser = BeautifulSoup(request.text, "html.parser")
news_html = parser.find_all('a', {'class': 'article'})
# print(news_html[0])

sentiments = []
for i in range(0, len(news_html)):
    sentiments.append(
        {
            'ticker': ticker,
            'date': news_html[i].find('h5', {'class': 'article__date'}).text,
            'title': news_html[i].find('h4', {'class': 'article__title-text'}).text,
            'text': news_html[i].find('p', {'class': 'article__text'}).text
        }
    )

# print(sentiments[0])

df = pd.DataFrame(sentiments)
#df['ticker'] = df['ticker'].str.lstrip()
#df['date'] = df['date'].str.lstrip()
#df['title'] = df['title'].str.replace('  ', '')
#df['text'] = df['text'].str.lstrip()
#df = df.set_index('date')

# df = df.replace(r"^ +| +$", r"", regex=True)

print(df)

#analyser = SentimentIntensityAnalyzer()
# print(df['text'][4])
# print(analyser.polarity_scores(df['text'][4]))


def calc_sentiment_score(text):
    return analyser.polarity_scores(text)["compound"]


analyser = SentimentIntensityAnalyzer()
df['sentiment_score'] = df['text'].apply(calc_sentiment_score)

# print(df)

mean = df['sentiment_score'].mean()
print("")
# print(mean)
htxt = ""

if (mean > 0.2):
    htxt = "Good Sentiments."
elif(mean < -0.05):
    htxt = "Bad Sentiments."
else:
    htxt = "Neutral Sentiments."
xax = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
yax = df['sentiment_score']
plt.bar(xax, yax)
plt.xlabel(htxt)
plt.ylabel(mean)
plt.show()
#df['sentiment_score'].plot(kind='bar', figsize=(10, 5))

df.to_html('news.html')
url = 'file://' + os.getcwd() + '/news.html'
webbrowser.open(url, new=2)
