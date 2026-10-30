from extract import extract
from transform import transform
from load import load


def main():
    df = extract()
    edificios, registros = transform(df)
    load(edificios, registros)
    print("\nPipeline completado.")


if __name__ == "__main__":
    main()