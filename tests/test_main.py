from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from bot import main as bot_main

TOKEN = "123456:TEST-TOKEN"


def test_build_application_registers_every_command():
    application = bot_main.build_application(TOKEN)

    registered = {
        command
        for handlers in application.handlers.values()
        for handler in handlers
        for command in handler.commands
    }
    assert registered == set(bot_main.COMMANDS)


async def test_post_init_starts_monitor_task(monkeypatch):
    monitor = AsyncMock()
    monkeypatch.setattr(bot_main, "start_monitor", monitor)
    application = SimpleNamespace(bot="telegram-bot", bot_data={})

    await bot_main.post_init(application)
    await application.bot_data["monitor_task"]

    monitor.assert_awaited_once_with("telegram-bot")


def test_main_requires_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        bot_main.main()


def test_main_initializes_database_and_starts_polling(monkeypatch):
    application = MagicMock()
    init_db = MagicMock()
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", TOKEN)
    monkeypatch.setattr(bot_main, "init_db", init_db)
    monkeypatch.setattr(bot_main, "build_application", MagicMock(return_value=application))

    bot_main.main()

    init_db.assert_called_once_with()
    application.run_polling.assert_called_once_with()
