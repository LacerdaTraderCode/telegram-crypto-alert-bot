import aiohttp
import pytest

from bot import binance_client


class FakeResponse:
    def __init__(self, status=200, payload=None):
        self.status = status
        self._payload = payload if payload is not None else {}

    async def json(self):
        return self._payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.requests = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    def get(self, url, params=None):
        self.requests.append((url, params))
        if self.error:
            raise self.error
        return self.response


@pytest.fixture
def install_session(monkeypatch):
    def _install(response=None, error=None):
        session = FakeSession(response, error)
        monkeypatch.setattr(binance_client.aiohttp, "ClientSession", lambda **kwargs: session)
        return session

    return _install


TICKER_PAYLOAD = {
    "symbol": "BTCUSDT",
    "lastPrice": "65000.50",
    "priceChangePercent": "-1.25",
    "volume": "1234.5",
}


async def test_get_ticker_price_parses_response(install_session):
    session = install_session(FakeResponse(payload=TICKER_PAYLOAD))

    result = await binance_client.get_ticker_price("btcusdt")

    assert result == {
        "symbol": "BTCUSDT",
        "price": 65000.50,
        "change_24h": -1.25,
        "volume": 1234.5,
    }
    url, params = session.requests[0]
    assert url.endswith("/api/v3/ticker/24hr")
    assert params == {"symbol": "BTCUSDT"}


async def test_get_ticker_price_returns_none_on_http_error(install_session):
    install_session(FakeResponse(status=400))

    assert await binance_client.get_ticker_price("INVALID") is None


@pytest.mark.parametrize("error", [aiohttp.ClientError(), TimeoutError()])
async def test_get_ticker_price_returns_none_on_network_failure(install_session, error):
    install_session(error=error)

    assert await binance_client.get_ticker_price("BTCUSDT") is None


async def test_get_ticker_price_returns_none_on_malformed_payload(install_session):
    install_session(FakeResponse(payload={"symbol": "BTCUSDT"}))

    assert await binance_client.get_ticker_price("BTCUSDT") is None


async def test_get_price_only_parses_response(install_session):
    session = install_session(FakeResponse(payload={"symbol": "BTCUSDT", "price": "65000.10"}))

    assert await binance_client.get_price_only("BTCUSDT") == 65000.10
    assert session.requests[0][0].endswith("/api/v3/ticker/price")


async def test_get_price_only_returns_none_on_http_error(install_session):
    install_session(FakeResponse(status=500))

    assert await binance_client.get_price_only("BTCUSDT") is None


async def test_get_price_only_returns_none_on_malformed_payload(install_session):
    install_session(FakeResponse(payload={"price": "not-a-number"}))

    assert await binance_client.get_price_only("BTCUSDT") is None
