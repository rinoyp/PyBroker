from StockData import Stock, Market
from Trader import Trader
from SimpleStrategy import SimpleStrategy

def main():
    stock_names = []
    with open("PyBroker/sp500.txt", "r") as stocks:
        for stock in stocks:
            stock_names.append(stock[:-1])

    market = Market(stock_names)
    trader = Trader(capital=1000000.0, day=252)

    strategy = SimpleStrategy(trader, market)
    strategy.trade_for_days(252)

main()
