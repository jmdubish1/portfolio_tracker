from port_inventory import *
from indices_list import *
from optimal_port_decisions import *
from tools import *
import pandas as pd
import random
import matplotlib.pyplot as plt
import itertools

dat_loc = 'C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\Alpha_vantage\\port_creator_dat\\' \
          'TIME_SERIES_DAILY_ADJUSTED\\'
# world = random.sample(list(set(sp_500)), 10)
world = list(set(sp_500))
begin_stocks_dict = test_port
total_in_port = 9

start_cash = 1000000
risk_free = .0025
iterations = [40000]

start = pd.to_datetime("2019-09-27").date()
end = pd.to_datetime("2020-09-29").date()

trade_date = ['2019-12-02', '2020-01-06', '2020-02-03', '2020-03-02', '2020-04-06', '2020-05-04',
              '2020-06-01', '2020-07-06', '2020-08-03', '2020-09-25']
trade_dates = [pd.to_datetime(x).date() for x in trade_date]

def main():

    pr = start_profile()

    df = pd.read_csv(dat_loc + 'INTU' + '.csv')
    strt, nd = [pd.to_datetime(x).date() for x in [start, end]]
    df.iloc[:, 0] = [pd.to_datetime(x).date() for x in df.iloc[:, 0]]

    #remove already in port from sample group
    begin_stocks = [k for k, v in begin_stocks_dict.items()]
    tickers = [item for item in world if item not in begin_stocks]

    given_weights = [v for k, v in begin_stocks_dict.items()]

    for tick in list(tickers):
        if not os.path.exists(dat_loc + tick + '.csv'):
            tickers.remove(tick)
            print(tick, 'Not Found')
        else:
            print(tick, 'File Found')

    data_port = Portfolio('data_port')
    print('Loading sample stocks')
    for tick in list(tickers):
        data_port.get_data(tick, dat_loc, start)
        if data_port.holdings[tick].name in data_port.holdings:
            print(tick, 'tick data exists')
            if (len(data_port.holdings[tick].df.index)) <= 600 or \
                    (trade_dates[-1] not in list(data_port.holdings[tick].df.date)):
                tickers.remove(tick)
                print(tick, 'Removed from sample')
        else:
            tickers.remove(tick)

    print('Loading port stocks')
    for tick in begin_stocks:
        data_port.get_data(tick, dat_loc, start)

    tick_combos = itertools.combinations(tickers, total_in_port - len(begin_stocks))
    tick_combos = [i for i in tick_combos]

    full_res_dict = {}
    i = 0
    co = 0

    weight_covs = [*map(lambda x: create_weights_w_allo(total_in_port, x, given_weights), iterations)]

    for combo in tick_combos:

        port = Portfolio('main')
        combo_1 = [c for c in combo]

        for tick in combo_1 + begin_stocks:
            port.add_holding(data_port.holdings[tick])

        for itr in range(0, len(iterations)):
            working_dict = find_optimal_ports(port, combo, weight_covs[itr], begin_stocks, iterations[itr], risk_free)

            # print(working_dict)

            print('Combo: %s/%s Iterations: %s' % (co, len(tick_combos), iterations[itr]))

            dict_list = [[tick, cash] for tick, cash in working_dict.items()]

            for pair in dict_list[0:total_in_port]:
                tick = pair[0]
                allo = pair[1]

                port.holdings[tick].holding_reset()
                port.holdings[tick].cash = allo * start_cash
                port.holdings[tick].allo = round(allo,4)*100
                pos = int(port.holdings[tick].cash/port.holdings[tick].day_close(start))
                port.holdings[tick].trade(start, pos)

            port.print_res(trade_dates[-1])
            res = [port.purse, port.pos_val, port.port_val]

            res_dict = dict(zip(['port_purse', 'port_pos_val', 'port_val'],res))

            new_dict = {**working_dict, **res_dict}
            full_res = [[key, val] for key,val in new_dict.items()]
            temp_dict = {}
            for pair in full_res:
                temp_dict.update({pair[0]: pair[1]})

            full_res_dict[i] = temp_dict

            if co % 1000 == 0:
                save_res_dict(full_res_dict, world, total_in_port)

            i += 1
        co += 1

    save_res_dict(full_res_dict, world, total_in_port)

    # marg_df.to_csv('marg_iter_improv.csv')

    finish_profile(pr, 'main_profile.csv')


if __name__ == '__main__':
    main()