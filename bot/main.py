import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from bot.database import init_db
from bot.handlers import (
    alert_command,
    alerts_command,
    help_command,
    price_command,
    remove_command,
    start_command,
)
from bot.monitor import start_monitor

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

COMMANDS = {
    "start": start_command,
    "help": help_command,
    "price": price_command,
    "alert": alert_command,
    "alerts": alerts_command,
    "remove": remove_command,
}


async def post_init(application):
    application.bot_data["monitor_task"] = asyncio.create_task(start_monitor(application.bot))


def build_application(token: str) -> Application:
    application = Application.builder().token(token).post_init(post_init).build()
    for name, callback in COMMANDS.items():
        application.add_handler(CommandHandler(name, callback))
    return application


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    init_db()
    application = build_application(token)
    logger.info("Bot started. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
