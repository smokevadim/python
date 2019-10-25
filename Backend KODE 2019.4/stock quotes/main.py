import json
from threading import Thread, Event

from alphavantage_wrapper.AlphaVantage import AlphaVantage

from http.server import HTTPServer, CGIHTTPRequestHandler


def get_price(ticker):
    # API key
    api_key = 'YRKRMSKEG1ZJG5B2'

    av = AlphaVantage(api_key)

    # The company's stock symbol (ex.: Tesla)
    # ticker = 'NOKIA.HE'
    # Retrieval the 100 most recent financial data (daily time series, adjusted)
    # stock = av.get_time_series_daily_adjusted(ticker)
    stock = av.get_global_quote(ticker)
    # do stuff with data
    update_data(ticker, stock.values[4, 0])


def update_data(ticker, price):
    data = {}
    try:
        with open("data.json", "r") as file:
            json_data = file.read()
            data = json.loads(json_data)
    except FileNotFoundError:
        file = open("data.json", "x")
        file.close()
    except:
        pass
    data[ticker] = price
    file = open("data.json", "w")
    json_data = json.dumps(data)
    file.write(json_data)
    file.close()


def read_ticker_list():
    try:
        with open("tickers.json", "r") as file:
            json_data = file.read()
            return json.loads(json_data)['ticker']
    except:
        return None


def read_config():
    try:
        with open("emails.json", "r") as file:
            json_data = file.read()
            return json.loads(json_data)
    except:
        return None


def send_email(email, message):
    pass


def check_changes(ticker):
    try:
        with open("emails.json", "r") as file:
            json_data = file.read()
            emails = json.loads(json_data)

        with open("data.json", "r") as file:
            json_data = file.read()
            data = json.loads(json_data)

            # for ticker in data.keys():
            for email in emails.keys():
                price = float(data.get(ticker))

                tickers = emails.get(email)['tickers']
                for email_ticker in tickers:
                    min_price = float(email_ticker['min_price'])
                    max_price = float(email_ticker['max_price'])

                    if ticker == email_ticker:
                        message = ''
                        if (min_price > 0) and (price < min_price):
                            message = 'Price {} under minimum {}'.format(price, min_price)

                            # here we calling send email function but specification not asking for it
                            # and we just outputting text on display
                            print('{}: {}'.format(email, message))

                        if (max_price > 0) and (price > max_price):
                            message = 'Price {} above maximum {}'.format(price, max_price)

                            # here we calling send email function but specification not asking for it
                            # and we just outputting text on display
                            print('{}: {}'.format(email, message))
    except:
        pass


class GetPriceBackground(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        # reading tickers from file
        ticker_list = read_ticker_list()

        # trying get price in each ticker
        while True:
            for ticker in ticker_list:
                get_price(ticker)
                check_changes(ticker)

                # coz 'alphavantage' API allow for free only 5 requests per minute
                self.stopped.wait(12)


class HTTPPOSTServer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):


        server_address = ("localhost", 8000)
        # same directory as html file
        CGIHTTPRequestHandler.cgi_directories = ["/","\\"]
        httpd = HTTPServer(server_address, CGIHTTPRequestHandler)

        # waiting for POST request
        httpd.serve_forever()

if __name__ == "__main__":
    # update_tickers('TSLA')
    # update_config('it@zarodiny.ru','NOC','200','600')

    # Starting simple HTTP server
    thread_HTTPPOSTServer = HTTPPOSTServer()
    thread_HTTPPOSTServer.start()


    # Starting collect tickers and send emails in another thread
    stopFlag = Event()
    thread_GetPriceBackground = GetPriceBackground(stopFlag)
    thread_GetPriceBackground.start()

    # stopFlag.set()
