# Trading Bot with Flask and Alpaca API

This project is a Python-based trading bot that implements a Simple Moving Average (SMA) strategy. It features a Flask web interface where users can configure trading parameters, choose between real and paper trading modes, and view results. The bot integrates with the Alpaca API for live trading, allowing automated execution of buy and sell orders based on the SMA strategy.

## Features
- Web Interface: Built with Flask for easy configuration of trading parameters (e.g., asset symbol, fast and slow SMAs).
- Simple Moving Average (SMA) trading strategy.
- Trading Modes: Supports both paper trading (simulated trades) and real trading using the Alpaca API.
- Real-time market data and order execution.
- Alpaca Integration: Connects with the Alpaca API for real-time trading and order execution.

## Installation

  1. Clone this repository:
```bash
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot
```
 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
 3. Set up your environment variables for Alpaca API by creating a .env file in the project root:
```bash
touch .env
```
 4. Add the following lines to your .env file:
```bash
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```
 5.  Run the Flask app:
```bash
python app.py
```
 6. Open your browser and go to
```bash
http://127.0.0.1:5000/
```

## Configurations
 - Fast SMA: Sets the period for the fast-moving average.
 - Slow SMA: Sets the period for the slow-moving average.
 - Symbol: Input the symbol for the asset to trade (e.g., EURUSD=X, BTC-USD).
 - Trade Mode: Choose between paper trading and real trading.

## Usage
 - Open the web interface.
 - Input the asset symbol and SMA parameters.
 - Choose between paper or real trading.
 - Click "Start Trading" to execute the strategy.

## Dependencies
 - Flask
 - Alpaca Trade API
 - dotenv
 - yfinance
 - pandas
Install all dependencies via the requirements.txt file.

