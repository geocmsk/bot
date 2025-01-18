import ccxt
import time
from config.settings import API_KEY, SECRET_KEY, PASSPHRASE
from src.trading_strategy import check_buy_sell_signal

def initialize_api():
    exchange = ccxt.okx({
        'apiKey': API_KEY,
        'secret': SECRET_KEY,
        'password': PASSPHRASE
    })
    return exchange

def get_balance(exchange):
    balance = exchange.fetch_balance()
    return balance['total']['USDT']  # USDT bakiyesi örneği

def execute_trade(exchange, action, symbol='BTC/USDT', amount=0.1):
    if action == 'BUY':
        exchange.create_market_buy_order(symbol, amount)
    elif action == 'SELL':
        exchange.create_market_sell_order(symbol, amount)

def main():
    exchange = initialize_api()
    symbol = 'BTC/USDT'  # işlem yapılacak pariteyi buradan seçebilirsin
    amount = 0.1  # Alım-satım için belirleyeceğin miktar

    while True:
        balance = get_balance(exchange)
        print(f'Balance: {balance} USDT')
        
        # Veriyi al
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='4h')  # 4 saatlik grafik
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Al-Sat sinyalini kontrol et
        signal = check_buy_sell_signal(df)
        print(f'Signal: {signal}')
        
        # İşlemi gerçekleştir
        if signal == 'BUY':
            execute_trade(exchange, 'BUY', symbol, amount)
        elif signal == 'SELL':
            execute_trade(exchange, 'SELL', symbol, amount)
        
        time.sleep(60 * 60 * 4)  # 4 saat bekle

if __name__ == '__main__':
    main()
