"""Input validation utilities"""


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: Order side ('BUY' or 'SELL')

    Returns:
        Uppercase side

    Raises:
        ValueError: If side is invalid
    """
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.

    Args:
        order_type: Order type ('MARKET' or 'LIMIT')

    Returns:
        Uppercase order type

    Raises:
        ValueError: If order type is invalid
    """
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError(f"Invalid order type '{order_type}'. Must be 'MARKET' or 'LIMIT'")
    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate order quantity.

    Args:
        quantity: Order quantity

    Returns:
        Validated quantity

    Raises:
        ValueError: If quantity is invalid
    """
    if not isinstance(quantity, (int, float)):
        raise ValueError(f"Quantity must be a number, got {type(quantity).__name__}")
    
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {quantity}")
    
    return float(quantity)


def validate_price(price: float, order_type: str) -> float:
    """
    Validate price for order.

    Args:
        price: Order price
        order_type: Type of order ('MARKET' or 'LIMIT')

    Returns:
        Validated price

    Raises:
        ValueError: If price is invalid
    """
    order_type = order_type.upper()
    
    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        
        if not isinstance(price, (int, float)):
            raise ValueError(f"Price must be a number, got {type(price).__name__}")
        
        if price <= 0:
            raise ValueError(f"Price must be greater than 0, got {price}")
    
    return float(price) if price is not None else None
