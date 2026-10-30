from pathlib import Path

import pandas as pd

from extract import extract

SALIDA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

COLUMNAS_FECHA = ["f_ord_indi", "f_dogv", "f_resolu", "ap_s_lic_f", "ad_c_deb_f"]


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
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip().replace("", pd.NA)
    return df


def limpiar_referencias_registro(df):
    """Libro, tomo, folio y finca son identificadores: se guardan como texto."""
    df = df.copy()
    cols = [
        c for c in df.columns
        if c.startswith(("l_reg_", "t_reg_", "f_reg_", "fi_reg_"))
    ]
    for col in cols:
        df[col] = (
            df[col].astype("string")
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
            .replace("", pd.NA)
        )
    return df


def convertir_fechas(df):
    """Las fechas del CSV vienen como milisegundos desde 1970."""
    df = df.copy()
    for col in COLUMNAS_FECHA:
        if col not in df.columns:
            continue
        numeros = pd.to_numeric(df[col], errors="coerce")
        antes = df[col].notna().sum()
        df[col] = pd.to_datetime(numeros, unit="ms", errors="coerce")
        despues = df[col].notna().sum()
        if despues < antes:
            print(f"Aviso: {col} perdió {antes - despues} fechas al convertir")
    return df


def registros_a_largo(df):
    """Convierte las columnas l_reg_01..10, t_reg_01..10, etc. en una fila por registro."""
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

    invalidas = df[df["refcat"].str.len() != 14]
    if not invalidas.empty:
        print(f"Aviso: {len(invalidas)} referencias catastrales con longitud distinta de 14")

    df = limpiar_referencias_registro(df)
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