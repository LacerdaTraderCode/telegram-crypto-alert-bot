<div align="center">

# 🤖 Telegram Crypto Alert Bot

**A Telegram bot that monitors cryptocurrency prices and sends real-time alerts**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Binance](https://img.shields.io/badge/Binance-FCD535?logo=binance&logoColor=black)](https://binance-docs.github.io/apidocs/)
[![License](https://img.shields.io/badge/License-MIT-orange)](https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github)](https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot)
[![Unofficial](https://img.shields.io/badge/Bot-Unofficial-red)](https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot)

</div>

---

## 📌 About the Project

A Telegram bot that monitors cryptocurrency prices in real time via the **Binance API** and sends customized alerts when prices hit the thresholds set by the user. Built with `python-telegram-bot` on a fully asynchronous architecture.

> ⚠️ **Unofficial** project — not affiliated with Telegram or Binance. It independently uses Binance's public API and Telegram's bot API.

### Features

- ✅ **Real-time price lookup** for any crypto pair (BTC/USDT, ETH/USDT, etc.)
- ✅ **Above/below price alerts** with a user-defined value
- ✅ **List of active alerts** per user
- ✅ **Asynchronous background monitoring**
- ✅ **SQLite persistence** — alerts survive restarts
- ✅ **Automatic rate limiting** respecting Binance API limits

---

## 🛠️ Technologies

- **python-telegram-bot** — Official framework for Telegram bots
- **aiohttp** — Asynchronous HTTP client for the Binance API
- **SQLAlchemy** — ORM for alert persistence
- **asyncio** — Native asynchronous programming
- **APScheduler** — Scheduling of periodic monitoring jobs

---

## 📁 Structure

```
telegram-crypto-alert-bot/
├── bot/
│   ├── main.py              # Entry point
│   ├── handlers.py          # Command handlers
│   ├── binance_client.py    # Binance API client
│   ├── database.py          # Alert persistence
│   └── monitor.py           # Background monitoring job
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- Telegram bot token — [create one via @BotFather](https://t.me/BotFather)

### Steps

```bash
git clone https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot.git
cd telegram-crypto-alert-bot

python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN

python -m bot.main
```

---

## 💬 Available Commands

| Command | Description | Example |
|---------|-----------|---------|
| `/start` | Welcome message | `/start` |
| `/help` | Lists all commands | `/help` |
| `/price <pair>` | Current price of the pair | `/price BTCUSDT` |
| `/alert <pair> <above\|below> <value>` | Creates an alert | `/alert BTCUSDT above 70000` |
| `/alerts` | Lists active alerts | `/alerts` |
| `/remove <id>` | Removes an alert by ID | `/remove 3` |

---

## 🖼️ Usage Example

```
User: /price BTCUSDT
Bot: 💰 BTCUSDT: $67,432.50 (+2.15% in 24h)

User: /alert BTCUSDT above 70000
Bot: ✅ Alert created! I'll notify you when BTCUSDT passes $70,000

[when the price rises...]
Bot: 🚨 ALERT! BTCUSDT reached $70,150 — your target was $70,000
```

---

## 🔒 Security

- ✅ Bot token is never committed (kept in `.env`)
- ✅ Each user only sees their own alerts
- ✅ Rate limiting prevents Binance API abuse
- ✅ Error handling on all asynchronous operations

---

## 🚀 24/7 Deploy

- **VPS** — DigitalOcean, Linode, Contabo
- **Railway** or **Render** — free tier available
- **Raspberry Pi** — ideal for personal use

---

## ✅ Requirements

- Python **3.11** or higher
- Telegram bot token

---

## 👤 Author

<div align="center">

**Wagner Lacerda** — Senior Software Engineer | Python, Backend, AI Apps, Automation & Systems

[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github&logoColor=white)](https://github.com/LacerdaTraderCode)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wagner%20Lacerda-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/wagner-lacerda-da-silva-958b9481)
[![YouTube](https://img.shields.io/badge/YouTube-LacerdaTraderCode-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@LacerdaTraderCode)
[![Telegram](https://img.shields.io/badge/Telegram-LacerdaTraderCode-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode)
[![Telegram Bots](https://img.shields.io/badge/Telegram-Bots-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode_bots)

📍 Rio Grande do Sul, Brazil

</div>

---

## 📄 License

Distributed under the MIT license. See [LICENSE](LICENSE) for more details.
