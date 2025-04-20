import numpy as np
import pandas as pd

class Stock():
    def __init__(self, price_data):
        self.price_data = price_data

    def annual_volatility(self, timeframe_years=1) -> float:
        closing_prices = pd.Series([float(self.price_data[date]['4. close']) 
                                    for date in self.price_data])
        
        closing_prices = closing_prices.iloc[:252 * timeframe_years]

        returns = np.log(closing_prices / closing_prices.shift(1)).dropna()
        
        daily_vol = returns.std()

        annual_vol = daily_vol * np.sqrt(252)

        return annual_vol
    
    def annual_return(self, timeframe_years=1) -> float:
        closing_prices = pd.Series([float(self.price_data[date]['4. close']) 
                                    for date in self.price_data])

        closing_prices = closing_prices.iloc[:252 * timeframe_years]

        total_return = (closing_prices.iloc[0] / closing_prices.iloc[-1]) - 1

        num_years = (len(closing_prices) / 252)  # Assuming 252 trading days per year

        annualized_return = (1 + total_return) ** (1 / num_years) - 1

        return annualized_return