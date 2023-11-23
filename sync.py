import os
import dotenv
from trading.airtable import AirtableClient
from trading.wallstreet import WallStreetSurvivorClient
    
dotenv.load_dotenv()

portfolio_client = WallStreetSurvivorClient(os.getenv("COOKIE"))
ssheet_client = AirtableClient(os.getenv("AIRTABLE_ACCESS_TOKEN"))

holdings = portfolio_client.get_holdings()
ssheet_client.build_holdings_sheet(holdings)
print("Updated portfolio with holdings: ", holdings)