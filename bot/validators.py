"""
Input validation helpers for order parameters.
All validators raise ValueError with a human-readable message on failure.
"""

from decimal import Decimal, InvalidOperation
from typing import Optional


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP", "STOP_MARKET"}
VALID_TIF = {"GTC", "IOC", "FOK", "GTX"}


def validate_symbol(symbol: str) -> str:
    """Return uppercased symbol or raise ValueError."""
    if not symbol or not symbol.strip():
        raise ValueError("Symbol must not be empty.")
    return symbol.strip().upper()


def validate_side(side: str) -> str:
    """Return uppercased side or raise ValueError."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be one of {sorted(VALID_SIDES)}, got '{side}'.")
    return side


def validate_order_type(order_type: str) -> str:
    """Return uppercased order type or raise ValueError."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Order type must be one of {sorted(VALID_ORDER_TYPES)}, got '{order_type}'."
        )
    return order_type


def validate_quantity(quantity: str) -> str:
    """
    Validate that quantity is a positive decimal number.
    Returns the string representation suitable for the API.
    """
    try:
        qty = Decimal(str(quantity))
    except InvalidOperation:
        raise ValueError(f"Quantity must be a valid number, got '{quantity}'.")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {qty}.")
    return str(qty)


def validate_price(price: Optional[str], order_type: str) -> Optional[str]:
    """
    Validate price for LIMIT / STOP orders.
    Returns None for MARKET / STOP_MARKET; validated string otherwise.
    """
    if order_type in {"MARKET", "STOP_MARKET"}:
        if price is not None:
            # Silently ignore price for market orders
            pass
        return None

    # LIMIT or STOP — price is required
    if price is None:
        raise ValueError(f"A price is required for {order_type} orders.")
    try:
        p = Decimal(str(price))
    except InvalidOperation:
        raise ValueError(f"Price must be a valid number, got '{price}'.")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0, got {p}.")
    return str(p)


def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[str]:
    """Validate stopPrice for STOP / STOP_MARKET orders."""
    if order_type not in {"STOP", "STOP_MARKET"}:
        return None
    if stop_price is None:
        raise ValueError(f"A stop price is required for {order_type} orders.")
    try:
        sp = Decimal(str(stop_price))
    except InvalidOperation:
        raise ValueError(f"Stop price must be a valid number, got '{stop_price}'.")
    if sp <= 0:
        raise ValueError(f"Stop price must be greater than 0, got {sp}.")
    return str(sp)


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> dict:
    """
    Run all validations and return a clean parameter dict ready for the API.
    Raises ValueError on the first invalid field encountered.
    """
    clean: dict = {}
    clean["symbol"] = validate_symbol(symbol)
    clean["side"] = validate_side(side)
    clean["type"] = validate_order_type(order_type)
    clean["quantity"] = validate_quantity(quantity)

    validated_price = validate_price(price, clean["type"])
    if validated_price is not None:
        clean["price"] = validated_price
        clean["timeInForce"] = "GTC"  # sensible default for limit orders

    validated_stop = validate_stop_price(stop_price, clean["type"])
    if validated_stop is not None:
        clean["stopPrice"] = validated_stop

    return clean
