import datetime as dt
import pandas as pd

from poloniex import dl_history, get_tickers, posix
from poloniex import update_csv, find_next_timestamp
from poloniex import ticker_data_exists, prompt_for_date_limits



def main():
    cmd = str()
    #Endless loop reads user input and executes selected function
    while cmd.lower() != 'exit':    
        cmd = input('cmd: ')
        
        #dl price history CSV(s) to "./CSVs"
        if cmd.lower() == 'download':
            #Set start date to 20 weeks ago (140 days)
            now = dt.datetime.utcnow()
            history_length = dt.timedelta(140)
            start_date = posix(
                    dt.datetime(now.year, now.month, now.day, tzinfo=None)
                    - history_length)
            
            #Get tickers and download histories
            ticker_symbol_list = get_tickers()
            for symbol in ticker_symbol_list:
                dl_history(symbol, start_date)
            print('download(s) complete!')
        
        #Update CSVs in "./CSVs"
        elif cmd.lower() == 'update':
            ticker_symbol_list = get_tickers()
            for symbol in ticker_symbol_list:
                filename = "./CSVs/"+symbol+'.csv'
                df = pd.read_csv(filename)
                start_date = find_next_timestamp(df)
                df.set_index('date',inplace=True)
                update_csv(df, symbol, start_date)

        #Load a dataframe with CSV ticker data from a given time range
        elif cmd.lower() == 'load':
            symbol = input('ticker symbol: ')
            exists, path = ticker_data_exists(symbol)
            if exists:
                df = pd.read_csv(path)
                f_dt, l_dt = date_limits(df)
                lower_lim, upper_lim = prompt_for_date_limits(f_dt, l_dt)
                #open_df = get_data_range(path, '...')
            else:
                print("./CSVs/"+symbol+'.csv not found.')
        elif cmd.lower() != 'exit':
            print('cmd not recognized')

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    