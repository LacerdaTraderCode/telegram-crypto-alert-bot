"""
Monitor que roda em background verificando os alertas periodicamente.
"""
import os
import asyncio
import logging

from dotenv import load_dotenv

from bot.binance_client import get_price_only
from bot.database import list_all_active_alerts, trigger_alert

load_dotenv()

logger = logging.getLogger(__name__)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))


async def check_alerts(bot):
    """Verifica todos os alertas ativos e dispara os que atingiram a meta."""
    alerts = list_all_active_alerts()
    if not alerts:
        return

    # Agrupar por symbol para fazer menos chamadas à API
    symbols = set(a.symbol for a in alerts)
    prices = {}
    for symbol in symbols:
        price = await get_price_only(symbol)
        if price is not None:
            prices[symbol] = price

    # Verificar cada alerta
    for alert in alerts:
        current_price = prices.get(alert.symbol)
        if current_price is None:
            continue

        triggered = False
        if alert.direction == "above" and current_price >= alert.target_price:
            triggered = True
        elif alert.direction == "below" and current_price <= alert.target_price:
            triggered = True

        if triggered:
            arrow = "⬆️" if alert.direction == "above" else "⬇️"
            try:
                await bot.send_message(
                    chat_id=alert.user_id,
                    text=(
                        f"🚨 *ALERTA DISPARADO!*\n\n"
                        f"{arrow} *{alert.symbol}* atingiu `${current_price:,.4f}`\n"
                        f"Sua meta era: `${alert.target_price:,.4f}` ({alert.direction})"
                    ),
                    parse_mode="Markdown",
                )
                trigger_alert(alert.id)
                logger.info(f"Alerta {alert.id} disparado para user {alert.user_id}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta {alert.id}: {e}")


async def start_monitor(bot):
    """Loop infinito de monitoramento."""
    logger.info(f"Monitor iniciado (intervalo: {CHECK_INTERVAL}s)")
    while True:
        try:
            await check_alerts(bot)
        except Exception as e:
            logger.error(f"Erro no monitor: {e}")
        await asyncio.sleep(CHECK_INTERVAL)
