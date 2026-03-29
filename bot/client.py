"""Binance Futures API client wrapper"""

import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
import requests.exceptions

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
            error_msg = "BINANCE_API_KEY and BINANCE_SECRET_KEY must be set in .env file"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self.client = Client(api_key, api_secret)
            self.client.API_URL = base_url
            logger.info(f"Initialized Binance Futures client with base URL: {base_url}")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise

    def test_connection(self):
        """
        Test connection to Binance Futures API.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info("Testing connection to Binance Futures API...")
            self.client.futures_ping()
            logger.info("✅ Connection to Binance Futures API successful")
            return True
        except BinanceAPIException as e:
            logger.error(f"❌ Binance API error during connection test: {e.message} (Code: {e.code})")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ Network connection error: Unable to reach Binance Futures API")
            return False
        except requests.exceptions.Timeout:
            logger.error("❌ Connection timeout: Binance Futures API did not respond in time")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during connection test: {type(e).__name__}: {e}")
            return False

    def place_order(self, **kwargs):
        """
        Place an order on Binance Futures.

        Args:
            **kwargs: Order parameters (symbol, side, type, quantity, price, etc.)

        Returns:
            Order response from Binance

        Raises:
            BinanceAPIException: If order placement fails
            ConnectionError: If network issue occurs
        """
        try:
            logger.debug(f"Placing order with parameters: {kwargs}")
            order = self.client.futures_create_order(**kwargs)
            logger.info(f"✅ Order placed successfully - ID: {order.get('orderId')}")
            return order
        except BinanceAPIException as e:
            logger.error(f"❌ Binance API error: {e.message} (Code: {e.code})")
            raise ValueError(f"Binance API error: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"❌ Binance request error: {e.message}")
            raise ValueError(f"Request error: {e.message}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Network connection error: {e}")
            raise ConnectionError("Unable to connect to Binance API. Check your internet connection.")
        except requests.exceptions.Timeout as e:
            logger.error(f"❌ Request timeout: {e}")
            raise TimeoutError("Request to Binance API timed out. Try again later.")
        except Exception as e:
            logger.error(f"❌ Unexpected error placing order: {type(e).__name__}: {e}")
            raise
