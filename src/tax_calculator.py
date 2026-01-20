import pandas as pd


class TaxCalculator:
    def __init__(self, df, tax_rate=0.28):
        self.df = df
        self.tax_rate = tax_rate

    def calculate_capital_gains_tax(self):
        """Calcula imposto sobre lucros de vendas (Mais-valias)"""
        sales = self.df[self.df['Action'] == 'Market sell']
        total_profit = sales['Result'].sum()

        tax_due = max(0, total_profit * self.tax_rate)

        return {
            "profit": total_profit,
            "tax_due": tax_due
        }

    def calculate_dividends_tax(self):
        """Calcula imposto sobre dividendos (considerando retenção na fonte)"""
        div_mask = self.df['Action'].str.contains('Dividend', na=False)
        dividends_df = self.df[div_mask]

        gross_dividends = dividends_df['Total'].sum()
        tax_withheld_abroad = dividends_df['Withholding tax'].sum()

        total_tax_target = gross_dividends * self.tax_rate
        pt_tax_due = max(0, total_tax_target - tax_withheld_abroad)

        return {
            "gross_amount": gross_dividends,
            "withheld_abroad": tax_withheld_abroad,
            "pt_tax_due": pt_tax_due
        }

    def full_report(self):
        gains = self.calculate_capital_gains_tax()
        divs = self.calculate_dividends_tax()

        print("\n--- CALCULADORA FISCAL (Para Portugal) ---")
        print(f"MAIS-VALIAS: Lucro de {gains['profit']:.2f}€ -> Imposto: {gains['tax_due']:.2f}€")
        print(f"DIVIDENDOS: Bruto de {divs['gross_amount']:.2f}€ -> Imposto PT: {divs['pt_tax_due']:.2f}€")
        print(f"TOTAL A RESERVAR PARA O ESTADO: {gains['tax_due'] + divs['pt_tax_due']:.2f}€")