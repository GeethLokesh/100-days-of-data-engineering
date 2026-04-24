import os
import sqlite3
import pandas as pd

DATA_FILE = "data/sales_data.csv"
OUTPUT_DIR = "output"
DB_FILE = os.path.join(OUTPUT_DIR, "sales.db")

def load_csv_to_sqlite():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_FILE)
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data loaded into SQLite database at: {DB_FILE}")

if __name__ == "__main__":
    load_csv_to_sqlite()

