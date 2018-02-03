"""
various methods to support collecting price histories from the Poloniex
JSON API
"""
import datetime as dt
import datetime
import pandas as pd
import os.path

def prompt_for_date_limits(f_dt, l_dt):
    print('oldest data is dated',dt.datetime.strftime(f_dt, '%Y-%m-%d %H:%M:%S'))
    print('latest data is dated',dt.datetime.strftime(l_dt, '%Y-%m-%d %H:%M:%S'))
    in_ll = input("""enter first date in "yyyy,m,d,h,m" format: """)
    print('soorry!  load function not supported yet... try out update! it works...')
    return datetime.datetime(2018,1,1,0,0), datetime.datetime(2018,1,1,0,0)

    #if...

def ticker_data_exists(symbol):
    '''
    Check for existence of CSV file for symbol
    param:      symbol; string
    out ->      bool; file exists
    out ->      string; file path
    '''
    filename = "./CSVs/"+symbol+'.csv'
    return os.path.isfile(filename), filename
    
def update_csv(df_in, symbol, start_date, end_date='9999999999', period=300):
    '''
    Requests latest price history on 'symbol'.
    Accepts current data, appends new data, then overwrites old CSV.
    param:		df_in; pd.dataframe.DataFrame object; data from current CSV
    param: 		symbol; string
    param: 		start_date; string
    [param]:	   end_date; string = '9999999999'
    [param]:    period; int = 300 (seconds)
    out -> 		bool; "operation successful" (file updated)
    '''

    #Get JSON data
    url = get_url(symbol, start_date, end_date, period)
    try:
        df = pd.read_json(url).set_index('date')
    except:
        print('Error processing URL:', url)
        print()
        print('Are you sure that pair exists?')
        return False

    #Append new data and overwrite old CSV
    try:
        filename = "./CSVs/"+symbol+'.csv'
        df_out = df_in.append(df).dropna()
        os.remove(filename)
        df_out.to_csv(filename)
        print('Updated:', symbol)
    except:
        print('Error overwriting',filename)
        return False
    else:
        return True

def date_limits(df):
    '''
    Returns first and last dates in dataframe
    param:      df; pd.dataframe.DataFrame object with ticker history data
    out ->      datetime.DateTime; first date in dataframe
    out ->      datetime.DateTime; last date in dataframe
    '''
    first_date = df['date'][0]
    first_dt = datetime.datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
    
    last_index = (df['date'].size-1)
    last_date = df['date'][last_index]
    last_dt = datetime.datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')

    return first_dt, last_dt
    
def find_next_timestamp(df):
    #Params: symbol; string represents currency pair, e.g. 'BTC_XRP' is
    #        the bitcoin/ripple pair
    #Returns: string; POSIX timestamp that's 5 minutes later than the
    #               newest data in the file.  Intended to be used directly
    #               as the start date for a JSON price history request
    #               from Poloniex
    
    #Get last date from dataframe and add 5 minutes to get next timestamp
    last_index = (df['date'].size-1)
    last_date = (df['date'][last_index])
    last_dt = datetime.datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
    five_min = datetime.timedelta(minutes=5)
    next_dt = last_dt + five_min
        
    #convert next timestamp from datetime.datetime object to POSIX string
    next_dt_posix = posix(next_dt)
    return next_dt_posix

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
    if os.path.isfile("./CSVs/"+symbol+'.csv'):
        print(symbol,'.csv already exists.  Delete file or use update_csv instead.')
        return False
    
    url = get_url(symbol, start_date, end_date, period)
    
    try:
        df = pd.read_json(url)
        df.set_index('date',inplace=True)
        df.to_csv("./CSVs/"+symbol + '.csv')
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