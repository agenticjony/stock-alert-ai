import requests
from config import FMP_API_KEY

BASE_URL = "https://financialmodelingprep.com/stable"

def get_profile(symbol: str):
    """Fetches key price, market cap, volume, and company overview metrics."""
    url = f"{BASE_URL}/profile?symbol={symbol.upper()}&apikey={FMP_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        if isinstance(data, dict) and "error" in data:
            return None
        return data[0] if data and len(data) > 0 else None
    except Exception:
        return None

def get_financial_ratios(symbol: str):
    """Fetches trailing twelve months (TTM) margins and leverage metrics."""
    url = f"{BASE_URL}/ratios?symbol={symbol.upper()}&apikey={FMP_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return data[0] if data and len(data) > 0 else None
    except Exception:
        return None

def get_financial_growth(symbol: str):
    """Fetches year-over-year revenue and growth performance metrics."""
    url = f"{BASE_URL}/financial-growth?symbol={symbol.upper()}&apikey={FMP_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return data[0] if data and len(data) > 0 else None
    except Exception:
        return None

def get_technical_indicators(symbol: str):
    """Fetches key moving averages (SMA 50, SMA 200) and RSI data."""
    url = f"{BASE_URL}/technical-indicators?symbol={symbol.upper()}&apikey={FMP_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return data[0] if data and len(data) > 0 else None
    except Exception:
        return None

def get_institutional_ownership(symbol: str):
    """Fetches institutional and insider ownership percentages."""
    url = f"{BASE_URL}/institutional-ownership?symbol={symbol.upper()}&apikey={FMP_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return data[0] if data and len(data) > 0 else None
    except Exception:
        return None

def get_company_news(symbol: str, limit: int = 5):
    """Fetches the latest corporate news headlines and summaries for a ticker."""
    url = f"{BASE_URL}/stock_news?symbol={symbol.upper()}&limit={limit}&apikey={FMP_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return data if isinstance(data, list) else []
    except Exception:
        return []