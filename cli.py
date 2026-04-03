#!/usr/bin/env python3
"""
cli.py – CLI entry point for the Binance Futures Testnet trading bot.

Usage examples
--------------
# Market BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Limit SELL
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000

# Stop-Market BUY (bonus order type)
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 95000

# Stop-Limit SELL (bonus order type)
python cli.py --symbol ETHUSDT --side SELL --type STOP --quantity 0.01 --price 3000 --stop-price 3100

# Override API credentials inline (not recommended – prefer .env)
python cli.py --api-key <KEY> --api-secret <SECRET> --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logging
from bot.orders import place_order

load_dotenv()  # load .env if present


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Credentials (fall back to env vars)
    creds = parser.add_argument_group("API credentials (or set via .env / env vars)")
    creds.add_argument(
        "--api-key",
        default=os.getenv("BINANCE_TESTNET_API_KEY"),
        help="Binance Testnet API key  [env: BINANCE_TESTNET_API_KEY]",
    )
    creds.add_argument(
        "--api-secret",
        default=os.getenv("BINANCE_TESTNET_API_SECRET"),
        help="Binance Testnet API secret  [env: BINANCE_TESTNET_API_SECRET]",
    )

    # Order parameters
    order = parser.add_argument_group("Order parameters")
    order.add_argument(
        "--symbol", required=True, metavar="SYMBOL",
        help="Trading pair, e.g. BTCUSDT",
    )
    order.add_argument(
        "--side", required=True, choices=["BUY", "SELL"],
        type=str.upper,
        help="Order side: BUY or SELL",
    )
    order.add_argument(
        "--type", required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT", "STOP", "STOP_MARKET"],
        type=str.upper,
        help="Order type",
    )
    order.add_argument(
        "--quantity", required=True, metavar="QTY",
        help="Order quantity in base asset",
    )
    order.add_argument(
        "--price", default=None, metavar="PRICE",
        help="Limit price (required for LIMIT / STOP)",
    )
    order.add_argument(
        "--stop-price", default=None, metavar="STOP_PRICE",
        help="Stop trigger price (required for STOP / STOP_MARKET)",
    )

    # Misc
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Console log verbosity (default: INFO)",
    )

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Initialise logging before anything else
    setup_logging(level=args.log_level)
    logger = logging.getLogger(__name__)

    # Credential check
    if not args.api_key or not args.api_secret:
        parser.error(
            "API credentials are required.\n"
            "Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET in .env "
            "or pass --api-key / --api-secret."
        )

    client = BinanceClient(api_key=args.api_key, api_secret=args.api_secret)

    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
        print("\n✅  Order placed successfully.\n")
        logger.info("CLI completed successfully.")

    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(f"\n❌  Validation error: {exc}\n", file=sys.stderr)
        sys.exit(2)

    except BinanceClientError as exc:
        logger.error("Binance API error %s: %s", exc.code, exc.message)
        print(f"\n❌  Binance API error {exc.code}: {exc.message}\n", file=sys.stderr)
        sys.exit(3)

    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        print(f"\n❌  Unexpected error: {exc}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
