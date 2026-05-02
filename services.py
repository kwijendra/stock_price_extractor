import os
import requests


def fetch_alpha_vantage_data(symbol: str):
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract the "Monthly Time Series" data
    return data.get("Monthly Time Series", {})