 Binance Futures Testnet Trading Bot

A CLI-based trading bot for placing orders on the Binance Futures Testnet (USDT-M).

This project was built to understand how trading systems actually work under the hood — especially API authentication, request signing, and order execution — without relying on external SDKs.
All interactions are done using raw REST calls (requests) to keep things transparent and controllable.

Features
Supports multiple order types:
MARKET
LIMIT
STOP (Stop-Limit)
STOP_MARKET
BUY and SELL support
CLI interface using argparse
Input validation to prevent invalid orders
Logging system (file + console)
Clean, modular code structure
Project Structure
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
Setup
1. Get Binance Testnet API Keys
Go to: https://testnet.binancefuture.com
Login using GitHub
Generate API Key and Secret
2. Clone and Install
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

Shows detailed API request/response logs.

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
Console output: clean and readable
File logs: detailed debug information
Error Handling

The bot handles common failure scenarios:

Invalid inputs → validation errors
Binance API errors → clear error messages
Network failures → logged with details
Design Decisions
No Binance SDK used
→ Helps understand request signing and API behavior directly
CLI-first approach
→ Easier to test and extend before adding UI
Validation layer
→ Prevents unnecessary API calls with invalid data
Limitations
Works only on Binance Futures Testnet
Assumes one-way position mode
No strategy/automation layer (execution-only bot)
Future Improvements
Add trading strategies (signal-based execution)
Mainnet support via config
Async request handling
Simple dashboard or web UI
Tech Stack
Python 3.9+
requests
python-dotenv
Note

This is not a profit-generating bot.
It is a learning-focused project designed to build a strong understanding of trading APIs and system design.
