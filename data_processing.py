# data_preprocessing.py
import yfinance as yf
import pandas as pd

class DataPreprocessor:
    def __init__(self, symbol):
        self.symbol = symbol
        self.df = None

    def fetch_data(symbol="EURUSD=X"):
        df = yf.download(symbol, period="max").dropna()  # Fetching maximum period data
        df.columns = ["open", "high", "low", "close", "adj close", "volume"]
        df.index.name = "time"
        del df["adj close"]
        return df
