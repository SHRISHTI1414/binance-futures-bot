# Binance Futures Testnet Trading Bot

A simple CLI-based trading bot for placing orders on the Binance Futures Testnet (USDT-M).

I built this project to understand how trading systems actually work — especially API authentication, request signing, and order execution — without relying on any external SDKs. Everything is implemented using raw REST calls (`requests`) so the flow stays clear and easy to follow.

---

## Features

- Supports MARKET, LIMIT, STOP, and STOP_MARKET orders  
- BUY and SELL support  
- CLI interface using argparse  
- Input validation to prevent invalid orders  
- Logging system (file + console)  
- Clean and modular code structure  

 ## Project Structure

    trading_bot/
    ├── bot/
    │   ├── client.py
    │   ├── orders.py
    │   ├── validators.py
    │   └── logging_config.py
    ├── logs/
    ├── cli.py
    ├── .env.example
    ├── requirements.txt
    └── README.md

## Setup

1. Get API keys from:
https://testnet.binancefuture.com

2. Clone the repository:

git clone https://github.com/<your-username>/binance-futures-bot.git
cd binance-futures-bot

3. Install dependencies:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4. Configure environment variables:

cp .env.example .env

Add your keys:

BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_API_SECRET=your_secret_here

---

## Usage

Example:

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

---

## Logging

Logs are stored in:

logs/trading_bot.log

---

## Design Decisions

- No Binance SDK used → better understanding of API internals  
- CLI-first approach → easier testing and iteration  
- Validation layer → avoids invalid API calls  

---

## Limitations

- Works only on Binance Futures Testnet  
- No trading strategy or automation layer  

---

## Tech Stack

- Python  
- requests  
- python-dotenv  

---

## Note

This is a learning-focused project meant for understanding trading APIs and system design. It is not intended for real trading.
