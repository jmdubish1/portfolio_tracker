import numpy as np
import random
import pandas as pd
from port_inventory import *
import itertools
import cProfile, pstats, io
from numba import njit, jit
import gc, os
import matplotlib.pyplot as plt


#Slow
def make_ret_mat(port, tickers):
    day_ret_mat = []
    ann_rets = []
    for tick in tickers:
        day_ret_mat.append(np.array(port.holdings[tick].daily_ret)[1:]*100)
        ann_rets.append(get_ann_ret(port.holdings[tick].daily_ret))

    day_ret_mat = np.array(day_ret_mat)
    ann_rets = np.array(ann_rets).transpose()
    
    return day_ret_mat, ann_rets


def get_ann_ret(ret_list):
    ret_list = [x+1 for x in ret_list]
    ret = np.nanprod(ret_list)-1
    return ret*100


def weight_cov(weights):
    return [weights, np.outer(weights, weights)]


def create_weights(num_in_port, iters):
    weights = []
    l, h = [1, 2]
    for i in range(0, int(iters * .8)):
        group_1 = [random.uniform(0, 1) for x in range(0, num_in_port)]
        weights.append([group_1[x] / sum(group_1) for x in range(0, len(group_1))])
    for i in range(int(iters * .8), int(iters * .9)):
        group_2 = [random.uniform(l, h) for x in [1]] + [random.uniform(0, 1) for x in range(0, num_in_port - 1)]
        weights.append([group_2[x] / sum(group_2) for x in range(0, len(group_2))])
    for i in range(int(iters * .9), int(iters)):
        group_3 = [random.uniform(l, h) for x in [1, 2]] + [random.uniform(0, 1) for x in range(0, num_in_port - 2)]
        weights.append([group_3[x] / sum(group_3) for x in range(0, len(group_3))])

    weights = np.array([np.array(l) for l in weights])

    return [*map(weight_cov, weights)]


def create_weights_w_allo(num_in_port, iters, given_weights):
    allos = []
    for g in range(0, len(given_weights)):
        if given_weights[g] > 0:
            allos.append([g, given_weights[g]])

    num_in_port -= len(allos)
    weights = []
    l, h = [1, 2]
    for i in range(0, int(iters * .8)):
        group_1 = [random.uniform(0, 1) for x in range(0, num_in_port)]
        weights.append([group_1[x]/sum(group_1) for x in range(0, len(group_1))])
    for i in range(int(iters * .8), int(iters * .9)):
        group_2 = [random.uniform(l, h) for x in [1]] + [random.uniform(0, 1) for x in range(0, num_in_port - 1)]
        weights.append([group_2[x]/sum(group_2) for x in range(0, len(group_2))])
    for i in range(int(iters * .9), int(iters)):
        group_3 = [random.uniform(l, h) for x in [1, 2]] + [random.uniform(0, 1) for x in range(0, num_in_port - 2)]
        weights.append([group_3[x]/sum(group_3) for x in range(0, len(group_3))])

    w_allo = []
    for wts in weights:
        for al in allos:
            wts.insert(*al)
        w_sum = sum(wts)
        w_allo.append([w/w_sum for w in wts])

    weights = np.array([np.array(l) for l in w_allo])

    return [*map(weight_cov, weights)]


def weight_cov_mat(weight_cov, cov_mat):
    return np.matmul(weight_cov, cov_mat)


def get_slope(exp_ret, std, risk_free):
    return (exp_ret-risk_free)/std


def find_best_slope(slope_list, iterations):
    slopes = [x[3] for x in slope_list]
    high = np.unique(slopes)[int(iterations*.999)]
    max_s = [x for x in range(0, len(slopes)) if slopes[x] == high]
    return slope_list[max_s[0]]


def create_port_dict(tickers, best_weights):
    labels = tickers + ['exp_ret', 'std_dev']
    weights = [i for i in best_weights[0]]
    port_data = weights + best_weights[1:]
    port_dict = dict(zip(labels, port_data))

    return port_dict


def find_optimal_ports(port, combo, weight_cov, begin_stocks, iterations, risk_free):
    ##create all combinations of world of tickers
    print(combo)
    select_ticks = [i for i in combo]
    tickers = begin_stocks + select_ticks
    day_ret_mat, ann_rets = make_ret_mat(port, tickers)

    '''from a list of beginning stocks, 
    find those stocks with the closest to zero from abs correlation values'''

    cov_mat = np.cov(day_ret_mat)
    data_result = []
    for wts in weight_cov:
        ##multiply weights by ret for expected return
        ##possibly assign randomly multiple times in order to maximize computing efficiency
        exp_ret = np.dot(np.array(wts[0]), ann_rets)

        # find port variance
        w_cov_mat = weight_cov_mat(wts[1], cov_mat)
        port_var = np.sqrt(np.sum(w_cov_mat))*np.sqrt(len(day_ret_mat))
        slope = get_slope(exp_ret, port_var, risk_free)
        data = [wts[0], exp_ret, port_var, slope]
        data_result.append(data)

    best_wts = find_best_slope(data_result, iterations)
    port_dict = create_port_dict(tickers, best_wts)

    return port_dict
