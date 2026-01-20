import pandas as pd
import os
import glob

def load_and_clean_data():

    folder_path = os.path.join(os.path.dirname(__file__), "..", "data")

    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"Nenhum ficheiro CSV encontrado na pasta: {folder_path}")

    latest_file = max(csv_files, key=os.path.getmtime)

    print(f" A ler o ficheiro mais recente: {os.path.basename(latest_file)}")

    df = pd.read_csv(latest_file)

    df.columns = df.columns.str.strip()

    df['Time'] = pd.to_datetime(df['Time'])

    cols_financeiras = ['Total', 'Result', 'Withholding tax', 'No. of shares']
    for col in cols_financeiras:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    df['Month_Year'] = df['Time'].dt.to_period('M')

    return df
