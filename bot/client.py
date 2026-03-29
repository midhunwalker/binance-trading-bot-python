"""Binance Futures API client wrapper with automatic fallback to mock"""

import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def get_client():
    """
    Get Binance Futures client with automatic fallback to mock.
    
    Returns:
        BinanceFuturesClient or MockBinanceFuturesClient
    """
    try:
        # Try to import and initialize real Binance client
        from binance.client import Client
        from binance.exceptions import BinanceAPIException, BinanceRequestException
        import requests.exceptions
        
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_SECRET_KEY')
        base_url = os.getenv('BASE_URL', 'https://testnet.binancefuture.com')

        # If no credentials, fall back to mock immediately
        if not api_key or not api_secret:
            logger.warning("No API credentials found in .env - using Mock Client")
            from bot.mock_client import MockBinanceFuturesClient
            return MockBinanceFuturesClient()

        # Try to initialize real client
        try:
            client = Client(api_key, api_secret)
            client.API_URL = base_url
            
            # Test connection
            logger.info("Testing connection to Binance Futures API...")
            client.futures_ping()
            
            logger.info(f"✅ Connected to Binance Futures API: {base_url}")
            return BinanceFuturesClient(client, base_url)
            
        except (BinanceAPIException, BinanceRequestException, 
                requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout) as e:
            logger.warning(f"Binance API unavailable: {e}")
            logger.warning("⚠️  FALLBACK: Using Mock Client (Binance API unavailable)")
            from bot.mock_client import MockBinanceFuturesClient
            return MockBinanceFuturesClient()
            
    except ImportError as e:
        logger.warning(f"Binance library not available: {e}")
        logger.warning("⚠️  FALLBACK: Using Mock Client (Dependencies missing)")
        from bot.mock_client import MockBinanceFuturesClient
        return MockBinanceFuturesClient()
    
    except Exception as e:
        logger.error(f"Unexpected error initializing client: {e}")
        logger.warning("⚠️  FALLBACK: Using Mock Client (Initialization failed)")
        from bot.mock_client import MockBinanceFuturesClient
        return MockBinanceFuturesClient()


class BinanceFuturesClient:
    """Wrapper for Binance Futures API operations"""

    def __init__(self, client, base_url):
        """
        Initialize with existing Binance client.
        
        Args:
            client: Initialized Binance Client instance
            base_url: API base URL
        """
        self.client = client
        self.base_url = base_url

    def test_connection(self):
        """
        Test connection to Binance Futures API.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            from binance.exceptions import BinanceAPIException
            import requests.exceptions
            
            logger.info("Testing connection to Binance Futures API...")
            self.client.futures_ping()
            logger.info("✅ Connection to Binance Futures API successful")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {type(e).__name__}: {e}")
            return False

    def place_order(self, **kwargs):
        """
        Place an order on Binance Futures.

        Args:
            **kwargs: Order parameters (symbol, side, type, quantity, price, etc.)

        Returns:
            Order response from Binance

        Raises:
            ValueError: If API error occurs
            ConnectionError: If network issue occurs
        """
        try:
            from binance.exceptions import BinanceAPIException, BinanceRequestException
            import requests.exceptions
            
            logger.debug(f"Placing order with parameters: {kwargs}")
            order = self.client.futures_create_order(**kwargs)
            logger.info(f"✅ Order placed successfully - ID: {order.get('orderId')}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message} (Code: {e.code})")
            raise ValueError(f"Binance API error: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {e.message}")
            raise ValueError(f"Request error: {e.message}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network connection error: {e}")
            raise ConnectionError("Unable to connect to Binance API. Check your internet connection.")
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {e}")
            raise TimeoutError("Request to Binance API timed out. Try again later.")
        except Exception as e:
            logger.error(f"Unexpected error placing order: {type(e).__name__}: {e}")
            raise
