from unittest.mock import AsyncMock

import pytest

from bot import handlers
from bot.database import add_alert, list_user_alerts

TICKER = {"symbol": "BTCUSDT", "price": 65000.0, "change_24h": 2.5, "volume": 1500.0}


@pytest.fixture
def ticker(monkeypatch):
    mock = AsyncMock(return_value=TICKER)
    monkeypatch.setattr(handlers, "get_ticker_price", mock)
    return mock


async def test_start_command_greets_user(make_update, make_context, reply_text):
    update = make_update()

    await handlers.start_command(update, make_context())

    assert "Crypto Alert Bot" in reply_text(update)


async def test_help_command_lists_commands(make_update, make_context, reply_text):
    update = make_update()

    await handlers.help_command(update, make_context())

    text = reply_text(update)
    assert all(command in text for command in ("/price", "/alert", "/alerts", "/remove"))


async def test_price_command_requires_symbol(make_update, make_context, reply_text):
    update = make_update()

    await handlers.price_command(update, make_context())

    assert "Usage: /price" in reply_text(update)


async def test_price_command_shows_ticker(ticker, make_update, make_context, reply_text):
    update = make_update()

    await handlers.price_command(update, make_context("btcusdt"))

    ticker.assert_awaited_once_with("BTCUSDT")
    text = reply_text(update)
    assert "65,000.0000" in text
    assert "📈" in text
    assert "+2.50%" in text


async def test_price_command_shows_negative_change(ticker, make_update, make_context, reply_text):
    ticker.return_value = {**TICKER, "change_24h": -3.0}
    update = make_update()

    await handlers.price_command(update, make_context("BTCUSDT"))

    text = reply_text(update)
    assert "📉" in text
    assert "-3.00%" in text


async def test_price_command_reports_unknown_pair(ticker, make_update, make_context, reply_text):
    ticker.return_value = None
    update = make_update()

    await handlers.price_command(update, make_context("nope"))

    assert "Could not fetch data" in reply_text(update)


async def test_alert_command_validates_argument_count(make_update, make_context, reply_text):
    update = make_update()

    await handlers.alert_command(update, make_context("BTCUSDT", "above"))

    assert "Usage: /alert" in reply_text(update)


async def test_alert_command_validates_direction(ticker, make_update, make_context, reply_text):
    update = make_update()

    await handlers.alert_command(update, make_context("BTCUSDT", "sideways", "70000"))

    assert "Direction must be" in reply_text(update)
    ticker.assert_not_awaited()


async def test_alert_command_validates_price(ticker, make_update, make_context, reply_text):
    update = make_update()

    await handlers.alert_command(update, make_context("BTCUSDT", "above", "abc"))

    assert "Invalid price" in reply_text(update)


async def test_alert_command_rejects_unknown_pair(ticker, make_update, make_context, reply_text):
    ticker.return_value = None
    update = make_update()

    await handlers.alert_command(update, make_context("NOPE", "above", "1"))

    assert "not found" in reply_text(update)
    assert list_user_alerts(1) == []


async def test_alert_command_creates_alert(ticker, make_update, make_context, reply_text):
    update = make_update(user_id=7)

    await handlers.alert_command(update, make_context("btcusdt", "ABOVE", "70000"))

    assert "Alert created" in reply_text(update)
    [alert] = list_user_alerts(7)
    assert (alert.symbol, alert.direction, alert.target_price) == ("BTCUSDT", "above", 70000)


async def test_alerts_command_handles_empty_list(make_update, make_context, reply_text):
    update = make_update()

    await handlers.alerts_command(update, make_context())

    assert "no active alerts" in reply_text(update)


async def test_alerts_command_lists_user_alerts(make_update, make_context, reply_text):
    add_alert(1, "BTCUSDT", "above", 70000)
    add_alert(1, "ETHUSDT", "below", 2000)
    add_alert(2, "BNBUSDT", "above", 600)
    update = make_update(user_id=1)

    await handlers.alerts_command(update, make_context())

    text = reply_text(update)
    assert "BTCUSDT" in text
    assert "ETHUSDT" in text
    assert "BNBUSDT" not in text


async def test_remove_command_requires_id(make_update, make_context, reply_text):
    update = make_update()

    await handlers.remove_command(update, make_context())

    assert "Usage: /remove" in reply_text(update)


async def test_remove_command_validates_id(make_update, make_context, reply_text):
    update = make_update()

    await handlers.remove_command(update, make_context("abc"))

    assert "Invalid ID" in reply_text(update)


async def test_remove_command_removes_alert(make_update, make_context, reply_text):
    alert = add_alert(1, "BTCUSDT", "above", 70000)
    update = make_update(user_id=1)

    await handlers.remove_command(update, make_context(str(alert.id)))

    assert "removed" in reply_text(update)
    assert list_user_alerts(1) == []


async def test_remove_command_rejects_foreign_alert(make_update, make_context, reply_text):
    alert = add_alert(1, "BTCUSDT", "above", 70000)
    update = make_update(user_id=2)

    await handlers.remove_command(update, make_context(str(alert.id)))

    assert "not found" in reply_text(update)
    assert len(list_user_alerts(1)) == 1
