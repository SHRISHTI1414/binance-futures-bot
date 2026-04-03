"""
Binance Futures Testnet API client wrapper.
Handles authentication, request signing, and HTTP communication.
"""

import hashlib
import hmac
import time
import logging
from urllib.parse import urlencode
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceClientError(Exception):
    """Raised when the Binance API returns an error response."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")


class BinanceClient:
    """
    Lightweight wrapper around the Binance Futures Testnet REST API.
    Handles HMAC-SHA256 request signing and error normalisation.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = TESTNET_BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sign(self, params: dict) -> dict:
        """Append a HMAC-SHA256 signature to *params* (mutates and returns it)."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        signed: bool = False,
    ) -> Any:
        """
        Execute an HTTP request and return the parsed JSON body.

        Raises:
            BinanceClientError: for API-level errors (non-200 or ``code`` in body).
            requests.exceptions.RequestException: for network-level failures.
        """
        params = params or {}
        if signed:
            params = self._sign(params)

        url = f"{self.base_url}{endpoint}"
        logger.debug("→ %s %s  params=%s", method.upper(), url, params)

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, data=params, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except requests.exceptions.RequestException as exc:
            logger.error("Network failure: %s", exc)
            raise

        logger.debug("← %s  body=%s", response.status_code, response.text[:500])

        data = response.json()

        # Binance wraps API errors in {"code": <negative int>, "msg": "..."}
        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceClientError(data["code"], data.get("msg", "Unknown error"))

        return data

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    def get_exchange_info(self) -> dict:
        """Return exchange info (symbol metadata, filters, etc.)."""
        return self._request("GET", "/fapi/v1/exchangeInfo")

    def get_account(self) -> dict:
        """Return account details (balances, positions, etc.)."""
        return self._request("GET", "/fapi/v2/account", signed=True)

    def place_order(self, **kwargs) -> dict:
        """
        Place a new futures order.

        Common kwargs: symbol, side, type, quantity, price, timeInForce,
                       stopPrice, reduceOnly, newOrderRespType.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        logger.info("Placing order: %s", params)
        result = self._request("POST", "/fapi/v1/order", params=params, signed=True)
        logger.info("Order placed successfully: orderId=%s status=%s", result.get("orderId"), result.get("status"))
        return result

    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancel an open order by symbol and orderId."""
        params = {"symbol": symbol, "orderId": order_id}
        return self._request("DELETE", "/fapi/v1/order", params=params, signed=True)

    def get_order(self, symbol: str, order_id: int) -> dict:
        """Query a single order's current status."""
        params = {"symbol": symbol, "orderId": order_id}
        return self._request("GET", "/fapi/v1/order", params=params, signed=True)
