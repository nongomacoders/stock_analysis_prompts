"""CLI Runner for LEW (LEW) 2-Year Forecast."""

from .config import TICKER, COMPANY_NAME

def main():
    print(f'=== 2-Year Analyst Forecast Model: {COMPANY_NAME} ({TICKER}) ===')
    print('To run full valuation, populate baseline metrics from documents/analysis.sqlite.')

if __name__ == '__main__':
    main()
