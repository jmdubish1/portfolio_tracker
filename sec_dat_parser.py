import numpy as np
import random
from optimal_port_decisions import *
from indices_list import *
import itertools
import csv
import time
import pandas as pd
import os


def find_cik(cik_df, ticker):
    return list(cik_df[cik_df.iloc[:, 1] == ticker].CIK)[0]


def read_txt(file):
    with open(file, 'r') as file_r:
        reader = csv.reader(file_r, delimiter="\t")
        return list(reader)


def find_compy_report(sub_dat, comp_cik, report):
    '''returns adsh'''

    for line in sub_dat:
        if (line[1] == str(comp_cik)) and (line[25] == report):
            return line[0]


def find_report_dat(num_dat, adsh, year_qrts, qtr_date):
    report = []
    for line in num_dat:
        if (line[0] == adsh) and (line[4] == year_qrts.get(qtr_date)):
            report.append(line)
    return report


qtrly_dat = 'C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\Quarterly_data\\'

cik_dat = qtrly_dat + 'cik_ticker.csv'
tickers = set(sp_500 + sp_600)

periods = ['2020q1', '2020q2', '2018q1', '2018q2', '2018q3',
           '2018q4', '2016q1', '2016q2', '2016q3', '2016q4']

def main():

    csv.field_size_limit(100000000)
    cik_df = pd.read_csv(cik_dat)

    for period in periods:
        print(period)
        year_sub = qtrly_dat + period + '\\' + 'sub.txt'
        year_num = qtrly_dat + period + '\\' + 'num.txt'

        try:
            sub_d = read_txt(year_sub)
            num_d = read_txt(year_num)

            for tick in tickers:
                print(period, tick)
                try:
                    cik = find_cik(cik_df, tick)
                    adsh = find_compy_report(sub_d, cik, '10-Q')

                    report = []
                    for line in num_d:
                        if (line[0] == adsh):
                            report.append(line)
                    file = qtrly_dat + 'stock_data\\' + tick + '_qrtly.txt'
                    with open(file, 'a') as file_a:
                        for line in report:
                            file_a.write('\n %s' % line)
                        file_a.close()
                        print('appended')

                except:
                    print('cik not found')

        finally:
            if (type(year_sub) is not str) or (type(year_num) is not str):
                year_sub.close()
                year_num.close()


if __name__ == '__main__':
    main()