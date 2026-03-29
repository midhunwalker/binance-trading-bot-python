"""Binance Futures API client wrapper"""

import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """Wrapper for Binance Futures API operations"""

    def __init__(self):
        """Initialize Binance Futures client with testnet configuration"""
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_SECRET_KEY')
        base_url = os.getenv('BASE_URL', 'https://testnet.binancefuture.com')

        if not api_key or not api_secret:
            raise ValueError("BINANCE_API_KEY and BINANCE_SECRET_KEY must be set in .env file")

        self.client = Client(api_key, api_secret)
        self.client.API_URL = base_url
        
        logger.info(f"Initialized Binance Futures client with base URL: {base_url}")

    def place_order(self, **kwargs):
        """
        Place an order on Binance Futures.

        Args:
            **kwargs: Order parameters (symbol, side, type, quantity, price, etc.)

        Returns:
            Order response from Binance

        Raises:
            BinanceAPIException: If order placement fails
        """
        try:
            order = self.client.futures_create_order(**kwargs)
            logger.info(f"Order placed successfully: {order.get('orderId')}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Failed to place order: {e}")
            raise
