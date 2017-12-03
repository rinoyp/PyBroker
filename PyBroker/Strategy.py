from StockData import Market
from Trader import Trader
import math

class Strategy(object):
    def __init__(self, trader, market):
        self.trader = trader
        self.market = market
        self.start_day = trader.day
        self.max_gains = 0.0
        self.max_losses = 0.0
        self.highest_capital = self.trader.capital
        self.lowest_capital = self.trader.capital

    def trade_for_day(self):
        total_assets = self.trader.get_total_assets()
        if total_assets > self.highest_capital:
            self.highest_capital = total_assets
        elif total_assets < self.lowest_capital:
            self.lowest_capital = total_assets

        for position in self.trader.positions:
            if position.gains > self.max_gains:
                self.max_gains = position.gains
            elif position.gains < self.max_losses:
                self.max_losses = position.gains

        current_date = self.market.get_date(self.trader.day)
        print "Strategy: Ending Day %s Total Assets: $%.2f\n" %(current_date, total_assets)
        self.trader.next_trading_day()

    def trade_for_days(self, days):
        while self.trader.day < self.start_day + days:
            self.trade_for_day()

        print "Strategy: Total available capital: $%.2f After %d days" %(self.trader.capital, days)
        market_value = self.trader.get_market_value()
        print "Strategy: Total Market Value: $%.2f" %market_value
        total_assets = self.trader.get_total_assets()
        print "Strategy: Total Assets: $%.2f" %total_assets
        print "Strategy: Highest Capital: $%.2f Lowest Capital: $%.2f" %(self.highest_capital, self.lowest_capital)
        print "Strategy: Max Gains Per Trade: $%.2f Max Loss Per Trade: $%.2f" %(self.max_gains, self.max_losses)

