from port_inventory import *
from indices_list import *
from optimal_port_decisions import *
import pandas as pd
import random
import matplotlib.pyplot as plt
import itertools
import cProfile, pstats, io

dat_loc = 'C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\Alpha_vantage\\S&P_500\\' \
          'TIME_SERIES_DAILY_ADJUSTED\\'
world = test_40

begin_stocks = ['AMD', 'LNT', 'JEF', 'WMT', 'BBY', 'CDNS', 'KMI']
total_in_port = 9
start_cash = 200000
risk_free = .0025
iterations = [30000]
iter_of_iters = 10

start = pd.to_datetime("2019-09-03").date()
end = pd.to_datetime("2020-09-01").date()

trade_date = ['2019-12-02', '2020-01-06', '2020-02-03', '2020-03-02', '2020-04-06', '2020-05-04',
              '2020-06-01', '2020-07-06', '2020-08-03', '2020-09-25']
trade_dates = [pd.to_datetime(x).date() for x in trade_date]

def main():

    pr = cProfile.Profile()
    pr.enable()

    df = pd.read_csv(dat_loc + 'AKAM.csv')
    strt, nd = [pd.to_datetime(x).date() for x in [start, end]]
    df.iloc[:, 0] = [pd.to_datetime(x).date() for x in df.iloc[:, 0]]

    #remove already in port from sample group
    tickers = [item for item in world if item not in begin_stocks]
    for tick in tickers:
        if not os.path.exists(dat_loc + tick + '.csv'):
            tickers.remove(tick)
        else:
            print(tick, 'file found')

    marg_improv_iterations = []
    data_port = Portfolio('data_port')
    for tick in tickers + begin_stocks:
        data_port.get_data(tick, dat_loc, start)

    tick_combos = itertools.combinations(tickers, total_in_port - len(begin_stocks))
    tick_combos = [i for i in tick_combos]
    print(len(tick_combos))

    full_res_dict = []
    i = 0
    co = 1
    for combo in tick_combos:
        port = Portfolio('main')
        combo_1 = [c for c in combo]
        for tick in combo_1 + begin_stocks:
            t_hold = Holding(tick, 0)
            port.add_holding(t_hold)
            port.holdings[tick] = data_port.holdings[tick]

        for iteration in iterations:
            for i in range(0, iter_of_iters):

                working_dict = find_optimal_ports(port, combo, total_in_port,
                                                  begin_stocks, iteration, risk_free)

                print(working_dict)

                print('Combo: %s/%s Iterations: %s, Trial: %s' % (co, len(tick_combos), iteration, i))

                dict_list = [(tick, cash) for tick, cash in working_dict.items()]

                for pair in dict_list[0:total_in_port]:
                    tick = pair[0]
                    allo = pair[1]

                    port.holdings[tick].holding_reset()
                    port.holdings[tick].cash = allo * start_cash
                    port.holdings[tick].allo = round(allo,4)*100
                    pos = int(port.holdings[tick].cash/port.holdings[tick].day_close(start))
                    port.holdings[tick].trade(start, pos)

                res = [port.purse, port.pos_val, port.port_val]

                res_dict = dict(zip(['port_purse', 'port_pos_val', 'port_val'],res))

                new_dict = {**working_dict, **res_dict}
                full_res = [[key, val] for key,val in new_dict.items()]
                full_res_dict.append([i, full_res])

                port.print_res(trade_dates[-1])
                i += 1
                marg_improv_iterations.append([iteration, port.pos_val, port.port_val])
        co += 1

    dat_df = pd.DataFrame(full_res_dict)
    dat_df.to_csv('res_df.csv')

    marg_df = pd.DataFrame(marg_improv_iterations, columns = ['iterations', 'pos_val', 'port_val'])
    marg_df.to_csv('marg_iter_improv.csv')

    pr.disable()

    result = io.StringIO()
    pstats.Stats(pr, stream=result).print_stats()
    result = result.getvalue()
    # chop the string into a csv-like buffer
    result = 'ncalls' + result.split('ncalls')[-1]
    result = '\n'.join([','.join(line.rstrip().split(None, 5)) for line in result.split('\n')])
    # save it to disk

    with open('main_profile.csv', 'w+') as f:
        # f=open(result.rsplit('.')[0]+'.csv','w')
        f.write(result)
        f.close()

if __name__ == '__main__':
    main()