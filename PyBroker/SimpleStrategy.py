from Strategy import Strategy
from StockData import Market
from Trader import Trader
import math

class SimpleStrategy(Strategy):

    def sell_positions(self):
        for position in self.trader.positions:
            percent_gain = (position.current_price - position.start_price)/position.start_price
            if percent_gain > 0.05 or percent_gain < -0.05:
                self.trader.sell_stock(position.stock, position.shares)

    def find_increasing_stocks(self, day):
        stocks = {}
        for stock_name in self.market.stocks:
            if stock_name == "SPX":
                continue

            stock = self.market.stocks[stock_name]

            if stock.get_close_price(day) > 125.0 or stock.get_close_price(
                    day) < 31.0:
                # print "Invalid Stock", stock_name, "Size:", len(stock.close_prices)
                continue

            close_price = stock.get_close_price(day - 1)
            prev_close_price = stock.get_close_price(day - 2)

            if close_price > prev_close_price and prev_close_price != 0.0:
                stocks[stock.stock_name] = (close_price - prev_close_price) / prev_close_price

        return stocks

    def buy_positions(self):
        buys = []

        if self.trader.capital > 1000.0:
            increasing_stocks = self.find_increasing_stocks(self.trader.day)

            for stock_name in increasing_stocks:
                stock = self.market.stocks[stock_name]
                buys.append(stock)

            max_increase = -100.0
            max_stock = None
            for stock in buys:
                if increasing_stocks[stock.stock_name] > max_increase:
                    max_increase = increasing_stocks[stock.stock_name]
                    max_stock = stock
            if max_stock is not None:
                print "SimpleStrategy: Buy stock", max_stock.stock_name, "For Price:", max_stock.get_close_price(
                    self.trader.day), "% Increase:", max_increase
                shares = int(self.trader.get_total_assets() * 0.006)
                if max_stock.get_close_price(self.trader.day) < 38:
                    shares = 200

                if max_stock.get_close_price(self.trader.day) * shares > self.trader.capital:
                    shares = math.floor(self.trader.capital / max_stock.get_close_price(self.trader.day))
                self.trader.buy_stock(max_stock, shares)

    def trade_for_day(self):
        # Find stocks to buy if holding cash
        self.buy_positions()

        # Sell stocks if they've reached a profit threshold
        self.sell_positions()

        super(SimpleStrategy, self).trade_for_day()
