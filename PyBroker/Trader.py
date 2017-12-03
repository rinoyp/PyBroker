class Position(object):
    def __init__(self, stock, shares = 0, day = 0):
        self.stock = stock
        self.start_price = self.stock.get_close_price(day)
        self.current_price = self.start_price
        self.shares  = shares
        self.day = day
        self.days_held = 0
        self.gains = 0.0
        self.earnings = 0.0
        self.dividends = 0.0


    def hold(self, day):
        self.days_held+=1
        volume_ratio = self.stock.get_adj_volume(day) / self.stock.get_volume(day)
        prev_volume_ratio = self.stock.get_adj_volume(day - 1) / self.stock.get_volume(day - 1)
        if volume_ratio != prev_volume_ratio:
            new_ratio = prev_volume_ratio/volume_ratio
            self.shares *= new_ratio
            print "Position: Stock Split vr: %f pvr: %f" %(volume_ratio, prev_volume_ratio)

        self.dividends += self.stock.get_dividend(day) * self.shares
        self.current_price = self.stock.get_close_price(day)
        self.gains = self.shares * (self.current_price - self.start_price) + self.dividends
        revenue = self.shares * self.current_price
        print  "Position: Holding",self.shares,self.stock.stock_name,"for day", self.days_held, "Current Prce:", self.current_price, "Gains:", self.gains

    def buy(self, shares, day):
        # Can only buy more if not currently holding any shares
        if self.shares != 0:
            return

        self.shares += shares
        self.start_price = self.stock.get_close_price(day)
        self.day = day
        self.days_held = 0
        self.current_price = self.start_price
        self.gains = 0
        self.dividends = 0.0

    def get_cost(self):
        return self.start_price * self.shares

    def get_market_value(self, day):
        return self.stock.get_close_price(day) * self.shares

    def sell(self, shares):
        if shares > self.shares:
            print "Position: Error selling shares"
            return

        self.shares -= shares
        self.earnings += shares * (self.current_price - self.start_price)
        if self.dividends > 0.0:
            print "Position: Earned $%.2f Dividends" %(self.dividends)
        return self.current_price * shares + self.dividends


    def get_gains(self):
        return self.gains

    def get_earnings(self):
        return self.earnings

class UnsettledPosition(object):
    def __init__(self, revenue, day, sell_day):
        self.revenue = revenue
        self.day = day
        self.sell_day = sell_day

class Trader(object):
    def __init__(self, capital = 0, gains = 0, day = 0):
        self.capital = capital
        self.lowest_assets = capital
        self.highest_assets = capital
        self.initial_capital = capital
        self.gains = gains
        self.positions = []
        self.position_cnt = 0
        self.unsettled_positions = []
        self.day = day
        self.dates = []

    def get_market_value(self):
        f = lambda x,y: x + y
        market_values = [self.positions[i].get_market_value(self.day) for i in range(len(self.positions))]
        market_value = reduce(f, market_values, 0)
        return market_value

    def get_unsettled_capital(self):
        f = lambda x,y: x + y.revenue
        unsettled_capital = reduce(f, self.unsettled_positions, 0)
        return unsettled_capital

    def get_total_assets(self):
        return self.get_market_value() + self.capital + self.get_unsettled_capital()

    def next_trading_day(self):
        self.day += 1
        for position in self.positions:
            if position.shares > 0:
                position.hold(self.day)

        for unsettled_position in self.unsettled_positions:
            if self.day - unsettled_position.day > 6 and self.day - unsettled_position.sell_day > 3:
                # print "Trader: Settled Position For Revenue", unsettled_position.revenue
                self.capital += unsettled_position.revenue
                unsettled_position.revenue = 0
            elif unsettled_position.revenue > 0:
                # print "Trader: UnSettled Position Revenue:", unsettled_position.revenue
                pass

        self.unsettled_positions = [self.unsettled_positions[i] for i in range(len(self.unsettled_positions)) if self.unsettled_positions[i].revenue > 0]


    def buy_stock(self, stock, shares):
        for position in self.positions:
            if position.stock.stock_name == stock.stock_name:
                print "Trader: Error buying stock: Already holding"
                return

        position = Position(stock, shares, self.day)
        if self.capital - position.get_cost() < 0:
            print  "Trader: Error buying stock: Not enough capital"
            return
        self.capital -= position.get_cost()
        print "Trader: Bought Position ", position.stock.stock_name
        print "Trader: Remaining Capital", self.capital
        self.positions.append(position)
        self.position_cnt += 1

    def sell_stock(self, stock, shares):
        self.position_cnt -= 1
        stock_index = 0
        for i, position in enumerate(self.positions):
            if position.stock.stock_name == stock.stock_name:
                revenue = position.sell(shares)
                stock_index = i
                unsettled_position = UnsettledPosition(revenue, position.day, self.day)
                self.unsettled_positions.append(unsettled_position)
                print "Trader: Sold Position ", position.stock.stock_name, "For Revenue:", revenue
                break

        self.positions.remove(self.positions[stock_index])



