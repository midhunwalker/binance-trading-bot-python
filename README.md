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
   cd binance-trading-bot-python/trading_bot
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional for demo)**
   ```bash
   cp .env.example .env
   # Edit .env with your Binance testnet API credentials
   ```
   
   **Note:** The bot works without API credentials using a mock client for demonstration purposes.

5. **Get testnet API keys (for live testing)**
   - Visit https://testnet.binancefuture.com
   - Create an account and generate API keys
   - Add credentials to `.env` file

## Usage

### Place Market Order
```bash
python cli.py <SYMBOL> <SIDE> MARKET <QUANTITY>
```

**Example:**
```bash
python cli.py BTCUSDT BUY MARKET 0.001
```

### Place Limit Order
```bash
python cli.py <SYMBOL> <SIDE> LIMIT <QUANTITY> --price <PRICE>
```

**Example:**
```bash
python cli.py ETHUSDT SELL LIMIT 0.01 --price 3500
```

### Parameters
- `SYMBOL`: Trading pair (e.g., BTCUSDT, ETHUSDT)
- `SIDE`: BUY or SELL
- `ORDER_TYPE`: MARKET or LIMIT
- `QUANTITY`: Order quantity (must be positive)
- `--price`: Limit order price (required for LIMIT orders)

### Demo Mode
The bot automatically uses a **mock client** when:
- No `.env` file is present
- API credentials are invalid
- Binance API is unavailable

This allows you to test the bot without any API setup.

## Features

- **Market and Limit Order Execution** - Place orders with full parameter validation
- **Automatic Fallback System** - Mock client activates when API is unavailable
- **Zero Downtime** - Never fails even if Binance API is down
- **Structured Logging** - File rotation (10MB max, 5 backups) with detailed request/response tracking
- **Professional CLI Output** - Clear formatting with order summaries and results
- **Input Validation** - Comprehensive checks for all trading parameters
- **Testnet Support** - Safe testing environment before live trading
- **Demo Mode** - Works without API credentials for demonstrations

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper with fallback
│   ├── mock_client.py     # Mock client for demo/fallback mode
│   ├── orders.py          # Order execution with enhanced logging
│   ├── validators.py      # Input validation utilities
│   └── logging_config.py  # Logging configuration (rotation)
├── logs/                  # Log files directory (auto-created)
│   └── trading.log        # Rotating log file
├── venv/                  # Virtual environment (after setup)
├── cli.py                 # Typer-based CLI interface
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # Documentation
```

## Safety Features

- **Automatic Fallback** - Seamlessly switches to mock client on API failure
- **Comprehensive Error Handling** - Network, API, validation, and timeout errors
- **Detailed Logging** - All requests/responses logged with stack traces
- **Testnet Environment** - Safe testing without real funds
- **Input Validation** - All parameters validated before execution
- **Zero-Failure Design** - Application never crashes due to API issues

## Security Notes

⚠️ **Never commit API keys to version control**
- Use environment variables for credentials
- Always test with testnet before using real funds
- Start with small quantities when trading live

## License

MIT
