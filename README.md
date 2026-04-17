# 🤖 Telegram Crypto Alert Bot

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Binance](https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=black)](https://binance-docs.github.io/apidocs/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

Bot para Telegram que monitora preços de criptomoedas em tempo real na Binance e envia alertas quando os preços atingem valores configurados pelo usuário. Construído com `python-telegram-bot` e arquitetura assíncrona.

---

## 📋 Funcionalidades

- ✅ **Consulta de preços em tempo real** de qualquer par cripto (BTC/USDT, ETH/USDT, etc.)
- ✅ **Sistema de alertas** por preço acima/abaixo de um valor
- ✅ **Lista de alertas ativos** por usuário
- ✅ **Monitoramento assíncrono** em background
- ✅ **Persistência em SQLite** (alertas sobrevivem a restarts)
- ✅ **Comandos interativos** com menu de ajuda
- ✅ **Rate limit** automático da API Binance

---

## 🛠️ Tecnologias

- **python-telegram-bot** — Framework oficial do Telegram
- **aiohttp** — Cliente HTTP assíncrono para Binance API
- **SQLAlchemy** — ORM para persistência
- **asyncio** — Programação assíncrona
- **APScheduler** — Agendamento de tarefas periódicas

---

## 📁 Estrutura

```
telegram-crypto-alert-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada
│   ├── handlers.py          # Handlers dos comandos
│   ├── binance_client.py    # Cliente da API Binance
│   ├── database.py          # Persistência de alertas
│   └── monitor.py           # Job de monitoramento
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.11+
- Token de bot do Telegram ([crie um aqui](https://t.me/BotFather))

### Passos

```bash
# Clonar repositório
git clone https://github.com/LacerdaTraderCode/telegram-crypto-alert-bot.git
cd telegram-crypto-alert-bot

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar token
cp .env.example .env
# Edite .env e adicione seu TELEGRAM_BOT_TOKEN

# Rodar o bot
python -m bot.main
```

---

## 💬 Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Mensagem de boas-vindas | `/start` |
| `/help` | Lista todos os comandos | `/help` |
| `/price <par>` | Consulta preço atual | `/price BTCUSDT` |
| `/alert <par> <above\|below> <preço>` | Cria alerta | `/alert BTCUSDT above 70000` |
| `/alerts` | Lista seus alertas ativos | `/alerts` |
| `/remove <id>` | Remove alerta | `/remove 3` |

---

## 🖼️ Exemplo de Uso

```
Usuário: /price BTCUSDT
Bot: 💰 BTCUSDT: $67,432.50 (+2.15% em 24h)

Usuário: /alert BTCUSDT above 70000
Bot: ✅ Alerta criado! Vou avisar quando BTCUSDT passar de $70.000

[alguns minutos depois, quando o preço sobe...]
Bot: 🚨 ALERTA! BTCUSDT atingiu $70.150 (sua meta era $70.000)
```

---

## 🔒 Segurança

- ✅ Token do bot nunca é commitado (fica em `.env`)
- ✅ Cada usuário só vê seus próprios alertas
- ✅ Rate limiting previne abuso da API Binance
- ✅ Tratamento de erros em todas as operações assíncronas

---

## 🚀 Deploy

Recomendado rodar 24/7 em:
- **VPS** (DigitalOcean, Linode, Contabo)
- **Railway** ou **Render** (gratuito até certo limite)
- **Raspberry Pi** (para uso pessoal)

---

## 👨‍💻 Autor

**Wagner Lacerda**  
🔗 [LinkedIn](https://www.linkedin.com/in/wagner-lacerda-da-silva-958b9481)  
🐙 [GitHub](https://github.com/LacerdaTraderCode)  

---

## 📄 Licença

MIT License - use livremente em seus projetos.
