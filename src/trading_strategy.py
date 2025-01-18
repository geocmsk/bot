import ccxt
import pandas as pd

def get_williams_r(df, period=90):
    highest_high = df['high'].rolling(window=period).max()
    lowest_low = df['low'].rolling(window=period).min()
    williams_r = -100 * ((highest_high - df['close']) / (highest_high - lowest_low))
    return williams_r

def check_buy_sell_signal(df):
    williams_r = get_williams_r(df)
    
    # Strateji: Williams %R < -97 AL, Williams %R > -5 SAT
    if williams_r.iloc[-1] < -97:
        return 'BUY'
    elif williams_r.iloc[-1] > -5:
        return 'SELL'
    else:
        return 'HOLD'
