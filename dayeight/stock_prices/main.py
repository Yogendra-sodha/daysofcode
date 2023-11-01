import requests
import json
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "TESLA"
stock_key = "T38X7H1DGOGWCTYY"
json_path = "dayeight/stock_prices/stock_prices.json"

stock_param = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey": stock_key
}

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock(param,days=2):
    response = requests.get("https://www.alphavantage.co/query",params=param)
    response.raise_for_status()
    stock_data = response.json()
    print(stock_data)
    try:
        with open(json_path,"r") as read_file:
            content = json.load(read_file)
            content.update(stock_data)

        with open(json_path,"w") as write_file:
            json.dump(content,write_file,indent=4)

    except FileNotFoundError:
        with open(json_path,"w") as new_file:
            json.dump(stock_data,new_file,indent=4)

with open(json_path,"r") as df:
    prices = json.load(df)

prices = prices["Time Series (Daily)"]
def stockPrecentChange(days=2):
    two_day = {}
    temp = 0
    for i in prices:
        temp+=1
        if temp>2:
            break
        close_price = prices.get(i)["4. close"]
        two_day[i] = int(float(close_price))
    two_day = list(two_day.values())[::-1]
    diff = round(((two_day[0] - two_day[1])/two_day[0])*100,2)
    return diff



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_key = "6c14060e8f31474cbf23d565343a718d"
news_json = "dayeight/stock_prices/news.json"

news_param = {
    "q":COMPANY_NAME,
    "apiKey":news_key
}

def getNews():
    response = requests.get("https://newsapi.org/v2/everything",params=news_param)
    response.raise_for_status()
    news = response.json()
    print(news)
    try:
        with open(news_json,"r") as read_file:
            news_data = json.load(read_file)
            news_data.update(news)
        
        with open(news_json,"w") as write_file:
            json.dump(news_data,write_file,indent=4)

    except FileNotFoundError:
        with open(news_json,"w") as open_file:
            json.dump(news,open_file,indent=4)

with open(news_json,"r") as load_file:
    content = json.load(load_file)

top_news = content["articles"][:3]
top_news = [str(i+1)+"-"+top_news[i]["title"] for i in range(len(top_news))]
top_news = " ".join(top_news)

change = stockPrecentChange()
stock_change = (f"{change} % up")
tesla_news = (f"Headline :{top_news}")

sms_body = stock_change+"\n"+tesla_news

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

account_sid = os.getenv("account_sid")
auth_token  = os.getenv("auth_token")

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+12012389412",
    from_="+18776163360",
    body=sms_body)

print(message.sid)



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

