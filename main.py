from port_inventory import *
import pandas as pd

dat_loc = 'C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\Alpha_vantage\\S&P_500\\' \
          'TIME_SERIES_DAILY_ADJUSTED\\'
world = ['AKAM','AAL','BBY']
trade_date = ["2020-01-03", "2020-02-24", "2020-03-12", "2020-04-17",
              "2020-05-14", "2020-06-11", "2020-07-01", "2020-08-03"]
trades = [80, -80, 10, -10, 10, -10, 10, -10]

start = "2020-01-02"
end = "2020-09-01"

def main():

    df = pd.read_csv(dat_loc + 'AKAM.csv')
    strt, nd = [pd.to_datetime(x).date() for x in [start, end]]
    df.iloc[:, 0] = [pd.to_datetime(x).date() for x in df.iloc[:, 0]]
    df = df[(df.iloc[:, 0] >= strt) & (df.iloc[:, 0] <= nd)]
    dates = df.iloc[:, 0]
    trade_dates = [pd.to_datetime(x).date() for x in trade_date]

    port = Portfolio('Jeff')
    for tick in world:
        hold = Holding(tick, 10000)
        hold.get_df(dat_loc, start, end)
        port.add_holding(hold)

    i = 0
    for d in dates:
        if d in trade_dates:
            for tick in world:
                pos = trades[i]
                port.holdings[tick].trade(d, pos)
            print(port.print_dat(d))
            i += 1


if __name__ == '__main__':
    main()