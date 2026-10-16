from pathlib import Path

import pandas as pd

RUTA_CSV = Path("data/raw/edificios.csv")


def extract():
    if not RUTA_CSV.exists():
        raise FileNotFoundError(
            f"No encuentro {RUTA_CSV}. Descarga el CSV y colócalo en data/raw/"
        )
    try:
        df = pd.read_csv(RUTA_CSV, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(RUTA_CSV, sep=None, engine="python", encoding="latin-1")

    #utilizo tryexcept por si viene con codificacion y los acentos raros, que a veces pasa en datos de admin.

    print(f"Leídas {len(df)} filas y {len(df.columns)} columnas")
    print("\nColumnas:")
    print(df.columns.tolist())
    print("\nPrimeras filas:")
    print(df.head())
    print("\nValores nulos por columna:")
    print(df.isnull().sum())
    return df

if __name__ == "__main__":
    extract()