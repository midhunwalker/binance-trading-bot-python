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
        
    Raises:
        ValueError: If validation fails or API error occurs
        ConnectionError: If network issue occurs
    """
    try:
        logger.info(f"Preparing market order: {side} {quantity} {symbol}")
        
        # Validate inputs
        side = validate_side(side)
        quantity = validate_quantity(quantity)
        
        # Log request parameters
        logger.info(f"Request params - Symbol: {symbol}, Side: {side}, Type: MARKET, Quantity: {quantity}")
        
        # Initialize client and place order
        client = BinanceFuturesClient()
        response = client.place_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        # Log successful response
        logger.info(f"Market order executed - Order ID: {response.get('orderId')}, "
                   f"Status: {response.get('status')}, Executed Qty: {response.get('executedQty')}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error for market order: {e}")
        raise
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error placing market order: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error placing market order: {type(e).__name__}: {e}")
        raise


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
        
    Raises:
        ValueError: If validation fails or API error occurs
        ConnectionError: If network issue occurs
    """
    try:
        logger.info(f"Preparing limit order: {side} {quantity} {symbol} @ {price}")
        
        # Validate inputs
        side = validate_side(side)
        quantity = validate_quantity(quantity)
        price = validate_price(price, 'LIMIT')
        
        # Log request parameters
        logger.info(f"Request params - Symbol: {symbol}, Side: {side}, Type: LIMIT, "
                   f"Quantity: {quantity}, Price: {price}, TimeInForce: GTC")
        
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
        
        # Log successful response
        logger.info(f"Limit order executed - Order ID: {response.get('orderId')}, "
                   f"Status: {response.get('status')}, Executed Qty: {response.get('executedQty')}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error for limit order: {e}")
        raise
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error placing limit order: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error placing limit order: {type(e).__name__}: {e}")
        raise
