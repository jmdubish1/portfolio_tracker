import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from random import uniform

class Portfolio:
    def __init__(self, name):
        self.name = name
        self.purse = 0
        self.pnl = 0
        self.pos_val = 0
        self.port_val = 0
        self.holdings = {}

    def add_holding(self, _holding):
        self.holdings[_holding.name] = _holding

    def get_val(self, date):
        for x in self.holdings:
            self.holdings[x].curr_hold_dat(date)
        self.pos_val = sum([self.holdings[x].curr_val for x in self.holdings])
        self.purse = sum([self.holdings[x].cash for x in self.holdings]) + \
                     sum([self.holdings[x].dividends for x in self.holdings])

        self.port_val = self.purse + self.pos_val

    def get_data(self, tick, dat_loc, start):
        t_hold = Holding(tick, 0)
        t_hold.get_df(dat_loc)
        t_hold.get_year_before(start)
        self.add_holding(t_hold)

    def print_dat(self, date):
        self.get_val(date)

        inv = [['name', 'curr_price', 'pos', 'hold_cash', 'allocation']]
        for hold in self.holdings:
            inv.append([str(x) for x in [self.holdings[hold].name,
                                         self.holdings[hold].curr_price,
                                         self.holdings[hold].curr_pos,
                                         self.holdings[hold].cash,
                                         self.holdings[hold].allo]])
        inv.append(['', 'port_purse', 'port_pos_val', 'port_val'])
        inv.append([str(x) for x in ['Portfolio', self.purse, self.pos_val, self.port_val]])
        colwidth = max(len(word) for row in inv for word in row[:-1]) + 2
        for row in inv:
            print("".join(word.ljust(colwidth) for word in row))

        print(" ")

    def print_res(self, date):
        self.get_val(date)
        res = [['', 'port_purse', 'port_pos_val', 'port_val']]
        res.append([str(x) for x in ['Portfolio', self.purse, self.pos_val, self.port_val]])
        colwidth = max(len(word) for row in res for word in row[:-1]) + 2
        for row in res:
            print("".join(word.ljust(colwidth) for word in row))

        print(" ")


class Holding:
    def __init__(self, ticker, cash):
        self.name = ticker
        self.cash = cash
        self.curr_pos = 0
        self.curr_price = 0
        self.curr_val = 0
        self.side = None
        self.pnl = 0
        self.allo = 0
        self.trades = []
        self.df = None
        self.year_before = []
        self.daily_ret = []
        self.dividends = 0
        self.dividend_dat = []

    def get_df(self, data_loc):
        df = pd.read_csv(data_loc + self.name + '.csv', usecols=['date',
                                                                 '5. adjusted close',
                                                                 '7. dividend amount'])
        df.iloc[:, 0] = [pd.to_datetime(x).date() for x in df.iloc[:, 0]]
        self.df = df

    def trade(self, date, pos):
        self.curr_hold_dat(date)
        self.trades.append(Trade(date, pos, self.curr_price))
        self.curr_pos += pos
        self.cash -= self.curr_price * pos

    def check_div(self, date):
        if len(self.trades) > 0:
            last_trade_dt = self.trades[-1].date
            if last_trade_dt:
                check_df = self.df[(self.df.iloc[:, 0] >= last_trade_dt) &
                                   (self.df.iloc[:, 0] <= date)]
                if any(check_df[check_df.iloc[:, 2] > 0]):
                    check_df = check_df[check_df.iloc[:, 2] > 0]

                    for r in check_df.iloc[:, 2]:
                        if r > 0:
                            self.dividends += r

    def print_hold_dat(self):
        inv = [['Stock', 'Pos', 'Curr Price', 'Val', 'Allocation']]
        colwidth = max(len(word) for row in inv for word in row[:-1]) + 2
        inv.append([str(x) for x in [self.name, 
                                     self.curr_pos,
                                     self.curr_price,
                                     self.curr_val,
                                     self.allo]])
        for row in inv:
            print("".join(word.ljust(colwidth) for word in row))
            
    def curr_hold_dat(self, date):
        self.curr_price = self.df[self.df.iloc[:, 0] == date].iloc[0, 1]
        self.curr_val = self.curr_pos * self.curr_price
        self.check_div(date)
        if self.curr_pos > 0:
            self.side = 'long'
        elif self.curr_pos < 0:
            self.side = 'short'
        else:
            self.side = 'flat'
        
    def day_close(self, date):
        self.curr_price = self.df[self.df.iloc[:, 0] == date].iloc[0, 1]
        return self.curr_price

    def get_year_before(self, start):
        year_before_df = self.df[(self.df.iloc[:, 0] <= pd.to_datetime(start).date())]
        self.year_before = year_before_df.iloc[252:505, 1]
        self.dividend_dat = sum(year_before_df.iloc[252:505, 2])/self.year_before.iloc[-252]

        self.daily_ret = np.log(self.year_before) - np.log(self.year_before.shift(1))
        self.daily_ret.append(pd.Series(self.dividend_dat))

    def holding_reset(self):
        self.cash = 0
        self.curr_pos = 0
        self.curr_price = 0
        self.curr_val = 0
        self.side = None
        self.pnl = 0
        self.allo = 0
        self.trades = []
        self.dividends = 0

class Trade:
    def __init__(self, date, trade_pos, decision_price):
        self.date = date
        self.trade_pos = trade_pos
        self.dec_price = decision_price
        self.trade_val = self.trade_pos * self.dec_price

    def find_trade(self, date):
        if self.date == date:
            return self.trade_val, self.date

    def print_trade_dat(self):
        inv = [['Date', 'Pos', 'Decision Price', 'Val']]
        colwidth = max(len(word) for row in inv for word in row[:-1]) + 2
        inv.append([str(x) for x in [self.date,
                                     self.trade_pos,
                                     self.dec_price,
                                     self.trade_val]])
        for row in inv:
            print("".join(word.ljust(colwidth) for word in row))

