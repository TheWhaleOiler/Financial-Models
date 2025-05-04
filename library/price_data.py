import requests
import json
from library.env import API_KEY

def daily_timeseries(ticker: str, get_cache: bool = True) -> dict:
    _ticker = ticker.lower()

    if(get_cache):
        try:
            with open(f'cache/{_ticker}_daily_time_series.json', 'r') as f:
                data = json.load(f)
                print("loading from cache")
                return data
        except FileNotFoundError:
            pass

    # Issue with Stock split data 
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={_ticker}&apikey={API_KEY}&outputsize=full&datatype=json'
    r = requests.get(url)
    data = r.json()

    if("Information" in data):
        print("API limit reached, please try again later")
        return None

    with open(f'cache/{_ticker}_daily_time_series.json', 'w') as f:
        json.dump(data, f)

    return data