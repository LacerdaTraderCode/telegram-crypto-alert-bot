import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from bot import monitor
from bot.database import add_alert, list_all_active_alerts


@pytest.fixture
def telegram_bot():
    bot = MagicMock()
    bot.send_message = AsyncMock()
    return bot


@pytest.fixture
def prices(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr(monitor, "get_price_only", mock)
    return mock


@pytest.mark.parametrize(
    ("direction", "target", "current", "expected"),
    [
        ("above", 100, 100, True),
        ("above", 100, 99.9, False),
        ("below", 100, 100, True),
        ("below", 100, 100.1, False),
        ("sideways", 100, 100, False),
    ],
)
def test_is_triggered(direction, target, current, expected):
    assert monitor.is_triggered(direction, target, current) is expected


async def test_check_alerts_without_alerts_skips_price_lookup(telegram_bot, prices):
    await monitor.check_alerts(telegram_bot)

    prices.assert_not_awaited()
    telegram_bot.send_message.assert_not_awaited()


async def test_check_alerts_notifies_and_deactivates_triggered_alert(telegram_bot, prices):
    add_alert(42, "BTCUSDT", "above", 70000)
    prices.return_value = 71000.0

    await monitor.check_alerts(telegram_bot)

    telegram_bot.send_message.assert_awaited_once()
    assert telegram_bot.send_message.await_args.kwargs["chat_id"] == 42
    assert list_all_active_alerts() == []


async def test_check_alerts_keeps_alert_below_threshold(telegram_bot, prices):
    add_alert(1, "BTCUSDT", "above", 70000)
    prices.return_value = 69000.0

    await monitor.check_alerts(telegram_bot)

    telegram_bot.send_message.assert_not_awaited()
    assert len(list_all_active_alerts()) == 1


async def test_check_alerts_skips_symbols_without_price(telegram_bot, prices):
    add_alert(1, "BTCUSDT", "above", 1)
    prices.return_value = None

    await monitor.check_alerts(telegram_bot)

    telegram_bot.send_message.assert_not_awaited()
    assert len(list_all_active_alerts()) == 1


async def test_check_alerts_fetches_each_symbol_once(telegram_bot, prices):
    add_alert(1, "BTCUSDT", "above", 1)
    add_alert(2, "BTCUSDT", "below", 999999)
    prices.return_value = 100.0

    await monitor.check_alerts(telegram_bot)

    prices.assert_awaited_once_with("BTCUSDT")
    assert telegram_bot.send_message.await_count == 2


async def test_check_alerts_keeps_alert_active_when_delivery_fails(telegram_bot, prices):
    add_alert(1, "BTCUSDT", "above", 1)
    prices.return_value = 100.0
    telegram_bot.send_message.side_effect = RuntimeError("telegram down")

    await monitor.check_alerts(telegram_bot)

    assert len(list_all_active_alerts()) == 1


async def test_start_monitor_survives_check_failures(monkeypatch, telegram_bot):
    check = AsyncMock(side_effect=RuntimeError("boom"))
    sleep = AsyncMock(side_effect=[None, asyncio.CancelledError()])
    monkeypatch.setattr(monitor, "check_alerts", check)
    monkeypatch.setattr(monitor.asyncio, "sleep", sleep)

    with pytest.raises(asyncio.CancelledError):
        await monitor.start_monitor(telegram_bot)

    assert check.await_count == 2
