import requests

from library.env import API_KEY

def daily_timeseries(ticker: str) -> dict:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}&outputsize=full&datatype=json'
    r = requests.get(url)
    data = r.json()
    return data