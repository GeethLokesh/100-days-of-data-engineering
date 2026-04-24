import os
import pandas as pd


DATA_DIR ="data"
FILE_PATH = os.path.join(DATA_DIR, "sales_data.csv")

def create_sales_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    sales_data = [
        [1001, "2026-04-01", "C001", "Laptop", "Electronics", 1, 850.00, "Card"],
        [1002, "2026-04-01", "C002", "Mouse", "Electronics", 2, 25.00, "UPI"],
        [1003, "2026-04-02", "C003", "Desk Chair", "Furniture", 1, 120.00, "Card"],
        [1004, "2026-04-02", "C004", "Notebook", "Stationery", 5, 3.50, "Cash"],
        [1005, "2026-04-03", "C005", "Pen Pack", "Stationery", 3, 4.00, "UPI"],
        [1006, "2026-04-03", "C006", "Monitor", "Electronics", 1, 220.00, "Card"],
        [1007, "2026-04-04", "C007", "Desk", "Furniture", 1, 180.00, "Cash"],
        [1008, "2026-04-04", "C008", "Keyboard", "Electronics", 2, 45.00, "UPI"],
        [1009, "2026-04-05", "C009", "Water Bottle", "Accessories", 4, 12.00, "Cash"],
        [1010, "2026-04-05", "C010", "Backpack", "Accessories", 1, 40.00, "Card"],
        [1011, "2026-04-06", "C011", "Lamp", "Furniture", 2, 35.00, "UPI"],
        [1012, "2026-04-06", "C012", "USB Cable", "Electronics", 3, 10.00, "Card"],
        [1013, "2026-04-07", "C013", "Sticky Notes", "Stationery", 6, 2.50, "Cash"],
        [1014, "2026-04-07", "C014", "Office Bag", "Accessories", 2, 55.00, "Card"],
        [1015, "2026-04-08", "C015", "Tablet", "Electronics", 1, 300.00, "UPI"]
    ]

    columns = [
        "order_id",
        "order_date",
        "customer_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "payment_method"
    ]

    df = pd.DataFrame(sales_data, columns=columns)

    df.to_csv(FILE_PATH, index=False)
    print(f"Sample sales data created at: {FILE_PATH}")

if __name__ == "__main__":
    create_sales_data()
