import numpy as np
import pandas as pd

class Stock():
    def __init__(self, price_data):
        self.price_data = price_data

    def annual_volatility(self) -> float:
        closing_prices = pd.Series([float(self.price_data[date]['4. close']) 
                                    for date in self.price_data])
        returns = np.log(closing_prices / closing_prices.shift(1)).dropna()
        
        daily_vol = returns.std()

        annual_vol = daily_vol * np.sqrt(252)

        return annual_vol
    
    def annual_return(self) -> float:
        closing_prices = pd.Series([float(self.price_data[date]['4. close']) 
                                    for date in self.price_data])
        returns = np.log(closing_prices / closing_prices.shift(1)).dropna()
        
        annual_return = returns.mean() * 252

        return annual_return