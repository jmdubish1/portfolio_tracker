from datetime import datetime
import datetime as dt
import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import stat
from indices_list import *
import sched,time, threading

symbols = set(sp_500)
market = 'USD'
function = 'TIME_SERIES_DAILY_ADJUSTED'
interval = '5min'
datatype = 'csv'
api_key1 = "TS943WP11EVAK281"
api_key2 = "PUQT1Q2BJJIGP7MR"
api_key = api_key1
data_path = 'C:\\Users\\Jeff\\Documents\\Trading\\Python\\Data\\Alpha_vantage\\S&P_500\\'
api_url = "https://www.alphavantage.co/query"
outputsize = 'full'

columns = {'data', '1. open', '2. high', '3. low',
           '4. close', '5. adjusted close','6. volume'}

'''date', '1. open', '2. high', '3. low', '4. close', '5. adjusted close',
       '6. volume', '7. dividend amount', '8. split coefficient'''

age = 2
wait = 55

def main():

    if not os.path.exists(data_path + function):
        os.mkdir(data_path + function)

    refresh = []
    for symbol in symbols:
        if os.path.exists(data_path + function + '\\' + symbol + '.csv'):
            filestatsobj = os.stat(data_path + function + '\\' + symbol + '.csv')
            modified_time = time.ctime(filestatsobj[stat.ST_MTIME])
            print('File:          ', str(symbol))
            print('Modified Time: ', modified_time)
            time_dif = datetime.now() - pd.to_datetime(modified_time)
            print('File Age:      ', time_dif)
            if time_dif > dt.timedelta(hours=age):
                refresh.append(symbol)
        else:
            refresh.append(symbol)

    i = 0
    missing_downloads = []
    print('Downloading %s Files' % len(refresh))
    while i <= len(refresh) & (len(refresh)-i > 0):
        for symbol in refresh:
            try:
                if function == 'TIME_SERIES_INTRADAY':
                    if not os.path.exists(data_path + function + '\\' + interval):
                        os.mkdir(data_path + function + '\\' + interval)

                    file_to_save = data_path + function + '\\' + interval + '\\' + symbol + '.csv'
                    ts = TimeSeries(key=api_key,
                                    output_format='pandas')
                    data, meta_data = ts.get_intraday(symbol=symbol,
                                                      interval=interval,
                                                      outputsize=outputsize)
                    data['date'] = data.index
                    data.index = list(range(0,len(data.index)))
                    data = data[['date','1. open','2. high','3. low','4. close','5. volume']]

                    if os.path.exists(data_path + function + '\\' + interval + '\\' + symbol + '.csv'):
                        temp_df = pd.read_csv(data_path + function + '\\' + interval + '\\' + symbol + '.csv')
                        temp_df = temp_df[['date','1. open','2. high','3. low','4. close','5. volume']]
                        data = data.append(temp_df)
                        data.drop_duplicates(inplace=True)
                        data = data.sort_index()
                        data.to_csv(file_to_save)
                        print('Data saved to : %s' % file_to_save)

                    else:
                        data.to_csv(file_to_save)
                        print('Data saved to : %s' % file_to_save)

                elif function == 'TIME_SERIES_DAILY_ADJUSTED':
                    file_to_save = data_path + function + '\\' + symbol + '.csv'
                    ts = TimeSeries(key=api_key,
                                    output_format='pandas')
                    data, meta_data = ts.get_daily_adjusted(symbol=symbol,
                                                            outputsize=outputsize)
                    data.to_csv(file_to_save)
                    print('Data saved to : %s' % file_to_save)

                elif function == 'DIGITAL_CURRENCY_DAILY':
                    file_to_save = data_path + function + '\\' + symbol + '.csv'
                    cc = CryptoCurrencies(key=api_key2, output_format='pandas')
                    data, meta_data = cc.get_digital_currency_daily(symbol = symbols,
                                                                    market=market)
                    data.to_csv(file_to_save)
                    print('Data saved to : %s' % file_to_save)

                else:
                    print('Edit Code for new data')


                i += 1
                if i == len(refresh):
                    pass
                if (i % 5 == 0):
                    print('Waiting %s seconds' % wait)
                    print('%s Completed, %s Remain' % (i, (len(refresh)) - i))
                    print(str(datetime.now()))
                    print('Approximately %s Minutes Until Complete' % str(round((len(refresh)-i)/5*wait/60,1)))
                    time.sleep(wait)
                else:
                    pass

            except ValueError:
                print(str(symbol), ' Not Found')
                missing_downloads.append(symbol)
            except KeyError:
                print('Keyerror, waiting %s seconds' % '10')
                time.sleep(10)

    print('Download Complete')
    print('Missing Symbols: ', missing_downloads)

    names, df_list, missing = [],[],[]
    for symbol in symbols:
        names.append(symbol)
        try:
            n = pd.read_csv(data_path + function + '\\' + symbol +'.csv')
            df_list.append(n)
        except FileNotFoundError:
            print(str(symbol),' is missing.')
            missing.append(symbol)

    names.sort()
    print(names, 'Loaded')
    print(missing, 'Missing')

    tickers = []
    for x, y in zip(names, df_list):
        globals()[x] = y
        tickers.append(globals()[x])

    missing_downloads = pd.DataFrame(missing_downloads)
    missing_downloads.to_csv(data_path + function + '\\' + 'missing.csv')


if __name__ == '__main__':
    main()