from bs4 import BeautifulSoup
import requests
from _datetime import datetime
import csv

COINDESK_PAGE = "https://www.coindesk.com/price/stellar" # FOR PRICES
FCAS_PAGE = "https://cryptoperks.net/en/fundamental-crypto-asset-score" # FOR FCAS COIN HEALTH RATING
XLM_NEWS_PAGE = "https://www.newsnow.co.uk/h/Business+&+Finance/Cryptocurrencies/Stellar?type=ln" # NEWS ARTICLES LINKED TO STELLAR LUMENS

def soupScrape():
    # # GET CURRENT PRICES FROM COINDESK
    pricessoup = BeautifulSoup(requests.get(COINDESK_PAGE, headers={'Cache-Control': 'no-cache'}).text, 'html.parser')
    for coinBlock in pricessoup.find_all(name="div", class_="coin-info-block"):
        if coinBlock.select_one(".title").get_text() == "Price":
            CurrentPrice = coinBlock.select_one(".data-definition").get_text()
        elif coinBlock.select_one(".title").get_text() == "Market Cap":
            MarketCap = coinBlock.select_one(".data-definition").get_text()
        elif coinBlock.select_one(".title").get_text() == "Volume (24h)":
            Volume_24hr = coinBlock.select_one(".data-definition").get_text()
        elif coinBlock.select_one(".title").get_text() == "24 Hour Low":
            Low_24hr = coinBlock.select_one(".data-definition").get_text()
        elif coinBlock.select_one(".title").get_text() == "24 Hour High":
            High_24hr = coinBlock.select_one(".data-definition").get_text()
    # # GET CURRENT FCAS HEALTH SCORE
    FCASsoup = BeautifulSoup(requests.get(FCAS_PAGE, headers={'Cache-Control': 'no-cache'}).text, 'html.parser')
    for card in FCASsoup.find_all(name="div", class_="card bg-light mb-3"):
        if card.select_one(".card-header").select_one(".text-of-asset").get_text() == "Stellar":
            FCASScore = card.select_one(".card-body").select_one("strong").get_text()
    # GET CURRENT XLM NEWS
    NewsSoup = BeautifulSoup(requests.get(XLM_NEWS_PAGE, headers={'Cache-Control': 'no-cache'}).text, 'html.parser')
    news_headlines = []
    for newsCard in NewsSoup.select_one(".newsfeed ").find_all(name="div", class_="hl"):
        text_value = newsCard.select_one(".hl__inner").select_one(".time")
        textcontent = text_value.get_text() if text_value else "empty"
        if len(textcontent) == 5:
            Headline = newsCard.select_one(".hl__inner").select_one(".hll").get_text()
            news_headlines.append(Headline)
        else:
            continue
    ArticlesToday = len(news_headlines)

    # WRITE DETAILS TO CSV
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    coinlist = [now,CurrentPrice,High_24hr,Low_24hr, Volume_24hr,MarketCap,FCASScore,ArticlesToday]
    with open("XLM Analysis.csv", 'a', newline='') as CSVFile:
        writer_object = csv.writer(CSVFile)
        writer_object.writerow(coinlist)


soupScrape()