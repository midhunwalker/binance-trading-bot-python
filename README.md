# Binance Futures Trading Bot

A production-ready CLI-based trading bot for Binance Futures with testnet support.

## Tech Stack

- **Python 3.7+**
- **python-binance** - Binance API wrapper
- **typer** - CLI framework
- **python-dotenv** - Environment variable management

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/midhunwalker/binance-trading-bot-python.git
   cd binance-trading-bot-python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Binance testnet API credentials
   ```

4. **Get testnet API keys**
   - Visit https://testnet.binancefuture.com
   - Create an account and generate API keys

## Usage

Coming soon...

## Features

- Account balance monitoring
- Position tracking
- Market and limit order execution
- Input validation
- Structured logging with file rotation
- Testnet support for safe testing

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper
│   ├── orders.py          # Order management
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/                  # Log files directory
├── cli.py                 # CLI interface
├── requirements.txt
├── .env.example
└── README.md
```

## Safety Features

- Order preview before execution
- Comprehensive error handling and logging
- Testnet environment for safe testing
- Input validation for all trading parameters

## Security Notes

⚠️ **Never commit API keys to version control**
- Use environment variables for credentials
- Always test with testnet before using real funds
- Start with small quantities when trading live

## License

MIT
