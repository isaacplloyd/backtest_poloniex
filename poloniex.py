"""
various methods to support collecting price histories from the Poloniex
JSON API
"""
import datetime
import pandas as pd
import os.path

def dl_history(symbol, start_date, end_date='9999999999', period=300,):
    '''
    Sends a JSON request to Poloniex for price history of given ticker
    symbol.  Formats and saves the response as a CSV.
    Param: symbol; string of trade pair, e.g. 'USDT_ETH'
    Param: start_date; string POSIX timestamp
    [Param]: end_date; string POSIX timestamp default='9999999999'
    [Param]: period; int resolution of data, in seconds. default=300
        valid values: 300, 900, 1800, 7200, 14400, and 86400
    Returns: bool True if data is pulled and successfully written
    '''
    if os.path.isfile(symbol+'.csv'):
        print(symbol,'.csv already exists.  Delete file or use update_csv instead.')
        return False
    
    url = get_url(symbol, start_date, end_date, period)
    
    try:
        df = pd.read_json(url)
        df.set_index('date',inplace=True)
        df.to_csv(symbol + '.csv')
        print('Processed:',symbol)
    except:
        print('Error processing URL:',url)
        print()
        print('Are you sure that pair exists?')
        return False
    else:
        return True

def get_tickers():
    '''
    Gets a list of trading pairs of interest
    Returns -> string[] list of trading pairs, e.g. ['USDT_BTC', 'USDT_ETH']
    '''
    return ['USDT_BTC','USDT_ETH','USDT_XRP','USDT_STR','USDT_XMR',
               'USDT_LTC','USDT_DASH','BTC_ETH','BTC_XRP','BTC_STR',
               'BTC_XMR','BTC_BTS','BTC_LTC','BTC_DOGE','BTC_DASH',
               'BTC_FCT','BTC_MAID','BTC_CLAM']

def posix(timestamp):
    '''
    Converts a datetime object to a POSIX timestamp string
    Param: timestamp; datetime.datetime with no timezone (naive)
    Returns -> string; timestamp converted to posix
    '''
    unix_zero_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=None)
    time_delta = timestamp - unix_zero_time
    time_delta_s = time_delta.total_seconds()
    posix_str = str(int(time_delta_s))
    return posix_str

def get_url(symbol, start_date, end_date, period):
    '''
    Formats a Poloniex price history JSON request for given ticker/time
    Param: symbol; string ticker trading pair e.g. "USDT_BTC"
    Param: start_date; string POSIX timestamp
    Param: end_date; string POSIX timestamp
    Param: period; int resolution of data, in seconds
    Returns -> string; formatted JSON request to send
    '''
    url = 'https://poloniex.com/public?command=returnChartData'
    url += '&currencyPair=' + symbol
    url += '&end=' + end_date
    url += '&period=' + str(period)
    url += '&start=' + start_date
    return url





if __name__ == "__main__":
    print("this module is not the main program.")
    print("run 'main.py' instead")