# Binance Futures Trading Bot

A clean, production-ready CLI-based trading bot for Binance Futures.

## Features

- Account balance monitoring
- Position tracking
- Market and limit order execution
- Input validation
- Structured logging with file rotation
- Testnet support

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
└── README.md
```

## Installation

1. Clone the repository:
```bash
cd trading_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

## Usage

### Check Account Balance
```bash
python cli.py balance
```

### View Positions
```bash
# All positions
python cli.py position

# Specific symbol
python cli.py position --symbol BTCUSDT
```

### Place Market Order
```bash
# Preview order (dry run)
python cli.py market BTCUSDT buy 0.001

# Execute order
python cli.py market BTCUSDT buy 0.001 --confirm
```

### Place Limit Order
```bash
# Preview order
python cli.py limit BTCUSDT buy 0.001 50000

# Execute order
python cli.py limit BTCUSDT buy 0.001 50000 --confirm
```

### Testnet Mode
```bash
python cli.py --testnet balance
```

### Logging
```bash
# Set log level
python cli.py --log-level DEBUG balance
```

Logs are automatically saved to `logs/trading_bot.log` with rotation (max 10MB, 5 backups).

## Safety Features

- Validation of all inputs (symbol, side, quantity, price)
- Order preview before execution (requires --confirm flag)
- Comprehensive error handling and logging
- Support for testnet environment

## Requirements

- Python 3.7+
- Valid Binance API credentials
- Internet connection

## Security Notes

- Never commit API keys to version control
- Use environment variables for credentials
- Test with testnet before using real funds
- Start with small quantities

## License

MIT
