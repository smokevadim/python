import cgi
import json


def subscribe(email, ticker, min_price, max_price):
    emails = {}
    tickers = {}
    try:
        with open("emails.json", "r") as file:
            json_data = file.read()
            emails = json.loads(json_data)
            tickers = emails.get(email)['tickers']
    except FileNotFoundError:
        file = open("emails.json", "x")
        file.close()
    except:
        pass
    tickers[ticker] = {"min_price": min_price, "max_price": max_price}
    emails[email] = {"tickers": tickers}

    file = open("emails.json", "w")
    json_data = json.dumps(emails)
    file.write(json_data)
    file.close()


def update_tickers(ticker):
    ticker_list = []
    try:
        with open("tickers.json", "r") as file:
            json_data = file.read()
            ticker_list = json.loads(json_data)['ticker']
    except FileNotFoundError:
        file = open("tickers.json", "x")
        file.close()

    except:
        pass

    if ticker not in ticker_list:
        # append new ticker
        ticker_list.append(ticker)
        file = open("tickers.json", "w")
        json_data = json.dumps({"ticker": ticker_list})
        file.write(json_data)
        file.close()


if __name__ == "__main__":
    form=cgi.FieldStorage()
    print('Content-type: text/html\n')

    email = form.getfirst("email", "")
    ticker = form.getfirst("ticker", "")
    min_price = form.getfirst("min_price", "")
    max_price = form.getfirst("max_price", "")

    if min_price or max_price:
        #subscribe
        subscribe(email, ticker, min_price, max_price)
        update_tickers(ticker)
    else:
        # unsubscribe
        print('unsub done')