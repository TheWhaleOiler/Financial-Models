import numpy as np

import matplotlib.pyplot as plt
from library.stock import Stock
from library.price_data import daily_timeseries
import seaborn as sns

########################################
# Monte Carlo Simulation of Stock Prices
# Leveraged vs Regular
########################################

ticker = 'spy'
data = daily_timeseries(ticker,get_cache=True)

stock = Stock(data['Time Series (Daily)'])

######################################
# PARAMETERS
years = 23            # Time in years
annual_return = stock.annualized_return(timeframe_years=years) 
annual_vol    = stock.annualized_volatility(timeframe_years=years)


S0 = 100              # Initial price
mu = annual_return    # Expected return (annual)
sigma = annual_vol    # Volatility (annual)
steps = 252 * years   # Trading days in a year
dt = 1/252            # Time step (in years)
n = 5000              # Number of simulations
leverage = 3          # Leverage factor

# END PARAMETERS
#######################################

print(f" Annual Return: {annual_return:.2%}")
print(f" Annual Volatility: {annual_vol:.2%}")

price_paths = np.zeros((n, steps))
price_paths_lev = np.zeros((n, steps))
price_paths[:, 0] = S0
price_paths_lev[:, 0] = S0


for t in range(1, steps):

    mu_geom_daily = np.log(1 + mu) * dt
    sigma_daily = sigma / np.sqrt(252)
    mu_daily = mu_geom_daily + 0.5 * sigma_daily**2

    daily_return = np.random.normal(mu_daily, sigma_daily, n)

    # Discard any returns <= -1 
    daily_return = np.clip(daily_return, -0.999999, None)
    leveraged_daily_return = np.clip(daily_return * leverage, -0.999999, None)

    price_paths[:, t] = price_paths[:, t-1] * (1 + daily_return)
    price_paths_lev[:, t] = price_paths_lev[:, t-1] * (1 + leveraged_daily_return)


geometric_means_regular = (price_paths[:, -1] / price_paths[:, 0]) ** (1 / years) - 1
geometric_means_leveraged = (price_paths_lev[:, -1] / price_paths_lev[:, 0]) ** (1 / years) - 1

log_mean_regular = np.exp(np.mean(np.log(price_paths[:, -1])))
log_mean_leveraged = np.exp(np.mean(np.log(price_paths_lev[:, -1])))

log_returns = np.log(price_paths[:, 1:] / price_paths[:, :-1])
log_returns_lev = np.log(price_paths_lev[:, 1:] / price_paths_lev[:, :-1])

daily_vols = np.std(log_returns, axis=1)
daily_vols_lev = np.std(log_returns_lev, axis=1)

annualized_vols = daily_vols * np.sqrt(252)
annualized_vols_lev = daily_vols_lev * np.sqrt(252)

med_vol = np.median(annualized_vols)
med_vol_lev = np.median(annualized_vols_lev)


median_geometric_mean_regular = np.median(geometric_means_regular)
median_geometric_mean_leveraged = np.median(geometric_means_leveraged)

median_regular = np.median(price_paths[:, -1])
median_leveraged = np.median(price_paths_lev[:, -1])

print(f" Mean Price (Regular): {np.mean(price_paths[:, -1]):.2f}")
print(f" Mean Price ({leverage}x Leveraged): {np.mean(price_paths_lev[:, -1]):.2f}")

regular_calculated_geometric_return = mu - 0.5 * sigma**2
leverage_calculated_geometric_return = leverage*mu - 0.5 * (leverage * sigma)**2

print()
print(f" Log Average Price (Regular): {log_mean_regular:.2f}")
print(f" Log Average Price ({leverage}x Leveraged): {log_mean_leveraged:.2f}")
print()
print(f" Annualized Median Volatility (Regular): {med_vol:.2%}")
print(f" Annualized Median Volatility ({leverage}x Leveraged): {med_vol_lev:.2%}")
print(f" Annualized Median Geometric Return (Regular): {median_geometric_mean_regular:.2%}")
print(f" Annualized Median Geometric Return ({leverage}x Leveraged): {median_geometric_mean_leveraged:.2%}")

print(f" Theoretical Geometric Return: {regular_calculated_geometric_return:.2%}")
print(f" Theoretical Geometric Return ({leverage}x Leveraged): {leverage_calculated_geometric_return:.2%}")


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
axes[1].set_xscale('log')
sns.histplot(price_paths[:, -1], bins=50, color='blue', kde=True, label='Regular' if i == 0 else "", ax=axes[1])
sns.histplot(price_paths_lev[:, -1], bins=50, color='red', kde=True, label=f'{leverage}x Leveraged' if i == 0 else "", ax=axes[1])


# Highlight the mean of each distribution
axes[1].axvline(log_mean_regular, color='blue', linestyle='-', linewidth=2, label=f'Regular Log Mean: {log_mean_regular:.2f}')
axes[1].axvline(median_regular, color='blue', linestyle='--', linewidth=2, label=f'Regular Median: {median_regular:.2f}')
axes[1].axvline(log_mean_leveraged, color='red', linestyle='-', linewidth=2, label=f'{leverage}x Leveraged Log Mean: {log_mean_leveraged:.2f}')
axes[1].axvline(median_leveraged, color='red', linestyle='--', linewidth=2, label=f'{leverage}x Leveraged Median: {median_leveraged:.2f}')

# Add labels, title, and legend to the second subplot
axes[1].set_title("Distribution of Final Prices")
axes[1].set_xlabel("Final Price")
axes[1].set_ylabel("Frequency")
axes[1].legend(loc="upper right")

# Adjust layout and show the combined figure
plt.tight_layout()
plt.show()