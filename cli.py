"""CLI interface for Binance Futures Trading Bot"""

import typer
from typing import Optional
from bot.logging_config import setup_logging

app = typer.Typer()


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
    typer.echo(f"📊 Trade Command Received")
    typer.echo(f"Symbol: {symbol}")
    typer.echo(f"Side: {side}")
    typer.echo(f"Type: {order_type}")
    typer.echo(f"Quantity: {quantity}")
    if price:
        typer.echo(f"Price: {price}")
    
    # TODO: Integrate order execution logic


def main():
    """Main CLI entry point"""
    setup_logging()
    app()


if __name__ == '__main__':
    main()
