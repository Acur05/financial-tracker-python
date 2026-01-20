from datetime import datetime


def export_final_report(tax_summary, sector_df, asset_df, yield_on_cost):
    """Gera o ficheiro TXT formatado com os resultados"""
    filename = f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d')}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("==========================================\n")
        f.write("      RELATÓRIO DE INVESTIMENTOS PRO      \n")
        f.write(f"      Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("==========================================\n\n")

        f.write(f"RENDIMENTO (Yield on Cost): {yield_on_cost:.2f}%\n\n")

        f.write("ESTIMATIVA FISCAL (IRS PT)\n")
        f.write(f"Vendas: {tax_summary['gains']['profit']:.2f}€ | Imposto: {tax_summary['gains']['tax_due']:.2f}€\n")
        f.write(
            f"Divs:   {tax_summary['divs']['gross_amount']:.2f}€ | Imposto PT: {tax_summary['divs']['pt_tax_due']:.2f}€\n")
        f.write(f"TOTAL A RESERVAR: {tax_summary['total_tax']:.2f}€\n\n")

        f.write("ALOCAÇÃO POR SECTOR\n")
        f.write(sector_df.to_string(index=False))
        f.write("\n\n")

        f.write("DETALHE POR ATIVO\n")
        f.write(asset_df.to_string(index=True))

    return filename


def perguntar_exportacao():
    """Gere a interação com o utilizador"""
    escolha = input("\nDeseja exportar o relatório para um ficheiro .txt? (s/n): ").lower()
    return escolha == 's'