from trading.portfolio.client import PortfolioClient
from trading.sheets.client import SpreadsheetClient


class SpreadsheetSyncerWorker:
    def __init__(self, sheet_client: SpreadsheetClient, portfolio_client: PortfolioClient):
        self.sheet_client = sheet_client
        self.portfolio_client = portfolio_client

    def run(self):
        holdings = self.portfolio_client.get_holdings()
        self.sheet_client.build_holdings_sheet(holdings)