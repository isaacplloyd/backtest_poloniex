import datetime

from poloniex import dl_history, get_tickers, posix


def main():
    cmd = str()
    #Endless loop reads user input and executes selected function
    while cmd.lower() != 'exit':    
        cmd = input('cmd: ')
        
        #dl price history CSV(s) to current directory
        if cmd.lower() == 'download':
            #Set start date to 20 weeks ago (140 days)
            now = datetime.datetime.utcnow()
            history_length = datetime.timedelta(140)
            start_date = posix(
                    datetime.datetime(now.year, now.month, now.day, tzinfo=None)
                    - history_length)
            
            #Get tickers and download histories
            ticker_symbol_list = get_tickers()
            for symbol in ticker_symbol_list:
                dl_history(symbol, start_date)
            print('download(s) complete!')
        
        #Update CSVs in program directory
        elif cmd.lower() == 'update':
            
            print('coming soon...')
            
        else:
            print('cmd not recognized')

if __name__ == "__main__":
    main()