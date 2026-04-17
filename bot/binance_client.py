"""
Cliente assíncrono para a API pública da Binance.
"""
import os
import aiohttp
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com")


async def get_ticker_price(symbol: str) -> Optional[dict]:
    """
    Obtém preço atual e variação 24h de um par.
    
    Args:
        symbol: Par de trading (ex: 'BTCUSDT')
    
    Returns:
        Dict com 'price' e 'change_24h' ou None se não encontrado.
    """
    symbol = symbol.upper()
    url = f"{BINANCE_API_URL}/api/v3/ticker/24hr"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params={"symbol": symbol}, timeout=10) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return {
                    "symbol": data["symbol"],
                    "price": float(data["lastPrice"]),
                    "change_24h": float(data["priceChangePercent"]),
                    "volume": float(data["volume"]),
                }
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None


async def get_price_only(symbol: str) -> Optional[float]:
    """Versão rápida que retorna apenas o preço (usado pelo monitor)."""
    symbol = symbol.upper()
    url = f"{BINANCE_API_URL}/api/v3/ticker/price"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params={"symbol": symbol}, timeout=5) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return float(data["price"])
        except Exception:
            return None


import asyncio  # noqa: E402
