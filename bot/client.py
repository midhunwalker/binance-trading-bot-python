"""Binance Futures API client wrapper"""

import logging
from typing import Dict, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """Wrapper for Binance Futures API operations"""

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        """
        Initialize Binance Futures client.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet if True
        """
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.testnet = testnet
        logger.info(f"Initialized Binance Futures client (testnet={testnet})")

    def get_account_balance(self) -> Dict:
        """Get futures account balance"""
        try:
            return self.client.futures_account_balance()
        except BinanceAPIException as e:
            logger.error(f"Error fetching account balance: {e}")
            raise

    def get_position_info(self, symbol: Optional[str] = None) -> Dict:
        """
        Get current position information.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT'). If None, returns all positions.
        """
        try:
            positions = self.client.futures_position_information(symbol=symbol)
            return positions
        except BinanceAPIException as e:
            logger.error(f"Error fetching position info: {e}")
            raise

    def get_symbol_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            raise
