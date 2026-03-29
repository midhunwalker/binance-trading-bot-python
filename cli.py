"""CLI interface for Binance Futures Trading Bot"""

import typer
import sys
from typing import Optional
from bot.logging_config import setup_logging
from bot.validators import validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import place_market_order, place_limit_order

app = typer.Typer()


def print_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None):
    """Print order summary before execution"""
    typer.echo("\n" + "="*60)
    typer.echo("===  ORDER REQUEST  ===")
    typer.echo("="*60)
    typer.echo(f"  Symbol:      {symbol}")
    typer.echo(f"  Side:        {side}")
    typer.echo(f"  Type:        {order_type}")
    typer.echo(f"  Quantity:    {quantity}")
    if price:
        typer.echo(f"  Price:       {price}")
    typer.echo("="*60 + "\n")


def print_order_response(response: dict):
    """Print formatted order response"""
    typer.echo("\n" + "="*60)
    typer.echo("===  ORDER RESULT  ===")
    typer.echo("="*60)
    typer.echo(f"  Order ID:       {response.get('orderId', 'N/A')}")
    typer.echo(f"  Status:         {response.get('status', 'N/A')}")
    typer.echo(f"  Executed Qty:   {response.get('executedQty', 'N/A')}")
    typer.echo(f"  Avg Price:      {response.get('avgPrice', 'N/A')}")
    typer.echo("="*60 + "\n")


def print_error(message: str):
    """Print formatted error message"""
    typer.echo("\n" + "="*60)
    typer.echo("===  ERROR  ===")
    typer.echo("="*60)
    for line in message.split('\n'):
        typer.echo(f"  {line}")
    typer.echo("="*60 + "\n")


@app.command()
def trade(
    symbol: str = typer.Argument(..., help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    order_type: str = typer.Argument(..., help="Order type (MARKET or LIMIT)"),
    quantity: float = typer.Argument(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, help="Limit price (required for LIMIT orders)")
):
    """
    Place a trade on Binance Futures.
    """
    try:
        # Validate inputs
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(price, order_type)
        
        # Print order summary
        print_order_summary(symbol, side, order_type, quantity, price)
        
        # Execute order based on type
        if order_type == 'MARKET':
            response = place_market_order(symbol, side, quantity)
        elif order_type == 'LIMIT':
            response = place_limit_order(symbol, side, quantity, price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")
        
        # Print success response
        print_order_response(response)
        
    except ValueError as e:
        print_error(f"Validation Error: {str(e)}")
        sys.exit(1)
    except ConnectionError as e:
        print_error(f"Network Error: {str(e)}\n\nPlease check your internet connection and try again.")
        sys.exit(1)
    except TimeoutError as e:
        print_error(f"Timeout Error: {str(e)}\n\nThe request took too long. Please try again.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected Error: {str(e)}\n\nPlease check the logs for more details.")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    setup_logging()
    app()


if __name__ == '__main__':
    setup_logging()
    app()
