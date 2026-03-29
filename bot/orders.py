"""Order execution and management"""

import logging
from typing import Dict, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


class OrderManager:
    """Manages order placement and execution"""

    def __init__(self, client: Client):
        """
        Initialize order manager.

        Args:
            client: Binance client instance
        """
        self.client = client

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        reduce_only: bool = False
    ) -> Dict:
        """
        Place a market order.

        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            reduce_only: Reduce-only flag

        Returns:
            Order response from Binance
        """
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity,
                reduceOnly=reduce_only
            )
            logger.info(f"Market order placed: {side} {quantity} {symbol}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error placing market order: {e}")
            raise

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        time_in_force: str = 'GTC'
    ) -> Dict:
        """
        Place a limit order.

        Args:
            symbol: Trading pair
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            time_in_force: Time in force (GTC, IOC, FOK)

        Returns:
            Order response from Binance
        """
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            logger.info(f"Limit order placed: {side} {quantity} {symbol} @ {price}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error placing limit order: {e}")
            raise

    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an open order"""
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            logger.info(f"Order cancelled: {order_id} for {symbol}")
            return result
        except BinanceAPIException as e:
            logger.error(f"Error cancelling order: {e}")
            raise

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict:
        """Get all open orders"""
        try:
            return self.client.futures_get_open_orders(symbol=symbol)
        except BinanceAPIException as e:
            logger.error(f"Error fetching open orders: {e}")
            raise
