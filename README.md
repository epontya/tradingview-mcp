# TradingView MCP

A Model Context Protocol (MCP) server that provides TradingView market data and technical analysis tools to AI assistants.

> Fork of [atilaahmettaner/tradingview-mcp](https://github.com/atilaahmettaner/tradingview-mcp) with additional features and improvements.

## Features

- 📈 **Real-time market data** — Fetch quotes, OHLCV data, and price information
- 🔍 **Technical analysis** — Access indicators like RSI, MACD, Moving Averages, Bollinger Bands
- 🔎 **Symbol search** — Search for stocks, crypto, forex, and futures symbols
- 📊 **Multi-timeframe support** — 1m, 5m, 15m, 1h, 4h, 1D, 1W and more
- 🌍 **Multiple exchanges** — NYSE, NASDAQ, BINANCE, COINBASE, and more
- 🤖 **MCP compatible** — Works with Claude, and any MCP-compatible AI client

## Requirements

- Python 3.10+
- `uv` (recommended) or `pip`

## Installation

### Using uv (recommended)

```bash
git clone https://github.com/your-username/tradingview-mcp.git
cd tradingview-mcp
uv sync
```

### Using pip

```bash
git clone https://github.com/your-username/tradingview-mcp.git
cd tradingview-mcp
pip install -r requirements.txt
```

## Configuration

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

See [`.env.example`](.env.example) for all available configuration options.

## Usage

### Running the MCP server

```bash
uv run python -m tradingview_mcp
```

Or directly:

```bash
uv run tradingview-mcp
```

### Docker

```bash
docker build -t tradingview-mcp .
docker run --env-file .env tradingview-mcp
```

## Claude Desktop Integration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/tradingview-mcp",
        "run",
        "tradingview-mcp"
      ]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_quote` | Get current price and market data for a symbol |
| `get_technical_analysis` | Get technical indicators and analysis summary |
| `search_symbols` | Search for trading symbols across exchanges |
| `get_history` | Fetch historical OHLCV candlestick data |
| `get_screener` | Screen stocks/crypto by technical conditions |

## Development

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
