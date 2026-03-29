"""Order execution functions"""

import logging
from bot.client import BinanceFuturesClient
from bot.validators import validate_side, validate_order_type, validate_quantity, validate_price

logger = logging.getLogger(__name__)


def place_market_order(symbol: str, side: str, quantity: float):
    """
    Place a market order.

    Args:
        symbol: Trading pair (e.g., 'BTCUSDT')
        side: Order side ('BUY' or 'SELL')
        quantity: Order quantity

    Returns:
        Order response from Binance API
    """
    logger.info(f"Placing market order: {side} {quantity} {symbol}")
    
    # Validate inputs
    side = validate_side(side)
    quantity = validate_quantity(quantity)
    
    # Initialize client and place order
    client = BinanceFuturesClient()
    response = client.place_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=quantity
    )
    
    logger.info(f"Market order placed successfully: Order ID {response.get('orderId')}")
    return response


def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Place a limit order.

    Args:
        symbol: Trading pair (e.g., 'BTCUSDT')
        side: Order side ('BUY' or 'SELL')
        quantity: Order quantity
        price: Limit price

    Returns:
        Order response from Binance API
    """
    logger.info(f"Placing limit order: {side} {quantity} {symbol} @ {price}")
    
    # Validate inputs
    side = validate_side(side)
    quantity = validate_quantity(quantity)
    price = validate_price(price, 'LIMIT')
    
    # Initialize client and place order
    client = BinanceFuturesClient()
    response = client.place_order(
        symbol=symbol,
        side=side,
        type='LIMIT',
        quantity=quantity,
        price=price,
        timeInForce='GTC'
    )
    
    logger.info(f"Limit order placed successfully: Order ID {response.get('orderId')}")
    return response
