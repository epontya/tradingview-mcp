"""
Yahoo Finance Price Service via Webshare Rotating Proxy.

Provides real-time quotes for stocks, ETFs, crypto pairs, indices
using the Yahoo Finance Chart API (no API key required).

Works with any symbol Yahoo Finance supports:
  Stocks:  AAPL, TSLA, MSFT, NVDA, GOOGL
  Crypto:  BTC-USD, ETH-USD, SOL-USD, BNB-USD
  ETFs:    SPY, QQQ, VTI
  Indices: ^GSPC (S&P500), ^DJI (Dow), ^IXIC (NASDAQ)
  FX:      EURUSD=X, GBPUSD=X
  Turkish: THYAO.IS, SASA.IS
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from typing import Optional

from tradingview_mcp.core.services.proxy_manager import build_opener_with_proxy

_TIMEOUT = 12
_UA = "tradingview-mcp/0.5.0"
_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"


def _fetch_quote(symbol: str) -> dict:
    """Fetch raw Yahoo Finance chart metadata for a symbol."""
    url = f"{_BASE}/{symbol}?interval=1d&range=2d"
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    opener = build_opener_with_proxy(_UA)
    with opener.open(req, timeout=_TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["chart"]["result"][0]["meta"]


def get_price(symbol: str) -> dict:
    """
    Get real-time price data for any Yahoo Finance symbol.

    Args:
        symbol: Yahoo Finance symbol (e.g. "AAPL", "BTC-USD", "THYAO.IS", "^GSPC")

    Returns:
        dict with price, change, change_pct, currency, exchange, market_state
    """
    try:
        meta = _fetch_quote(symbol)
        price      = meta.get("regularMarketPrice")
        prev_close = meta.get("previousClose") or meta.get("chartPreviousClose") or price
        chg        = round(price - prev_close, 4) if (price and prev_close) else None
        chg_pct    = round((price - prev_close) / prev_close * 100, 2) if (price and prev_close and prev_close != 0) else None

        return {
            "symbol":        symbol.upper(),
            "price":         price,
            "previous_close": prev_close,
            "change":        chg,
            "change_pct":    chg_pct,
            "currency":      meta.get("currency", "USD"),
            "exchange":      meta.get("exchangeName", ""),
            "market_state":  meta.get("marketState", ""),  # REGULAR, PRE, POST, CLOSED
            "52w_high":      meta.get("fiftyTwoWeekHigh"),
            "52w_low":       meta.get("fiftyTwoWeekLow"),
            "source":        "Yahoo Finance",
            "timestamp":     datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {"symbol": symbol.upper(), "error": str(e), "source": "Yahoo Finance"}


def get_prices_bulk(symbols: list[str]) -> list[dict]:
    """
    Get prices for multiple symbols at once.

    Args:
        symbols: List of Yahoo Finance symbols

    Returns:
        List of price dicts
    """
    results = []
    for sym in symbols:
        results.append(get_price(sym))
    return results


def get_market_snapshot() -> dict:
    """
    Get a snapshot of major market indices and crypto prices.

    Returns:
        Dict with stocks (S&P500, NASDAQ, Dow), crypto (BTC, ETH), and FX
    """
    groups = {
        "indices": ["^GSPC", "^DJI", "^IXIC", "^VIX"],
        "crypto":  ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"],
        "fx":      ["EURUSD=X", "GBPUSD=X", "JPYUSD=X"],
        "etfs":    ["SPY", "QQQ", "GLD"],
    }

    result = {}
    for group, syms in groups.items():
        result[group] = []
        for sym in syms:
            data = get_price(sym)
            if "error" not in data:
                result[group].append({
                    "symbol":     data["symbol"],
                    "price":      data["price"],
                    "change_pct": data["change_pct"],
                    "currency":   data["currency"],
                })

    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    return result
