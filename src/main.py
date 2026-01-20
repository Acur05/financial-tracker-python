from src.data_loader import load_and_clean_data
from src.tax_calculator import TaxCalculator
from src.portfolio_stats import PortfolioStats
from src.reporter import export_final_report, perguntar_exportacao


def main():
    print("A iniciar motor de análise financeira...")

    try:
        df = load_and_clean_data()
        stats = PortfolioStats(df)
        tax_calc = TaxCalculator(df)

        print("A consultar API do Yahoo Finance para classificação...")
        sector_data = stats.get_sector_allocation()
        asset_data = stats.get_allocation()
        yoc = stats.get_dividend_yield_on_cost()

        tax_calc.full_report()
        print(f"\nRENDIMENTO (Yield on Cost): {yoc:.2f}%")

        print("\nDETALHE POR ATIVO:")
        print(asset_data.round(2).to_string(index=True))
        # ----------------------------------

        print("\n ALOCAÇÃO POR SECTOR:")
        print(sector_data.round(2).to_string(index=False))

        if perguntar_exportacao():
            gains = tax_calc.calculate_capital_gains_tax()
            divs = tax_calc.calculate_dividends_tax()

            tax_summary = {
                'gains': gains,
                'divs': divs,
                'total_tax': gains['tax_due'] + divs['pt_tax_due']
            }

            nome_relatorio = export_final_report(
                tax_summary,
                sector_data.round(2),
                asset_data.round(2),
                yoc
            )
            print(f"Relatório guardado como: {nome_relatorio}")
        else:
            print("Exportação ignorada.")

    except Exception as e:
        print(f" Erro Crítico no Sistema: {e}")


if __name__ == "__main__":
    main()