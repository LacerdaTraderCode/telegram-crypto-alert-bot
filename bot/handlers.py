from telegram import Update
from telegram.ext import ContextTypes

from bot.binance_client import get_ticker_price
from bot.database import add_alert, deactivate_alert, list_user_alerts


def direction_arrow(direction: str) -> str:
    return "⬆️" if direction == "above" else "⬇️"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Hi! I'm the Crypto Alert Bot*\n\n"
        "I can help you track crypto prices and receive alerts.\n\n"
        "Type /help to see all commands.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "*📋 Available commands:*\n\n"
        "/price `<pair>` — Current price\n"
        "   _Example: /price BTCUSDT_\n\n"
        "/alert `<pair>` `<above|below>` `<price>` — Create an alert\n"
        "   _Example: /alert BTCUSDT above 70000_\n\n"
        "/alerts — List your active alerts\n\n"
        "/remove `<id>` — Remove an alert\n"
        "   _Example: /remove 3_\n\n"
        "💡 *Common pairs:* BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "⚠️ Usage: /price <pair>\nExample: /price BTCUSDT",
        )
        return

    symbol = context.args[0].upper()
    data = await get_ticker_price(symbol)

    if not data:
        await update.message.reply_text(
            f"❌ Could not fetch data for *{symbol}*.\n"
            "Check that the pair exists (e.g. BTCUSDT, ETHUSDT).",
            parse_mode="Markdown",
        )
        return

    emoji = "📈" if data["change_24h"] >= 0 else "📉"
    sign = "+" if data["change_24h"] >= 0 else ""

    await update.message.reply_text(
        f"💰 *{data['symbol']}*\n\n"
        f"Price: `${data['price']:,.4f}`\n"
        f"{emoji} 24h: `{sign}{data['change_24h']:.2f}%`\n"
        f"Volume: `{data['volume']:,.0f}`",
        parse_mode="Markdown",
    )


async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text(
            "⚠️ Usage: /alert <pair> <above|below> <price>\nExample: /alert BTCUSDT above 70000",
        )
        return

    symbol, direction, price_str = context.args
    direction = direction.lower()

    if direction not in ("above", "below"):
        await update.message.reply_text(
            "⚠️ Direction must be 'above' or 'below'",
        )
        return

    try:
        target_price = float(price_str)
    except ValueError:
        await update.message.reply_text("⚠️ Invalid price")
        return

    data = await get_ticker_price(symbol)
    if not data:
        await update.message.reply_text(
            f"❌ Pair *{symbol.upper()}* not found",
            parse_mode="Markdown",
        )
        return

    alert = add_alert(update.effective_user.id, symbol, direction, target_price)

    await update.message.reply_text(
        f"✅ *Alert created!*\n\n"
        f"ID: `{alert.id}`\n"
        f"{direction_arrow(direction)} {alert.symbol} {direction} `${target_price:,.2f}`\n"
        f"Current price: `${data['price']:,.2f}`",
        parse_mode="Markdown",
    )


async def alerts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_alerts = list_user_alerts(update.effective_user.id)

    if not user_alerts:
        await update.message.reply_text(
            "📭 You have no active alerts.\n\nCreate one with: /alert BTCUSDT above 70000",
        )
        return

    text = "*📋 Your active alerts:*\n\n"
    for alert in user_alerts:
        arrow = direction_arrow(alert.direction)
        text += f"`{alert.id}` {arrow} {alert.symbol} {alert.direction} `${alert.target_price:,.2f}`\n"

    text += "\n💡 Use /remove <id> to remove an alert"
    await update.message.reply_text(text, parse_mode="Markdown")


async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /remove <id>")
        return

    try:
        alert_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("⚠️ Invalid ID")
        return

    if deactivate_alert(alert_id, update.effective_user.id):
        await update.message.reply_text(
            f"✅ Alert `{alert_id}` removed.",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"❌ Alert `{alert_id}` not found.",
            parse_mode="Markdown",
        )
