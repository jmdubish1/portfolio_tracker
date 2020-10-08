import cProfile, pstats, io
from optimal_port_decisions import *
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def start_profile():
    pr = cProfile.Profile()
    pr.enable()
    return pr


def finish_profile(pr, output_name):
    pr.disable()

    result = io.StringIO()
    pstats.Stats(pr, stream=result).print_stats()
    result = result.getvalue()
    # chop the string into a csv-like buffer
    result = 'ncalls' + result.split('ncalls')[-1]
    result = '\n'.join([','.join(line.rstrip().split(None, 5)) for line in result.split('\n')])
    # save it to disk

    with open(str(output_name), 'w+') as f:
        f.write(result)
        f.close()


def save_res_dict(full_res_dict, world, total_in_port):
    with open('res_df' + '_' + str(len(world)) + '_' + str(total_in_port) + '.json', 'w') as fp:
        json.dump(full_res_dict, fp)
    fp.close()


def parse_res_dict(dat_loc, json_res, risk_free, gspc_list, plot=False):
    with open(dat_loc + json_res + '.json', 'r') as fp:
        data = json.load(fp)

    ret_sharp = []
    df_list = []
    for i in range(0, len(data)):
        work_dict = data[str(i)]
        work_dict['sharpe'] = (work_dict['exp_ret'] - risk_free)/work_dict['std_dev']
        r_s = [i, work_dict['exp_ret'], work_dict['std_dev'],
               work_dict['sharpe'], work_dict['port_val']]
        keys = [[k for k, v in work_dict.items()]]
        values = [v for k, v in work_dict.items()]
        key_val = keys + values
        df_list.append(key_val)
        ret_sharp.append(r_s)

    df = pd.DataFrame(df_list, columns=['stocks', 'stock_1', 'stock_2', 'stock_3', 'stock_4',
                                        'stock_5','stock_6', 'stock_7', 'stock_8', 'stock_9',
                                        'exp_ret', 'std_dev', 'port_purse', 'port_pos_val', 'port_val', 'sharpe'])
    df.to_csv(dat_loc + json_res + '.csv', index=False)

    print(len(df.index))
    print(df.head())

    if plot:
        ret, _, sharpe = gspc_list

        x = np.array([i[3] for i in ret_sharp])
        y = np.array([i[4] for i in ret_sharp])

        plt.scatter(x, y)
        plt.scatter(sharpe, ret, c='red')
        plt.xlabel('Sharpe')
        plt.ylabel('Expected Return')
        plt.show()


def prep_gspc_df(dat_loc, risk_free, start, end):
    gspc_df = pd.read_csv(dat_loc + '^GSPC.csv', usecols=['Date', 'Adj Close'])
    gspc_df.Date = [pd.to_datetime(x).date() for x in gspc_df.Date]
    gspc_df = gspc_df[(gspc_df.Date >= start) & (gspc_df.Date <= end)]
    rets = gspc_df.iloc[:, 1]
    rets = np.log(rets) - np.log(rets).shift(1)
    ret = get_ann_ret(rets)/100
    std = np.std(rets)*np.sqrt(len(rets))
    sharpe = (ret - risk_free)/std
    return [ret, std, sharpe]
