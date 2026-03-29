"""Mock Binance Futures client for fallback and testing"""

import random
import logging
import time

logger = logging.getLogger(__name__)


class MockBinanceFuturesClient:
    """Mock client that simulates Binance Futures API responses"""

    def __init__(self):
        """Initialize mock client"""
        logger.warning("⚠️  MOCK CLIENT ACTIVE - Using simulated trading (Binance API unavailable)")
        logger.info("Initialized Mock Binance Futures client")

    def test_connection(self):
        """Simulate successful connection test"""
        logger.info("✅ Mock connection test successful")
        return True

    def place_order(self, **kwargs):
        """
        Simulate order placement.

        Args:
            **kwargs: Order parameters (symbol, side, type, quantity, price, etc.)

        Returns:
            Simulated order response
        """
        symbol = kwargs.get('symbol', 'UNKNOWN')
        side = kwargs.get('side', 'BUY')
        order_type = kwargs.get('type', 'MARKET')
        quantity = kwargs.get('quantity', 0)
        price = kwargs.get('price')

        # Generate realistic mock response
        order_id = random.randint(100000000, 999999999)
        
        # Simulate market price if not provided
        if not price:
            # Mock market prices for common pairs
            mock_prices = {
                'BTCUSDT': 65000.00,
                'ETHUSDT': 3200.00,
                'BNBUSDT': 580.00,
            }
            price = mock_prices.get(symbol, 50000.00)
        
        # Market orders fill immediately, limit orders are NEW
        status = "FILLED" if order_type == "MARKET" else "NEW"
        executed_qty = str(quantity) if order_type == "MARKET" else "0"
        avg_price = str(price) if order_type == "MARKET" else "0"

        response = {
            "orderId": order_id,
            "symbol": symbol,
            "status": status,
            "clientOrderId": f"mock_{int(time.time())}",
            "price": str(price),
            "avgPrice": avg_price,
            "origQty": str(quantity),
            "executedQty": executed_qty,
            "cumQty": executed_qty,
            "cumQuote": str(float(executed_qty) * float(price)) if executed_qty != "0" else "0",
            "timeInForce": kwargs.get('timeInForce', 'GTC'),
            "type": order_type,
            "reduceOnly": False,
            "closePosition": False,
            "side": side,
            "positionSide": "BOTH",
            "stopPrice": "0",
            "workingType": "CONTRACT_PRICE",
            "priceProtect": False,
            "origType": order_type,
            "updateTime": int(time.time() * 1000)
        }

        logger.info(f"🎭 Mock order simulated - Order ID: {order_id}, Status: {status}")
        return response
