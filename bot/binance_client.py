import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com")
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=10)


async def _fetch_json(path: str, symbol: str) -> dict | None:
    url = f"{BINANCE_API_URL}{path}"
    try:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.get(url, params={"symbol": symbol.upper()}) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except (aiohttp.ClientError, TimeoutError):
        return None


async def get_ticker_price(symbol: str) -> dict | None:
    data = await _fetch_json("/api/v3/ticker/24hr", symbol)
    if data is None:
        return None
    try:
        return {
            "symbol": data["symbol"],
            "price": float(data["lastPrice"]),
            "change_24h": float(data["priceChangePercent"]),
            "volume": float(data["volume"]),
        }
    except (KeyError, TypeError, ValueError):
        return None


async def get_price_only(symbol: str) -> float | None:
    data = await _fetch_json("/api/v3/ticker/price", symbol)
    if data is None:
        return None
    try:
        return float(data["price"])
    except (KeyError, TypeError, ValueError):
        return None
