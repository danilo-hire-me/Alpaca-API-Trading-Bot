
import numpy as np
import pandas as pd

class SMAStrategy:
    def __init__(self, df, fast_sma=30, slow_sma=60, cost_ind=0.0001):
        self.df = df.copy()
        self.fast_sma = fast_sma
        self.slow_sma = slow_sma
        self.cost_ind = cost_ind

    def apply_strategy(self):
        self.df["SMA fast"] = self.df["close"].rolling(self.fast_sma).mean()
        self.df["SMA slow"] = self.df["close"].rolling(self.slow_sma).mean()
        self.df["signal"] = np.nan

        condition_buy = (self.df["SMA fast"] > self.df["SMA slow"]) & \
                       (self.df["SMA fast"].shift(1) < self.df["SMA slow"].shift(1))
        condition_sell = (self.df["SMA fast"] < self.df["SMA slow"]) & \
                        (self.df["SMA fast"].shift(1) > self.df["SMA slow"].shift(1))

        self.df.loc[condition_buy, "signal"] = 1
        self.df.loc[condition_sell, "signal"] = -1

        self.df["position"] = self.df["signal"].fillna(method="ffill")
        self.df["cost"] = (np.abs(self.df["signal"]) * self.cost_ind).fillna(0)
        self.df["pct"] = self.df["close"].pct_change(1)
        self.df["return"] = (self.df["pct"] * self.df["position"].shift(1) - self.df["cost"]) * 100

        return self.df
