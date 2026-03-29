"""CLI interface for Binance Futures Trading Bot"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    validate_api_credentials,
    ValidationError
)

logger = logging.getLogger(__name__)


def get_credentials():
    """Get API credentials from environment variables"""
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    try:
        validate_api_credentials(api_key, api_secret)
    except ValidationError as e:
        logger.error(f"Credential validation failed: {e}")
        print("Error: Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        sys.exit(1)
    
    return api_key, api_secret


def cmd_balance(args):
    """Get account balance"""
    api_key, api_secret = get_credentials()
    client = BinanceFuturesClient(api_key, api_secret, testnet=args.testnet)
    
    try:
        balance = client.get_account_balance()
        print("\nAccount Balance:")
        for asset in balance:
            if float(asset['balance']) > 0:
                print(f"  {asset['asset']}: {asset['balance']}")
    except Exception as e:
        logger.error(f"Failed to fetch balance: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_position(args):
    """Get position information"""
    api_key, api_secret = get_credentials()
    client = BinanceFuturesClient(api_key, api_secret, testnet=args.testnet)
    
    try:
        symbol = validate_symbol(args.symbol) if args.symbol else None
        positions = client.get_position_info(symbol)
        
        print("\nOpen Positions:")
        for pos in positions:
            if float(pos.get('positionAmt', 0)) != 0:
                print(f"  {pos['symbol']}: {pos['positionAmt']} @ {pos['entryPrice']}")
    except ValidationError as e:
        print(f"Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to fetch positions: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_market_order(args):
    """Place a market order"""
    api_key, api_secret = get_credentials()
    client = BinanceFuturesClient(api_key, api_secret, testnet=args.testnet)
    order_manager = OrderManager(client.client)
    
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        
        if not args.confirm:
            print(f"\nOrder Preview:")
            print(f"  Type: MARKET")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Quantity: {quantity}")
            print("\nUse --confirm to execute this order")
            return
        
        order = order_manager.place_market_order(symbol, side, quantity)
        print(f"\nOrder placed successfully!")
        print(f"  Order ID: {order['orderId']}")
        print(f"  Status: {order['status']}")
        
    except ValidationError as e:
        print(f"Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_limit_order(args):
    """Place a limit order"""
    api_key, api_secret = get_credentials()
    client = BinanceFuturesClient(api_key, api_secret, testnet=args.testnet)
    order_manager = OrderManager(client.client)
    
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)
        
        if not args.confirm:
            print(f"\nOrder Preview:")
            print(f"  Type: LIMIT")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Quantity: {quantity}")
            print(f"  Price: {price}")
            print("\nUse --confirm to execute this order")
            return
        
        order = order_manager.place_limit_order(symbol, side, quantity, price)
        print(f"\nOrder placed successfully!")
        print(f"  Order ID: {order['orderId']}")
        print(f"  Status: {order['status']}")
        
    except ValidationError as e:
        print(f"Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Binance Futures Trading Bot CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--testnet',
        action='store_true',
        help='Use Binance testnet'
    )
    
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Set logging level'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Balance command
    subparsers.add_parser('balance', help='Get account balance')
    
    # Position command
    position_parser = subparsers.add_parser('position', help='Get position information')
    position_parser.add_argument('--symbol', help='Trading pair symbol (optional)')
    
    # Market order command
    market_parser = subparsers.add_parser('market', help='Place market order')
    market_parser.add_argument('symbol', help='Trading pair (e.g., BTCUSDT)')
    market_parser.add_argument('side', help='Order side (buy/sell)')
    market_parser.add_argument('quantity', type=float, help='Order quantity')
    market_parser.add_argument('--confirm', action='store_true', help='Confirm order execution')
    
    # Limit order command
    limit_parser = subparsers.add_parser('limit', help='Place limit order')
    limit_parser.add_argument('symbol', help='Trading pair (e.g., BTCUSDT)')
    limit_parser.add_argument('side', help='Order side (buy/sell)')
    limit_parser.add_argument('quantity', type=float, help='Order quantity')
    limit_parser.add_argument('price', type=float, help='Limit price')
    limit_parser.add_argument('--confirm', action='store_true', help='Confirm order execution')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level, log_dir='logs')
    
    # Route to appropriate command
    if args.command == 'balance':
        cmd_balance(args)
    elif args.command == 'position':
        cmd_position(args)
    elif args.command == 'market':
        cmd_market_order(args)
    elif args.command == 'limit':
        cmd_limit_order(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
