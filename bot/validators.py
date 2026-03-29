"""Input validation utilities"""

import re
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading pair symbol format.

    Args:
        symbol: Trading pair symbol

    Returns:
        Uppercase symbol

    Raises:
        ValidationError: If symbol format is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper()
    
    # Basic pattern for crypto pairs (e.g., BTCUSDT, ETHUSDT)
    if not re.match(r'^[A-Z0-9]{3,}USDT?$', symbol):
        raise ValidationError(f"Invalid symbol format: {symbol}")
    
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: Order side ('buy' or 'sell')

    Returns:
        Uppercase side

    Raises:
        ValidationError: If side is invalid
    """
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")
    return side


def validate_quantity(quantity: float, min_qty: float = 0.0) -> float:
    """
    Validate order quantity.

    Args:
        quantity: Order quantity
        min_qty: Minimum allowed quantity

    Returns:
        Validated quantity

    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity: {quantity}")
    
    if qty <= min_qty:
        raise ValidationError(f"Quantity must be greater than {min_qty}")
    
    return qty


def validate_price(price: float) -> float:
    """
    Validate price value.

    Args:
        price: Price value

    Returns:
        Validated price

    Raises:
        ValidationError: If price is invalid
    """
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price: {price}")
    
    if p <= 0:
        raise ValidationError("Price must be greater than 0")
    
    return p


def validate_api_credentials(api_key: Optional[str], api_secret: Optional[str]) -> None:
    """
    Validate API credentials.

    Args:
        api_key: Binance API key
        api_secret: Binance API secret

    Raises:
        ValidationError: If credentials are missing or invalid
    """
    if not api_key or not api_secret:
        raise ValidationError("API key and secret are required")
    
    if len(api_key) < 10 or len(api_secret) < 10:
        raise ValidationError("Invalid API credentials format")
