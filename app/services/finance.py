import pandas as pd
from yfinance import Ticker
from requests.exceptions import HTTPError

class Finance:

    def __init__(self, ticker: str, period: str = "1y", interval: str = "1d"):
        self.ticker = ticker
        self.period = period
        self.interval = interval

    def __get_history(self) -> pd.DataFrame:
        result = Ticker(ticker=self.ticker).history(period=self.period, interval=self.interval) 
        return result
    
    def __calc_rsi(self, delta: pd.Series, period: int = 14) -> float:
        #Calculating gains and losses
        gain = delta.copy()
        loss = delta.copy()
        gain[gain < 0] = 0
        loss[loss > 0] = 0
        loss = loss.abs()

        #Calculating exponential moving averages of gains and losses
        avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
        avg_loss = loss.ewm(com=period - 1, adjust=False).mean()

        #Calculating Relative Strength (RS)
        rs = avg_gain / avg_loss

        #Calculating RSI
        temp = 100 - (100 / (1 + rs))

        #Returning the last RSI value
        return float(temp.iloc[-1])

    def __calc_statistics(self) -> dict:
        data = self.__get_history()

        #Calculating daily returns and adding it as a new column to the DataFrame
        data["Return"] = data["Close"].pct_change()

        #Calculating daily difference in closing prices and adding it as a new column to the DataFrame
        data["Difference"] = data["Close"].diff()

        #Creating all statistics
        avg_return = data["Return"].mean()
        median_return = data["Return"].median()
        cumulative_return = (data["Return"] + 1).prod() - 1
        max_price = data["Close"].max()
        min_price = data["Close"].min()
        avg_price = data["Close"].mean()
        median_price = data["Close"].median()
        current_price = data["Close"].iloc[-1]
        volatility = data["Close"].std()
        last_rsi = self.__calc_rsi(delta=data["Difference"])        

        return {
            "avg_return": avg_return,
            "median_return": median_return,
            "cumulative_return": cumulative_return,
            "max_price": max_price,
            "min_price": min_price,
            "avg_price": avg_price,
            "median_price": median_price,
            "current_price": current_price,
            "volatility": volatility,
            "last_rsi": last_rsi
        }
    
    def get_report(self) -> str:
        stats = self.__calc_statistics()

        return f"""
Stock Statistics for {self.ticker}:
Average Daily Return: {stats.get('avg_return', 'N/A'):.4f}
Median Daily Return: {stats.get('median_return', 'N/A'):.4f}
Cumulative Return: {stats.get('cumulative_return', 'N/A'):.4f}
Maximum Closing Price: ${stats.get('max_price', 'N/A'):.2f}
Minimum Closing Price: ${stats.get('min_price', 'N/A'):.2f}
Average Closing Price: ${stats.get('avg_price', 'N/A'):.2f}
Median Closing Price: ${stats.get('median_price', 'N/A'):.2f}
Current Closing Price: ${stats.get('current_price', 'N/A'):.2f}
Volatility: ${stats.get('volatility', 'N/A'):.2f}
Last RSI Value: {stats.get('last_rsi', 'N/A'):.2f}
"""