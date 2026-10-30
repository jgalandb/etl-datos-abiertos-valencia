from pathlib import Path

import pandas as pd

from extract import extract

SALIDA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def limpiar_nombres(df):
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def limpiar_textos(df):
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().replace("", pd.NA)
    return df

invalidas = df[df["refcat"].str.len() != 14]
if not invalidas.empty:
    print(f"Aviso: {len(invalidas)} referencias catastrales con longitud distinta de 14")


def convertir_fechas(df):
    df = df.copy()
    cols_fecha = [c for c in df.columns if c.startswith(("f_", "fi_")) or c.endswith("_f")]
    for col in cols_fecha:
        antes = df[col].notna().sum()
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        despues = df[col].notna().sum()
        if despues < antes:
            print(f"Aviso: {col} perdió {antes - despues} fechas al convertir")
    return df


def registros_a_largo(df):
    bloques = []
    for i in range(1, 11):
        n = f"{i:02d}"
        columnas = {
            f"l_reg_{n}": "l_reg",
            f"t_reg_{n}": "t_reg",
            f"f_reg_{n}": "f_reg",
            f"fi_reg_{n}": "fi_reg",
        }
        sub = df[["refcat"] + list(columnas)].rename(columns=columnas)
        sub["orden"] = i
        bloques.append(sub)

    largo = pd.concat(bloques, ignore_index=True)
    vacias = largo[["l_reg", "t_reg", "f_reg", "fi_reg"]].isna().all(axis=1)
    return largo[~vacias].sort_values(["refcat", "orden"]).reset_index(drop=True)


def transform(df):
    df = limpiar_nombres(df)
    df = limpiar_textos(df)
    df = convertir_fechas(df)
    df = df.drop_duplicates(subset="refcat")

    registros = registros_a_largo(df)
    columnas_wide = [
        c for c in df.columns
        if c.startswith(("l_reg_", "t_reg_", "f_reg_", "fi_reg_"))
    ]
    edificios = df.drop(columns=columnas_wide)
    return edificios, registros


if __name__ == "__main__":
    SALIDA_DIR.mkdir(parents=True, exist_ok=True)
    edificios, registros = transform(extract())

    edificios.to_csv(SALIDA_DIR / "edificios_limpio.csv", index=False)
    registros.to_csv(SALIDA_DIR / "registros.csv", index=False)

    print(f"\nEdificios: {edificios.shape[0]} filas, {edificios.shape[1]} columnas")
    print(f"Registros: {registros.shape[0]} filas")
    print(registros.head(10))

