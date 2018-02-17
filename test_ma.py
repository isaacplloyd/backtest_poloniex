import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def test_ma(df):
    '''
    Test a simple moving avg trading strategy and return performance vs market
    param:      df; pd.DataFrame containing crypto data range to test with
    out ->      float market performance
    out ->      float strategy performance
    '''
    lead = int(input('lead lookback period: '))
    lag = int(input('lag lookback period: '))
    pc_thresh = float(input('percent threshold (dec): '))
    ma_df = df.copy()
    ma_df['lead'] = ma_df['close'].rolling(lead).mean()
    ma_df['lag'] = ma_df['close'].rolling(lag).mean()
    ma_df['lead-lag'] = ma_df['lead']-ma_df['lag']
    ma_df['pc_diff'] = ma_df['lead-lag']/ma_df['close']
    ma_df['regime'] = np.where(ma_df['pc_diff'] > pc_thresh, 1, 0)
    ma_df['regime'] = np.where(ma_df['pc_diff'] < -pc_thresh, -1, ma_df['regime'])
    ma_df['Market'] = np.log(ma_df['close'] / ma_df['close'].shift(1))
    ma_df['Strategy'] = ma_df['regime'].shift(1) * ma_df['Market']
    ma_df[['Market','Strategy']] = ma_df[['Market','Strategy']].cumsum().apply(np.exp)