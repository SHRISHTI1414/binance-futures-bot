"""
Order placement logic and response formatting.
This layer sits between the CLI and the raw API client.
"""

import logging
from typing import Optional

from bot.client import BinanceClient, BinanceClientError
from bot.validators import validate_all

logger = logging.getLogger(__name__)


def _fmt_order_response(resp: dict) -> str:
    """Return a human-readable summary of an order response dict."""
    lines = [
        "",
        "┌─ Order Response ─────────────────────────────",
        f"│  orderId       : {resp.get('orderId', 'N/A')}",
        f"│  clientOrderId : {resp.get('clientOrderId', 'N/A')}",
        f"│  symbol        : {resp.get('symbol', 'N/A')}",
        f"│  side          : {resp.get('side', 'N/A')}",
        f"│  type          : {resp.get('type', 'N/A')}",
        f"│  status        : {resp.get('status', 'N/A')}",
        f"│  price         : {resp.get('price', 'N/A')}",
        f"│  origQty       : {resp.get('origQty', 'N/A')}",
        f"│  executedQty   : {resp.get('executedQty', 'N/A')}",
        f"│  avgPrice      : {resp.get('avgPrice', 'N/A')}",
        f"│  timeInForce   : {resp.get('timeInForce', 'N/A')}",
        f"│  updateTime    : {resp.get('updateTime', 'N/A')}",
        "└──────────────────────────────────────────────",
    ]
    return "\n".join(lines)


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> dict:
    """
    Validate inputs, place the order, and return the API response dict.

    Raises:
        ValueError: if any input parameter is invalid.
        BinanceClientError: if the exchange rejects the order.
        requests.exceptions.RequestException: on network failure.
    """
    # 1. Validate
    params = validate_all(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price,
    )

    # 2. Print request summary
    summary_lines = [
        "",
        "┌─ Order Request ──────────────────────────────",
        f"│  symbol     : {params['symbol']}",
        f"│  side       : {params['side']}",
        f"│  type       : {params['type']}",
        f"│  quantity   : {params['quantity']}",
        f"│  price      : {params.get('price', 'N/A (MARKET)')}",
        f"│  stopPrice  : {params.get('stopPrice', 'N/A')}",
        f"│  timeInForce: {params.get('timeInForce', 'N/A')}",
        "└──────────────────────────────────────────────",
    ]
    print("\n".join(summary_lines))
    logger.info("Submitting order: %s", params)

    # 3. Place
    response = client.place_order(**params)

    # 4. Print + log response
    print(_fmt_order_response(response))
    logger.info("Order response: %s", response)

    return response
