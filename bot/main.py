"""
Telegram Crypto Alert Bot - Ponto de entrada da aplicação.
"""
import os
import logging
import asyncio

from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

from bot.handlers import (
    start_command,
    help_command,
    price_command,
    alert_command,
    alerts_command,
    remove_command,
)
from bot.database import init_db
from bot.monitor import start_monitor

load_dotenv()

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Inicializa e executa o bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN não configurado no .env")

    # Inicializar banco
    init_db()

    # Criar aplicação
    app = Application.builder().token(token).build()

    # Registrar handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("alert", alert_command))
    app.add_handler(CommandHandler("alerts", alerts_command))
    app.add_handler(CommandHandler("remove", remove_command))

    # Iniciar monitor em background
    async def post_init(application):
        asyncio.create_task(start_monitor(application.bot))

    app.post_init = post_init

    logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
    app.run_polling()


if __name__ == "__main__":
    main()
