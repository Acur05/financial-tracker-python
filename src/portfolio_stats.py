import pandas as pd
import yfinance as yf
import logging

logging.getLogger('yfinance').setLevel(logging.CRITICAL)

class PortfolioStats:
    def __init__(self, df):
        self.df = df
        self._sector_cache = {}

    def get_sector_from_api(self, ticker):
        if ticker in self._sector_cache:
            return self._sector_cache[ticker]

        attempts = [ticker, f"{ticker}.DE", f"{ticker}.AS"]

        for symbol in attempts:
            try:
                t = yf.Ticker(symbol)
                info = t.info

                sector = info.get('sector')
                if not sector:
                    sector = info.get('quoteType')

                if sector and sector != 'None':
                    self._sector_cache[ticker] = sector
                    return sector
            except:
                continue

        return "ETF/Outros"

    def get_sector_allocation(self):
        buys = self.df[self.df['Action'] == 'Market buy'].copy()

        unique_tickers = buys['Ticker'].unique()
        ticker_to_sector = {t: self.get_sector_from_api(t) for t in unique_tickers}

        buys['Sector'] = buys['Ticker'].map(ticker_to_sector)

        return buys.groupby('Sector')['Total'].sum().sort_values(ascending=False).reset_index()

    def get_allocation(self):
        """Calcula quanto dinheiro tens investido em cada Ticker (Ação/ETF)"""

        buys = self.df[self.df['Action'] == 'Market buy']

        allocation = buys.groupby('Ticker')['Total'].sum().sort_values(ascending=False)

        total_invested = allocation.sum()
        weights = (allocation / total_invested) * 100

        return pd.DataFrame({
            'Investido (EUR)': allocation,
            'Peso no portfolio (%)': weights
        })

    def get_dividend_yield_on_cost(self):
        """Calcula o rendimento de dividendos face ao que pagaste"""
        div_mask = self.df['Action'].str.contains('Dividend', na=False)
        total_dividends = self.df[div_mask]['Total'].sum()

        total_invested = self.df[self.df['Action'] == 'Market buy']['Total'].sum()

        if total_invested == 0: return 0
        return (total_dividends / total_invested) * 100

    def print_stats(self):
        print("\n--- ESTATÍSTICAS DA CARTEIRA ---")
        print(f"Dividend Yield on Cost: {self.get_dividend_yield_on_cost():.2f}%")
        print("\nAlocação por Ativo:")
        print(self.get_allocation().round(2).to_string(
            index=True))