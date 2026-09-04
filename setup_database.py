import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:Neeharika%402005@localhost:5432/maya_db"

engine = create_engine(DATABASE_URL)

DATA_DIR = "./data"


def load_table(filename, table_name):
    print(f"Loading {filename}...")

    df = pd.read_csv(f"{DATA_DIR}/{filename}")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"  {table_name}: {len(df):,} rows")


def main():

    print("=" * 60)
    print("MAYA DATABASE SETUP")
    print("=" * 60)

    load_table(
        "customers.csv",
        "customers"
    )

    load_table(
        "products.csv",
        "products"
    )

    load_table(
        "orders.csv",
        "orders"
    )

    load_table(
        "order_items.csv",
        "order_items"
    )

    load_table(
        "campaigns.csv",
        "campaigns"
    )

    load_table(
        "customer_segments.csv",
        "customer_segments"
    )

    print()
    print("=" * 60)
    print("VERIFYING DATABASE")
    print("=" * 60)

    with engine.connect() as connection:

        tables = [
            "customers",
            "products",
            "orders",
            "order_items",
            "campaigns",
            "customer_segments"
        ]

        for table in tables:

            result = connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            )

            count = result.scalar()

            print(f"{table:20} {count:,} rows")

    print()
    print("MAYA DATABASE READY.")


if __name__ == "__main__":
    main()