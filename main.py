import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Data Preprocessing Function
def fetch_data(symbol="EURUSD=X"):
    df = yf.download(symbol).dropna()
    df.columns = ["open", "high", "low", "close", "adj close", "volume"]
    df.index.name = "time"
    del df["adj close"]
    return df

# Simple Moving Average Strategy Class
class SMAStrategy:
    def __init__(self, df, fast_sma=30, slow_sma=60, cost_ind=0.0001):
        self.df = df
        self.fast_sma = fast_sma
        self.slow_sma = slow_sma
        self.cost_ind = cost_ind

    def apply_strategy(self):
        df = self.df.copy()

        # Create SMAs
        df["SMA fast"] = df["close"].rolling(self.fast_sma).mean()
        df["SMA slow"] = df["close"].rolling(self.slow_sma).mean()

        # Create signals
        df["signal"] = np.nan
        condition_buy = (df["SMA fast"] > df["SMA slow"]) & (df["SMA fast"].shift(1) < df["SMA slow"].shift(1))
        condition_sell = (df["SMA fast"] < df["SMA slow"]) & (df["SMA fast"].shift(1) > df["SMA slow"].shift(1))
        df.loc[condition_buy, "signal"] = 1
        df.loc[condition_sell, "signal"] = -1

        # Position
        df["position"] = df["signal"].fillna(method="ffill")

        # Cost and returns
        df["cost"] = (np.abs(df["signal"]) * self.cost_ind).fillna(value=0)
        df["pct"] = df["close"].pct_change(1)
        df["return"] = (df["pct"] * df["position"].shift(1) - df["cost"]) * 100

        return df

# Visualization Functions
def plot_signals(df, symbol):
    # Get latest signals
    idx_buy = df[df["signal"] == 1].index
    idx_sell = df[df["signal"] == -1].index

    plt.figure(figsize=(15, 8))
    plt.scatter(idx_buy, df.loc[idx_buy]["close"], color="#57CE95", marker="^", label="Buy")
    plt.scatter(idx_sell, df.loc[idx_sell]["close"], color="red", marker="v", label="Sell")
    plt.plot(df["close"], alpha=0.35, label=symbol)
    plt.plot(df["SMA fast"], alpha=0.35)
    plt.plot(df["SMA slow"], alpha=0.35)
    plt.legend()
    plt.show()


def plot_cumulative_return(df, title, ylabel="P&L in %"):
    df["return"].cumsum().plot(figsize=(15, 8), title=title, ylabel=ylabel)
    plt.show()

# Main Function
def main():
    symbol = "EURUSD=X"

    # Data Preprocessing
    df = fetch_data(symbol)

    # Apply SMA Strategy
    strategy = SMAStrategy(df, fast_sma=30, slow_sma=60, cost_ind=0.0001)
    df_strategy = strategy.apply_strategy()

    # Visualization
    plot_signals(df_strategy, symbol)
    plot_cumulative_return(df_strategy, "Cumulative Return for the Trend Trading Strategy on EURUSD")

    # Example for BTC-USD
    df_btc = fetch_data("BTC-USD")
    btc_strategy = SMAStrategy(df_btc, fast_sma=30, slow_sma=60, cost_ind=0.001)
    df_btc_strategy = btc_strategy.apply_strategy()
    plot_cumulative_return(df_btc_strategy, "Cumulative Return for the Trend Trading Strategy on BTC-USD")

if __name__ == "__main__":
    main()







