import numpy as np
import pandas as pd
from datetime import datetime, timedelta

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
        self.purse = sum([self.holdings[x].cash for x in self.holdings])
        self.port_val = self.purse + self.pos_val

    def print_dat(self, date):
        self.get_val(date)
        
        inv = [['name', 'curr_price', 'pos', 'hold_cash']]
        for hold in self.holdings:
            inv.append([str(x) for x in [self.holdings[hold].name,
                                         self.holdings[hold].curr_price,
                                         self.holdings[hold].curr_pos,
                                         self.holdings[hold].cash]])
        inv.append(['', 'port_purse', 'port_pos_val', 'port_val'])
        inv.append([str(x) for x in ['Portfolio', self.purse, self.pos_val, self.port_val]])
        colwidth = max(len(word) for row in inv for word in row[:-1]) + 2
        for row in inv:
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
        self.trades = []
        self.df = None

    def get_df(self, data_loc, start, end):
        start, end = [pd.to_datetime(x).date() for x in [start, end]]
        df = pd.read_csv(data_loc + self.name + '.csv')
        df.iloc[:, 0] = [pd.to_datetime(x).date() for x in df.iloc[:, 0]]
        df = df[(df.iloc[:, 0] >= start) & (df.iloc[:, 0] <= end)]
        self.df = df.iloc[:, [0, 5]]

    def trade(self, date, pos):
        self.curr_price = self.df[self.df.iloc[:, 0] == date].iloc[0, 1]
        self.trades.append(Trade(date, pos, self.curr_price))
        self.curr_pos += pos
        self.cash -= self.curr_price * pos
        
    def print_hold_dat(self):
        inv = [['Stock', 'Pos', 'Curr Price', 'Val']]
        colwidth = max(len(word) for row in inv for word in row[:-1]) + 2
        inv.append([str(x) for x in [self.name, 
                                     self.curr_pos,
                                     self.curr_price,
                                     self.curr_val]])
        for row in inv:
            print("".join(word.ljust(colwidth) for word in row))
            
    def curr_hold_dat(self, date):
        self.curr_price = self.df[self.df.iloc[:, 0] == date].iloc[0, 1]
        self.curr_val = self.curr_pos * self.curr_price
        if self.curr_pos > 0:
            self.side = 'long'
        elif self.curr_pos < 0:
            self.side = 'short'
        else:
            self.side = 'flat'
        
    def day_close(self, date):
        pass


class Trade:
    def __init__(self, date, trade_pos, decision_price):
        self.date = date
        self.trade_pos = trade_pos
        self.dec_price = decision_price
        self.trade_val = self.trade_pos * self.dec_price




