inance-futures-bot
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security and quality
Insights
Settings
Owner avatar
binance-futures-bot
Public
SHRISHTI1414/binance-futures-bot
Go to file
t
Name		
SHRISHTI1414
SHRISHTI1414
Initial commit: Binance Futures Testnet trading bot
02af805
 · 
1 hour ago
bot
Initial commit: Binance Futures Testnet trading bot
1 hour ago
logs
Initial commit: Binance Futures Testnet trading bot
1 hour ago
.env.example
Initial commit: Binance Futures Testnet trading bot
1 hour ago
README.md
Initial commit: Binance Futures Testnet trading bot
1 hour ago
cli.py
Initial commit: Binance Futures Testnet trading bot
1 hour ago
requirements.txt
Initial commit: Binance Futures Testnet trading bot
1 hour ago
Repository files navigation
README
Binance Futures Testnet Trading Bot
A clean, production-style Python CLI application for placing orders on the Binance Futures Testnet (USDT-M). Built with direct REST calls (requests) — no third-party Binance SDK required.

Features
Capability	Details
Order types	MARKET, LIMIT, STOP (Stop-Limit), STOP_MARKET ✨
Sides	BUY and SELL
CLI	argparse-based with full validation and clear error messages
Logging	Rotating file log + console; DEBUG-level API traces in file
Error handling	Validation errors, Binance API errors, network failures — all caught and reported cleanly
Structure	Separate client / orders / validators / logging layers
Project Structure
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST client (auth, signing, HTTP)
│   ├── orders.py          # Order placement logic + response formatting
│   ├── validators.py      # Input validation (raises ValueError on bad input)
│   └── logging_config.py  # Rotating file + console logging setup
├── logs/
│   └── trading_bot.log    # Auto-created on first run
├── cli.py                 # CLI entry point (argparse)
├── .env.example           # Template for credentials
├── requirements.txt
└── README.md
Setup
1. Register on Binance Futures Testnet
Visit https://testnet.binancefuture.com
Log in with your GitHub account
Click "Generate API Key" under the API Management section
Copy your API Key and Secret Key
2. Clone and install
git clone https://github.com/<your-username>/binance-futures-bot.git
cd binance-futures-bot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configure credentials
cp .env.example .env
Edit .env:

BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_API_SECRET=your_secret_here
Never commit .env to version control.

How to Run
General syntax
python cli.py --symbol SYMBOL --side BUY|SELL --type ORDER_TYPE --quantity QTY [--price PRICE] [--stop-price STOP_PRICE]
Examples
Market BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
Output:

┌─ Order Request ──────────────────────────────
│  symbol     : BTCUSDT
│  side       : BUY
│  type       : MARKET
│  quantity   : 0.001
│  price      : N/A (MARKET)
│  stopPrice  : N/A
│  timeInForce: N/A
└──────────────────────────────────────────────

┌─ Order Response ─────────────────────────────
│  orderId       : 4751823649
│  clientOrderId : web_f8x2k9m1p0q3r4s5t6u7
│  symbol        : BTCUSDT
│  side          : BUY
│  type          : MARKET
│  status        : FILLED
│  price         : 0
│  origQty       : 0.001
│  executedQty   : 0.001
│  avgPrice      : 83421.50
│  timeInForce   : GTC
│  updateTime    : 1743668522013
└──────────────────────────────────────────────

✅  Order placed successfully.
Limit SELL
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000
Stop-Market BUY (bonus order type)
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 82000
Stop-Limit SELL (bonus order type)
python cli.py --symbol ETHUSDT --side SELL --type STOP --quantity 0.01 --price 3000 --stop-price 3100
Override credentials inline (not recommended — prefer .env)
python cli.py --api-key <KEY> --api-secret <SECRET> \
  --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
Verbose debug output
python cli.py --log-level DEBUG --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
CLI Reference
Flag	Required	Description
--symbol	✅	Trading pair, e.g. BTCUSDT
--side	✅	BUY or SELL
--type	✅	MARKET, LIMIT, STOP, or STOP_MARKET
--quantity	✅	Quantity in base asset
--price	⚠️	Required for LIMIT and STOP
--stop-price	⚠️	Required for STOP and STOP_MARKET
--api-key	❌	Falls back to BINANCE_TESTNET_API_KEY env var
--api-secret	❌	Falls back to BINANCE_TESTNET_API_SECRET env var
--log-level	❌	DEBUG/INFO/WARNING/ERROR (default: INFO)
Logging
Logs are written to logs/trading_bot.log (rotating, max 5 MB × 3 backups) and to the console.

File: DEBUG level — full API request/response traces
Console: INFO level by default (override with --log-level DEBUG)
Sample log entries:

2026-04-03T10:12:01 | INFO     | bot.client | Placing order: {'symbol': 'BTCUSDT', 'side': 'BUY', ...}
2026-04-03T10:12:02 | DEBUG    | bot.client | ← 200  body={"orderId":4751823649, ...}
2026-04-03T10:12:02 | INFO     | bot.client | Order placed successfully: orderId=4751823649 status=FILLED
Error Handling
Scenario	Exit code	Behaviour
Invalid input (bad symbol, missing price, etc.)	2	Prints ❌ Validation error: ...; logged as ERROR
Binance API rejection (bad qty, insufficient margin, etc.)	3	Prints ❌ Binance API error <code>: <message>
Network failure (timeout, DNS, etc.)	1	Prints ❌ Unexpected error: ...; stack trace in log
Assumptions
Testnet only — the base URL is hard-coded to https://testnet.binancefuture.com. To use mainnet, change TESTNET_BASE_URL in bot/client.py and update credentials accordingly.
One-way position mode assumed (positionSide=BOTH). Hedge mode requires adding positionSide to order params.
timeInForce defaults to GTC for LIMIT/STOP orders.
Quantity and price precision must satisfy the exchange's symbol filters (checked server-side; the API will return a meaningful error if violated).
Python 3.9+ required.
Requirements
requests>=2.31.0
python-dotenv>=1.0.0
No Binance SDK dependency — all API communication is done with plain requests.
