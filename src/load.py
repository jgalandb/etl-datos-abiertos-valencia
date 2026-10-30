import sqlite3
from pathlib import Path

from extract import extract
from transform import transform

RUTA_DB = Path(__file__).resolve().parent.parent / "data" / "edificios.db"


def load(edificios, registros):
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(RUTA_DB) as conexion:
        edificios.to_sql("edificios", conexion, if_exists="replace", index=False)
        registros.to_sql("registros", conexion, if_exists="replace", index=False)

        conexion.execute("CREATE INDEX idx_edificios_refcat ON edificios (refcat)")
        conexion.execute("CREATE INDEX idx_registros_refcat ON registros (refcat)")

    print(f"Base de datos creada en {RUTA_DB}")
    print(f"Tabla edificios: {len(edificios)} filas")
    print(f"Tabla registros: {len(registros)} filas")


if __name__ == "__main__":
    edificios, registros = transform(extract())
    load(edificios, registros)