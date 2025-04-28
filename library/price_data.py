import requests
import json
from library.env import API_KEY

def daily_timeseries(ticker: str, get_cache: bool = True) -> dict:

    if(get_cache):
        try:
            with open(f'cache/{ticker}_daily_time_series.json', 'r') as f:
                data = json.load(f)
                print("loading from cache")
                return data
        except FileNotFoundError:
            pass

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}&outputsize=full&datatype=json'
    r = requests.get(url)
    data = r.json()

    with open(f'cache/{ticker}_daily_time_series.json', 'w') as f:
        json.dump(data, f)

    return data