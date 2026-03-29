"""Order execution functions"""

import logging
from bot.client import get_client
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
        Order response from Binance API or Mock
        
    Raises:
        ValueError: If validation fails or API error occurs
        ConnectionError: If network issue occurs
    """
    try:
        logger.info(f"=== MARKET ORDER REQUEST ===")
        logger.info(f"Symbol: {symbol}, Side: {side}, Quantity: {quantity}")
        
        # Validate inputs
        side = validate_side(side)
        quantity = validate_quantity(quantity)
        
        # Log validated request parameters
        logger.info(f"Validated params - Symbol: {symbol}, Side: {side}, Type: MARKET, Quantity: {quantity}")
        
        # Initialize client (with auto-fallback) and place order
        client = get_client()
        response = client.place_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        # Log successful response with key details
        logger.info(f"=== MARKET ORDER RESPONSE ===")
        logger.info(f"Order ID: {response.get('orderId')}, Status: {response.get('status')}, "
                   f"Executed Qty: {response.get('executedQty')}, Avg Price: {response.get('avgPrice')}")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error for market order: {e}", exc_info=True)
        raise
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error placing market order: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error placing market order: {type(e).__name__}: {e}", exc_info=True)
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
        Order response from Binance API or Mock
        
    Raises:
        ValueError: If validation fails or API error occurs
        ConnectionError: If network issue occurs
    """
    try:
        logger.info(f"=== LIMIT ORDER REQUEST ===")
        logger.info(f"Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Price: {price}")
        
        # Validate inputs
        side = validate_side(side)
        quantity = validate_quantity(quantity)
        price = validate_price(price, 'LIMIT')
        
        # Log validated request parameters
        logger.info(f"Validated params - Symbol: {symbol}, Side: {side}, Type: LIMIT, "
                   f"Quantity: {quantity}, Price: {price}, TimeInForce: GTC")
        
        # Initialize client (with auto-fallback) and place order
        client = get_client()
        response = client.place_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        
        # Log successful response with key details
        logger.info(f"=== LIMIT ORDER RESPONSE ===")
        logger.info(f"Order ID: {response.get('orderId')}, Status: {response.get('status')}, "
                   f"Executed Qty: {response.get('executedQty')}, Avg Price: {response.get('avgPrice')}")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error for limit order: {e}", exc_info=True)
        raise
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error placing limit order: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error placing limit order: {type(e).__name__}: {e}", exc_info=True)
        raise
