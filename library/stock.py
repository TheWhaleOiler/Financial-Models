import numpy as np
import pandas as pd

class CandleStick():
    def __init__(self, date, open_price, high_price, low_price, close_price):
        self.date = date
        self.open_price = float(open_price)
        self.high_price = float(high_price)
        self.low_price = float(low_price)
        self.close_price = float(close_price)
    
    def __repr__(self):
        return f"CandleStick(date={self.date}, open_price={self.open_price}, high_price={self.high_price}, low_price={self.low_price}, close_price={self.close_price})"
    
    def __truediv__(self, other):
        if isinstance(other, CandleStick):
            return CandleStick(self.date, self.open_price / other.open_price, self.high_price / other.high_price, self.low_price / other.low_price, self.close_price / other.close_price)
        else:
            return CandleStick(self.date, self.open_price / other, self.high_price / other, self.low_price / other, self.close_price / other)

class Stock():
    def __init__(self, price_data):
        self.price_data = price_data

    def annualized_volatility(self, timeframe_years=1) -> float:
        prices = pd.Series([CandleStick(date,
                                        self.price_data[date]['1. open'],
                                        self.price_data[date]['2. high'],
                                        self.price_data[date]['3. low'],
                                        self.price_data[date]['4. close']
                                            ) 
                            for date in self.price_data])
        
        if(len(prices) < 252 * timeframe_years):
            raise ValueError(f"Not enough data for {timeframe_years} years. Available data: {len(prices) / 252:.2f} years.")

        prices = prices.iloc[:252 * timeframe_years]

        gross_return = pd.Series([candle.close_price for candle in (prices / prices.shift(1)).dropna() ])

        returns = np.log(gross_return)
        
        daily_vol = returns.std()

        annual_vol = daily_vol * np.sqrt(252)

        return annual_vol
    
    def annualized_return(self, timeframe_years=1) -> float:
        prices = pd.Series([CandleStick(date,
                                        self.price_data[date]['1. open'],
                                        self.price_data[date]['2. high'],
                                        self.price_data[date]['3. low'],
                                        self.price_data[date]['4. close']
                                            ) 
                            for date in self.price_data])
        
        if(len(prices) < 252 * timeframe_years):
            raise ValueError(f"Not enough data for {timeframe_years} years. Available data: {len(prices) / 252:.2f} years.")

        prices = prices.iloc[:252 * timeframe_years]

        start_price = prices.iloc[-1].close_price
        end_price = prices.iloc[0].close_price

        total_return = ( (end_price - start_price) / start_price ) + 1

        annualized_return = total_return ** (1/timeframe_years) - 1

        return annualized_return