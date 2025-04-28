import numpy as np

import matplotlib.pyplot as plt
from library.stock import Stock
from library.price_data import daily_timeseries
import seaborn as sns

ticker = 'tsla'
data = daily_timeseries(ticker)

stock = Stock(data['Time Series (Daily)'])

annual_vol = stock.annual_volatility(timeframe_years=5)
annual_return = stock.annual_return(timeframe_years=5)

print(f"Annual Return: {annual_return:.2%}")
print(f"Annual Volatility: {annual_vol:.2%}")

S0 = 100              # Initial price
mu = annual_return    # Expected return (annual)
sigma = annual_vol    # Volatility (annual)
T = 5                 # Time in years
steps = 252 * T       # Trading days in a year
dt = 1/252            # Time step (in years)
n = 1000               # Number of simulations

leverage = 2          # Leverage factor

price_paths = np.zeros((n, steps))
price_paths_lev = np.zeros((n, steps))
price_paths[:, 0] = S0
price_paths_lev[:, 0] = S0

for t in range(1, steps):
    z = np.random.normal(0, 1, n)
    price_paths[:, t] = price_paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

for t in range(1, steps):
    z = np.random.normal(0, 1, n)
    price_paths_lev[:, t] = price_paths_lev[:, t-1] * np.exp( leverage * (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

mean_regular = np.mean(price_paths[:, -1])
mean_leveraged = np.mean(price_paths_lev[:, -1])

# Create a figure with subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})

# Plot the price paths on the first subplot
for i in range(n):
    axes[0].plot(price_paths[i], alpha=0.1, color='blue', label='Regular' if i == 0 else "")
    axes[0].plot(price_paths_lev[i], alpha=0.1, color='red', label=f'{leverage}x Leveraged' if i == 0 else "")

# Add labels, title, and legend to the first subplot
axes[0].set_title(f"{ticker} Simulated Price Paths")
axes[0].set_xlabel("Time Steps")
axes[0].set_ylabel("Price")
axes[0].legend(loc="upper left")

# Plot the distribution of final prices on the second subplot
sns.histplot(price_paths[:, -1], bins=50, color='blue', kde=True, label='Regular' if i == 0 else "", ax=axes[1])
sns.histplot(price_paths_lev[:, -1], bins=50, color='red', kde=True, label=f'{leverage}x Leveraged' if i == 0 else "", ax=axes[1])

# Highlight the mean of each distribution
axes[1].axvline(mean_regular, color='blue', linestyle='--', linewidth=2, label=f'Regular Mean: {mean_regular:.2f}' if i == 0 else "")
axes[1].axvline(mean_leveraged, color='red', linestyle='--', linewidth=2, label=f'{leverage}x Leveraged Mean: {mean_leveraged:.2f}' if i == 0 else "")

# Add labels, title, and legend to the second subplot
axes[1].set_title("Distribution of Final Prices")
axes[1].set_xlabel("Final Price")
axes[1].set_ylabel("Frequency")
axes[1].legend(loc="upper right")

# Adjust layout and show the combined figure
plt.tight_layout()
plt.show()