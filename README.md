# Binance Futures Testnet Trading Bot

A CLI-based trading bot for placing orders on the Binance Futures Testnet (USDT-M).

This project was built to understand how trading systems actually work under the hood — especially API authentication, request signing, and order execution — without relying on external SDKs. All interactions are done using raw REST calls (`requests`) to keep things transparent and controllable.

---

## Features

- Supports multiple order types:
  - MARKET  
  - LIMIT  
  - STOP (Stop-Limit)  
  - STOP_MARKET  
- BUY and SELL support  
- CLI interface using argparse  
- Input validation to prevent invalid orders  
- Logging system (file + console)  
- Clean, modular code structure  

## Project Structure

```
trading_bot/
├── bot/
│   ├── client.py          # API authentication, signing, HTTP requests
│   ├── orders.py          # Order logic and response formatting
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/                  # Runtime logs (auto-created)
├── cli.py                 # CLI entry point
├── .env.example           # API key template
├── requirements.txt
└── README.md
```

## Setup

### 1. Get Binance Testnet API Keys

Go to: https://testnet.binancefuture.com  
Login using GitHub and generate API keys.

---

### 2. Clone and Install

```bash
git clone https://github.com/<your-username>/binance-futures-bot.git
cd binance-futures-bot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configure Environment Variables
cp .env.example .env

Add your keys:

BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_API_SECRET=your_secret_here

Do not commit .env to version control.

Usage
Basic Command
python cli.py --symbol SYMBOL --side BUY|SELL --type ORDER_TYPE --quantity QTY
Examples

Market Order (Buy)

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

Limit Order (Sell)

python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000

Stop Market Order

python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 82000
Debug Mode
python cli.py --log-level DEBUG ...

This shows detailed API request and response logs.

CLI Reference
Flag	Required	Description
--symbol	✅	Trading pair (e.g. BTCUSDT)
--side	✅	BUY or SELL
--type	✅	MARKET / LIMIT / STOP / STOP_MARKET
--quantity	✅	Order quantity
--price	⚠️	Required for LIMIT / STOP
--stop-price	⚠️	Required for STOP / STOP_MARKET
--api-key	❌	Overrides environment variable
--api-secret	❌	Overrides environment variable
--log-level	❌	DEBUG / INFO / WARNING / ERROR
Logging

Logs are stored in:

logs/trading_bot.log
Console → clean output
File → detailed debug logs
Design Decisions
No Binance SDK used → better understanding of API internals
CLI-first approach → easier testing and iteration
Validation layer → avoids invalid API calls
Limitations
Works only on Binance Futures Testnet
Assumes one-way position mode
No strategy or automation layer (execution-only bot)
Future Improvements
Add trading strategies
Mainnet support
Async request handling
Web dashboard / UI
Tech Stack
Python 3.9+
requests
python-dotenv
Note

This is a learning-focused project designed to understand trading APIs and system design. It is not intended to be a profit-generating bot.
