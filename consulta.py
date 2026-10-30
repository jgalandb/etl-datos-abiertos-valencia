import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent / "data" / "edificios.db"

con = sqlite3.connect(RUTA_DB)
cursor = con.execute(
    """
    SELECT e.refcat, e.nombarrio, COUNT(r.refcat) AS num_registros
    FROM edificios e
    LEFT JOIN registros r ON e.refcat = r.refcat
    GROUP BY e.refcat, e.nombarrio
    ORDER BY num_registros DESC
    """
)
for fila in cursor:
    print(fila)
con.close()