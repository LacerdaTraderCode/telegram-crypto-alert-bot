import asyncio
import logging
import os

from dotenv import load_dotenv

from bot.binance_client import get_price_only
from bot.database import list_all_active_alerts, trigger_alert
from bot.handlers import direction_arrow

load_dotenv()

logger = logging.getLogger(__name__)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))


def is_triggered(direction: str, target_price: float, current_price: float) -> bool:
    if direction == "above":
        return current_price >= target_price
    return direction == "below" and current_price <= target_price


async def check_alerts(bot):
    alerts = list_all_active_alerts()
    if not alerts:
        return

    prices = {}
    for symbol in {alert.symbol for alert in alerts}:
        price = await get_price_only(symbol)
        if price is not None:
            prices[symbol] = price

    for alert in alerts:
        current_price = prices.get(alert.symbol)
        if current_price is None:
            continue
        if not is_triggered(alert.direction, alert.target_price, current_price):
            continue

        try:
            await bot.send_message(
                chat_id=alert.user_id,
                text=(
                    "🚨 *ALERT TRIGGERED!*\n\n"
                    f"{direction_arrow(alert.direction)} *{alert.symbol}* "
                    f"reached `${current_price:,.4f}`\n"
                    f"Your target was: `${alert.target_price:,.4f}` ({alert.direction})"
                ),
                parse_mode="Markdown",
            )
            trigger_alert(alert.id)
            logger.info(f"Alert {alert.id} triggered for user {alert.user_id}")
        except Exception as e:
            logger.error(f"Failed to send alert {alert.id}: {e}")


async def start_monitor(bot):
    logger.info(f"Monitor started (interval: {CHECK_INTERVAL}s)")
    while True:
        try:
            await check_alerts(bot)
        except Exception as e:
            logger.error(f"Monitor error: {e}")
        await asyncio.sleep(CHECK_INTERVAL)
