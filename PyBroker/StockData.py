import pandas as pd
import threading

class Market(object):
    def __init__(self, stock_names = []):
        self.stocks = {}
        self.l = threading.Lock()
        self.s = threading.Semaphore(20)
        self.threads = []
        print "Market: Initializing Stocks..."
        for stock_name in stock_names:
            t = threading.Thread(target=self.init_stock, name=stock_name, args=(stock_name,))
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        self.num_trading_days = len(self.stocks["AAPL"].data)
        print "Market: %d trading days" %self.num_trading_days
        for stock_name in self.stocks:
            self.stocks[stock_name].num_trading_days = self.num_trading_days
            self.stocks[stock_name].dates = self.stocks["AAPL"].data.index

        print "Market Size:", len(self.stocks)

    def init_stock(self, stock_name):
        self.s.acquire()
        stock = Stock(stock_name)
        stock.date_cb = self.get_date
        self.s.release()
        if stock.data is not None:
            self.l.acquire()
            self.stocks[stock_name] = stock
            self.l.release()

    def get_stock(self, stock_name):
        return self.stocks[stock_name]

    def get_date(self, day):
        return self.stocks["AAPL"].data.index[day]


class Stock(object):
    def __init__(self, stock_name = ""):
        self.stock_name = stock_name
        self.num_trading_days = 0
        self.dates = None
        filename = "Data/" + stock_name + ".csv"
        labels = ["date",
                  "open",
                  "high",
                  "low",
                  "close",
                  "volume",
                  "ex-dividend",
                  "split_ratio",
                  "adj_open",
                  "adj_high",
                  "adj_low",
                  "adj_close",
                  "adj_volume"]

        labels.append("5-day-ma")
        labels.append("20-day-ma")
        labels.append("50-day-ma")
        labels.append("200-day-ma")
        labels.append("5-day-std")
        labels.append("20-day-std")
        labels.append("50-day-std")
        labels.append("200-day-std")
        try:
            self.csv_data = pd.read_csv(filename,names=labels,parse_dates=["date"],index_col="date")
        except IOError:
            self.data = None
            return

        self.data = self.csv_data[1:].convert_objects(convert_numeric=True)

    def get_date(self, day):
        pass

    def calculate_averages(self):
        self.data["5-day"] = self.calculateAverage(5)
        self.data["20-day"] = self.calculateAverage(20)
        self.data["50-day"] = self.calculateAverage(50)
        self.data["200-day"] = self.calculateAverage(200)
        # filename = "Data/" + self.stock_name + ".csv"
        # self.data.to_csv(filename)

    def calculateAverage(self, period):
        avgs = []
        for i in range(period-1):
            avgs.append(0.0)

        for i in range(period, len(self.data)+1):
            avg = self.data["close"][i-period:i].mean()
            avgs.append(avg)

        return pd.DataFrame(avgs, index = self.data.index)

    def get_close_price(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["close"].loc[day]
        except KeyError:
            pass

        return value

    def get_open_price(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["open"].loc[day]
        except KeyError:
            pass
        return value

    def get_high_price(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["high"].loc[day]
        except KeyError:
            pass
        return value

    def get_low_price(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["low"].loc[day]
        except KeyError:
            pass
        return value

    def get_average(self, period, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data[period].loc[day]
        except KeyError:
            pass
        return value

    def get_dividend(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["ex-dividend"].loc[day]
        except KeyError:
            pass
        return value

    def get_volume(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["volume"].loc[day]
        except KeyError:
            pass
        return value

    def get_adj_volume(self, day):
        if type(day) == int:
            day = self.dates[day]
        value = 0.0
        try:
            value = self.data["adj_volume"].loc[day]
        except KeyError:
            pass
        return value

    def to_csv(self):
        filename = "Data/" + self.stock_name + ".csv"
        self.data.to_csv(filename)

