# ETL de datos abiertos de Valencia

Pequeño proyecto para practicar el ciclo completo de un pipeline de datos: descargar datos públicos del Ayuntamiento de Valencia, limpiarlos y guardarlos en una base de datos para poder consultarlos con SQL.

Lo empecé para aprender ingeniería de datos con un caso real, y lo voy ampliando por fases. Más abajo explico qué está hecho y qué falta.

## Datos que uso

Trabajo con el dataset **[Libro Registro Edificios]**, publicado en el portal de datos abiertos del Ayuntamiento de Valencia ([opendata.vlci.valencia.es](https://opendata.vlci.valencia.es/dataset/libro-registro-edificios-llibre-registre-edificis)). Lo elegí porque la vivienda es ahora un tema bastante candente y me parece interesante poder trabajar sobre datos de este tipo para consultas o analisis.

## Cómo está organizado

```
etl-datos-abiertos-valencia/
├── data/
│   ├── raw/            # CSV descargado
│   └── processed/      # Datos limpios
├── src/
│   ├── extract.py      # Lee el CSV
│   └── transform.py    # Limpia y reestructura los datos 
├── requirements.txt
└── README.md
```

## Estado del proyecto

- [x] **Extract:** descarga del CSV desde el portal de datos abiertos
- [x] **Transform:** limpieza de columnas, tipos de datos, nulos y duplicados con pandas
- [ ] **Load:** carga en PostgreSQL con un modelo de tablas sencillo
- [ ] Un `main.py` que ejecute todo el proceso de seguido
- [ ] Automatización diaria con Airflow y Docker

Voy marcando cada punto según lo termino.

## Tecnologías

- Python 3
- pandas
- requests
- Git y GitHub

Más adelante: PostgreSQL, Docker y Airflow.

## Cómo lo he ejecutado

Lo primero ha sido tener Python y Git instalados.

1. Clonaje del repositorio:
```bash
   git clone https://github.com/[jgalandb]/etl-datos-abiertos-valencia.git
   cd etl-datos-abiertos-valencia
```

2. Creación y activacionj un entorno virtual:
```bash
   python -m venv venv
   venv\Scripts\activate      
   
```

3. Instalación de las dependencias:
```bash
   pip install -r requirements.txt
```

4. Comprobación de que el CSV del Libro Registro de Edificios está en `data/raw/edificios.csv`.

5. Lanzamiento de la extracción para comprobar que el archivo se lee bien:
   ```bash
   python src/extract.py
   ```
   Imprime el número de filas y columnas, los nombres de las columnas y los valores nulos.

6. Lanzamiento de la transformación:
   ```bash
   python src/transform.py
   ```
   Limpia los datos y genera dos archivos en `data/processed/`:
   - `edificios_limpio.csv`: una fila por inmueble.
   - `registros.csv`: una fila por cada registro asociado a un inmueble, relacionada con la tabla anterior por la referencia catastral (`refcat`).

Comprobando que todo vaya bien, creo el archivo `data/raw/edificios.csv` y el script imprime en pantalla cuántas filas ha descargado.

## Lo que estoy aprendiendo

- Manejar Git y GitHub de forma habitual (commits pequeños, mensajes claros).
- Separar un proceso de datos en fases independientes en lugar de hacerlo todo en un único script.
- Trabajar con entornos virtuales y mantener las dependencias controladas.

## Contacto

[Jorge Galán] · [LinkedIn](https://www.linkedin.com/in/[jorgegalandelblanco/]) · [jgalandb@gmail.com]