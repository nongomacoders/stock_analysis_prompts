"""CLI Runner for Orion Minerals (ORN) 2-Year Forecast."""

from .config import TICKER, COMPANY_NAME, SECTOR

def main():
    print(f'=== 2-Year Analyst Forecast Model: {COMPANY_NAME} ({TICKER}) [{SECTOR.upper()}] ===')
    print('To run full valuation, populate baseline metrics from documents/analysis.sqlite.')

if __name__ == '__main__':
    main()
