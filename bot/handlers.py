"""
Handlers dos comandos do bot.
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.binance_client import get_ticker_price
from bot.database import (
    add_alert,
    list_user_alerts,
    deactivate_alert,
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start — mensagem de boas-vindas."""
    await update.message.reply_text(
        "👋 *Olá! Eu sou o Crypto Alert Bot*\n\n"
        "Posso te ajudar a monitorar preços de cripto e receber alertas!\n\n"
        "Digite /help para ver todos os comandos.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help — lista os comandos."""
    help_text = (
        "*📋 Comandos disponíveis:*\n\n"
        "/price `<par>` — Preço atual\n"
        "   _Exemplo: /price BTCUSDT_\n\n"
        "/alert `<par>` `<above|below>` `<preço>` — Criar alerta\n"
        "   _Exemplo: /alert BTCUSDT above 70000_\n\n"
        "/alerts — Listar seus alertas ativos\n\n"
        "/remove `<id>` — Remover alerta\n"
        "   _Exemplo: /remove 3_\n\n"
        "💡 *Pares mais comuns:* BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /price — consulta preço atual."""
    if not context.args:
        await update.message.reply_text(
            "⚠️ Use: /price <par>\nExemplo: /price BTCUSDT"
        )
        return

    symbol = context.args[0].upper()
    data = await get_ticker_price(symbol)

    if not data:
        await update.message.reply_text(
            f"❌ Não consegui obter dados de *{symbol}*.\n"
            "Verifique se o par existe (ex: BTCUSDT, ETHUSDT).",
            parse_mode="Markdown",
        )
        return

    emoji = "📈" if data["change_24h"] >= 0 else "📉"
    sign = "+" if data["change_24h"] >= 0 else ""

    await update.message.reply_text(
        f"💰 *{data['symbol']}*\n\n"
        f"Preço: `${data['price']:,.4f}`\n"
        f"{emoji} 24h: `{sign}{data['change_24h']:.2f}%`\n"
        f"Volume: `{data['volume']:,.0f}`",
        parse_mode="Markdown",
    )


async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /alert — cria novo alerta."""
    if len(context.args) != 3:
        await update.message.reply_text(
            "⚠️ Use: /alert <par> <above|below> <preço>\n"
            "Exemplo: /alert BTCUSDT above 70000"
        )
        return

    symbol, direction, price_str = context.args
    direction = direction.lower()

    if direction not in ("above", "below"):
        await update.message.reply_text(
            "⚠️ Direção deve ser 'above' (acima) ou 'below' (abaixo)"
        )
        return

    try:
        target_price = float(price_str)
    except ValueError:
        await update.message.reply_text("⚠️ Preço inválido")
        return

    # Verificar se o par existe
    data = await get_ticker_price(symbol)
    if not data:
        await update.message.reply_text(f"❌ Par *{symbol.upper()}* não encontrado")
        return

    alert = add_alert(update.effective_user.id, symbol, direction, target_price)
    arrow = "⬆️" if direction == "above" else "⬇️"

    await update.message.reply_text(
        f"✅ *Alerta criado!*\n\n"
        f"ID: `{alert.id}`\n"
        f"{arrow} {alert.symbol} {direction} `${target_price:,.2f}`\n"
        f"Preço atual: `${data['price']:,.2f}`",
        parse_mode="Markdown",
    )


async def alerts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /alerts — lista alertas do usuário."""
    user_alerts = list_user_alerts(update.effective_user.id)

    if not user_alerts:
        await update.message.reply_text(
            "📭 Você não tem alertas ativos.\n\n"
            "Crie um com: /alert BTCUSDT above 70000"
        )
        return

    text = "*📋 Seus alertas ativos:*\n\n"
    for a in user_alerts:
        arrow = "⬆️" if a.direction == "above" else "⬇️"
        text += f"`{a.id}` {arrow} {a.symbol} {a.direction} `${a.target_price:,.2f}`\n"

    text += "\n💡 Use /remove <id> para remover um alerta"
    await update.message.reply_text(text, parse_mode="Markdown")


async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /remove — remove um alerta."""
    if not context.args:
        await update.message.reply_text("⚠️ Use: /remove <id>")
        return

    try:
        alert_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("⚠️ ID inválido")
        return

    success = deactivate_alert(alert_id, update.effective_user.id)
    if success:
        await update.message.reply_text(f"✅ Alerta `{alert_id}` removido.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Alerta `{alert_id}` não encontrado.", parse_mode="Markdown")
