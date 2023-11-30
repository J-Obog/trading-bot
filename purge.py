import os
import dotenv
from trading.data import HoldingType, Order, OrderType
from trading.wallstreet import WallStreetSurvivorClient

dotenv.load_dotenv()

portfolio_client = WallStreetSurvivorClient(os.getenv("COOKIE"))


holdings = portfolio_client.get_holdings()

for holding in holdings:
    order_type = OrderType.SELL if holding.holding_type == HoldingType.LONG else OrderType.BUY_TO_COVER
    order = Order(holding.quantity, holding.symbol, order_type)

    portfolio_client.place_order(order)