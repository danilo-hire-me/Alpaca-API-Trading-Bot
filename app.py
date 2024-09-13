import os
from alpaca_trade_api.rest import REST, TimeFrame
from flask import Flask, render_template, request
from main import SMAStrategy, fetch_data  # Import your strategy and data function
#dee392e9-834e-4d70-aefc-e80cdad7f3a6 my alpaca info delete before github
from dotenv import load_dotenv  # Import dotenv

load_dotenv()

#after downloading and signing up with alpaca, get your api and secret keys and replace them here
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
alpaca_base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

app = Flask(__name__)

# Initialize Alpaca API with environment variables
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
alpaca_base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

api = REST(alpaca_api_key, alpaca_secret_key, alpaca_base_url, api_version='v2')

@app.route('/')
def index():
    return render_template('index.html')  # Create a simple HTML form

@app.route('/trade', methods=['POST'])
def trade():
    symbol = request.form['symbol']
    fast_sma = int(request.form['fast_sma'])
    slow_sma = int(request.form['slow_sma'])
    trade_mode = request.form['trade_mode']  # 'paper' or 'real'

    # Fetch market data
    df = fetch_data(symbol)

    # Apply the strategy
    strategy = SMAStrategy(df, fast_sma=fast_sma, slow_sma=slow_sma)
    df_strategy = strategy.apply_strategy()

    if trade_mode == 'paper':
        # Simulate paper trading
        global paper_trading_balance
        paper_trading_balance = simulate_trades(df_strategy, paper_trading_balance)
        result_message = f"Paper Trading: Balance = ${paper_trading_balance:.2f}"
    else:
        # Real trading via Alpaca
        result_message = execute_real_trades(symbol, df_strategy)

    return render_template('result.html', message=result_message)

def simulate_trades(df, balance):
    for _, row in df.iterrows():
        if row['signal'] == 1:  # Buy signal
            balance -= row['close']
        elif row['signal'] == -1:  # Sell signal
            balance += row['close']
    return balance

def execute_real_trades(symbol, df):
    try:
        for _, row in df.iterrows():
            if row['signal'] == 1:  # Buy signal
                # Place a buy order via Alpaca API
                api.submit_order(
                    symbol=symbol,
                    qty=1,  # Number of shares/units
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
            elif row['signal'] == -1:  # Sell signal
                # Place a sell order via Alpaca API
                api.submit_order(
                    symbol=symbol,
                    qty=1,  # Number of shares/units
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
        return f"Real trading executed for {symbol}!"
    except Exception as e:
        return f"Error during real trading: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)




