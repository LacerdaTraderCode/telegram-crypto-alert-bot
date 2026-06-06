<div align="center">

# 🤖 Telegram Crypto Alert Bot

**Bot para Telegram que monitora preços de criptomoedas e envia alertas em tempo real**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Binance](https://img.shields.io/badge/Binance-FCD535?logo=binance&logoColor=black)](https://binance-docs.github.io/apidocs/)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-orange)](https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github)](https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot)

</div>

---

## 📌 Sobre o projeto

Bot para Telegram que monitora preços de criptomoedas em tempo real via **API da Binance** e envia alertas personalizados quando os preços atingem os valores configurados pelo usuário. Construído com `python-telegram-bot` e arquitetura totalmente assíncrona.

### Funcionalidades

- ✅ **Consulta de preços em tempo real** de qualquer par cripto (BTC/USDT, ETH/USDT, etc.)
- ✅ **Alertas por preço acima ou abaixo** de um valor definido pelo usuário
- ✅ **Lista de alertas ativos** por usuário
- ✅ **Monitoramento assíncrono** em background
- ✅ **Persistência em SQLite** — alertas sobrevivem a restarts
- ✅ **Rate limit** automático respeitando os limites da API Binance

---

## 🛠️ Tecnologias

- **python-telegram-bot** — Framework oficial para bots no Telegram
- **aiohttp** — Cliente HTTP assíncrono para a API Binance
- **SQLAlchemy** — ORM para persistência dos alertas
- **asyncio** — Programação assíncrona nativa
- **APScheduler** — Agendamento de jobs periódicos de monitoramento

---

## 📁 Estrutura

```
telegram-crypto-alert-bot/
├── bot/
│   ├── main.py              # Ponto de entrada
│   ├── handlers.py          # Handlers dos comandos
│   ├── binance_client.py    # Cliente da API Binance
│   ├── database.py          # Persistência de alertas
│   └── monitor.py           # Job de monitoramento em background
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📦 Instalação

### Pré-requisitos

- Python 3.11+
- Token de bot do Telegram — [crie via @BotFather](https://t.me/BotFather)

### Passos

```bash
git clone https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot.git
cd telegram-crypto-alert-bot

python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt

cp .env.example .env
# Edite .env e adicione seu TELEGRAM_BOT_TOKEN

python -m bot.main
```

---

## 💬 Comandos disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Mensagem de boas-vindas | `/start` |
| `/help` | Lista todos os comandos | `/help` |
| `/price <par>` | Preço atual do par | `/price BTCUSDT` |
| `/alert <par> <above\|below> <valor>` | Cria alerta | `/alert BTCUSDT above 70000` |
| `/alerts` | Lista alertas ativos | `/alerts` |
| `/remove <id>` | Remove alerta pelo ID | `/remove 3` |

---

## 🖼️ Exemplo de uso

```
Usuário: /price BTCUSDT
Bot: 💰 BTCUSDT: $67.432,50 (+2,15% em 24h)

Usuário: /alert BTCUSDT above 70000
Bot: ✅ Alerta criado! Aviso quando BTCUSDT passar de $70.000

[quando o preço sobe...]
Bot: 🚨 ALERTA! BTCUSDT atingiu $70.150 — sua meta era $70.000
```

---

## 🔒 Segurança

- ✅ Token do bot nunca é commitado (fica em `.env`)
- ✅ Cada usuário só vê seus próprios alertas
- ✅ Rate limiting previne abuso da API Binance
- ✅ Tratamento de erros em todas as operações assíncronas

---

## 🚀 Deploy 24/7

- **VPS** — DigitalOcean, Linode, Contabo
- **Railway** ou **Render** — gratuito até certo limite
- **Raspberry Pi** — ideal para uso pessoal

---

## ✅ Requisitos

- Python **3.11** ou superior
- Token de bot do Telegram

---

## 👤 Autor

<div align="center">

**Wagner Lacerda** — Python Backend Developer | APIs REST • Automação • Data Engineering

[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github&logoColor=white)](https://github.com/LacerdaTraderCode)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wagner%20Lacerda-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/wagner-lacerda-da-silva-958b9481)
[![YouTube](https://img.shields.io/badge/YouTube-LacerdaTraderCode-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@LacerdaTraderCode)
[![Telegram](https://img.shields.io/badge/Telegram-LacerdaTraderCode-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode)
[![Telegram Bots](https://img.shields.io/badge/Telegram-Bots-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode_bots)

📍 Rio Grande do Sul, Brasil

</div>

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
