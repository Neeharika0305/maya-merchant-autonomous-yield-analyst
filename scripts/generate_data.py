import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = Path("../data")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. PRODUCTS
# ============================================================

products = pd.DataFrame([
    ["P001", "Wireless Earbuds", "Audio", 2499, 1450],
    ["P002", "Smart Watch", "Wearables", 3999, 2400],
    ["P003", "Power Bank", "Power", 1299, 700],
    ["P004", "USB-C Cable", "Accessories", 499, 180],
    ["P005", "Phone Case", "Accessories", 699, 250],
    ["P006", "Bluetooth Speaker", "Audio", 2999, 1700],
    ["P007", "Wireless Mouse", "Computer", 999, 500],
    ["P008", "Keyboard", "Computer", 1799, 950],
    ["P009", "Laptop Stand", "Computer", 1499, 800],
    ["P010", "Charging Adapter", "Power", 899, 450],
], columns=[
    "product_id",
    "product_name",
    "category",
    "price",
    "cost"
])

products["stock"] = np.random.randint(100, 1500, len(products))

# ============================================================
# 2. CUSTOMERS
# ============================================================

N_CUSTOMERS = 5000

cities = [
    "Hyderabad", "Bangalore", "Mumbai", "Delhi",
    "Chennai", "Pune", "Kolkata", "Ahmedabad"
]

channels = [
    "Instagram", "Google", "Organic",
    "Referral", "YouTube", "Direct"
]

segments = [
    "New Customer",
    "Repeat Buyer",
    "High Value",
    "Price Sensitive",
    "Window Shopper",
    "Dormant"
]

customers = []

for i in range(1, N_CUSTOMERS + 1):

    # Create meaningful behavioral segments
    r = random.random()

    if r < 0.30:
        segment = "New Customer"
    elif r < 0.52:
        segment = "Repeat Buyer"
    elif r < 0.65:
        segment = "High Value"
    elif r < 0.80:
        segment = "Price Sensitive"
    elif r < 0.92:
        segment = "Window Shopper"
    else:
        segment = "Dormant"

    # Special high-potential group
    high_engagement = random.random() < (
        0.70 if segment in ["Repeat Buyer", "High Value"] else 0.20
    )

    customers.append([
        f"CUST{i:05d}",
        f"Customer {i}",
        f"customer{i}@example.com",
        random.choice(cities),
        random.randint(18, 55),
        random.choice(channels),
        (
            datetime(2025, 1, 1)
            + timedelta(days=random.randint(0, 500))
        ).date(),
        segment,
        0,
        0,
        None,
        high_engagement
    ])

customers = pd.DataFrame(customers, columns=[
    "customer_id",
    "name",
    "email",
    "city",
    "age",
    "acquisition_channel",
    "signup_date",
    "customer_segment",
    "total_orders",
    "total_spend",
    "last_order_date",
    "high_engagement"
])

# ============================================================
# 3. ORDERS + ORDER ITEMS
# ============================================================

orders = []
order_items = []

order_id = 1
item_id = 1

for _, customer in customers.iterrows():

    segment = customer["customer_segment"]

    if segment == "New Customer":
        n_orders = np.random.choice([1, 2], p=[0.75, 0.25])

    elif segment == "Repeat Buyer":
        n_orders = np.random.randint(2, 7)

    elif segment == "High Value":
        n_orders = np.random.randint(4, 9)

    elif segment == "Price Sensitive":
        n_orders = np.random.randint(1, 4)

    elif segment == "Window Shopper":
        n_orders = np.random.choice([0, 1], p=[0.65, 0.35])

    else:
        n_orders = np.random.choice([0, 1], p=[0.75, 0.25])

    for _ in range(n_orders):

        order_date = (
            datetime(2025, 3, 1)
            + timedelta(days=random.randint(0, 540))
        )

        order_status = random.choices(
            ["completed", "cancelled", "returned"],
            weights=[0.90, 0.06, 0.04]
        )[0]

        # ----------------------------------------------------
        # PRODUCT BEHAVIOR
        # ----------------------------------------------------

        chosen_products = []

        # Strong Earbuds signal
        if random.random() < 0.28:
            chosen_products.append("P001")

            # Intentional hidden opportunity:
            # repeat/high-engagement customers have
            # strong cable affinity
            if (
                segment in ["Repeat Buyer", "High Value"]
                and customer["high_engagement"]
            ):
                if random.random() < 0.14:
                    chosen_products.append("P004")

            else:
                if random.random() < 0.04:
                    chosen_products.append("P004")

        # Other products
        while len(chosen_products) < random.randint(1, 3):

            pid = random.choice(products["product_id"].tolist())

            if pid not in chosen_products:
                chosen_products.append(pid)

        total_amount = 0

        for pid in chosen_products:

            product = products[
                products["product_id"] == pid
            ].iloc[0]

            quantity = 1

            unit_price = product["price"]

            total_amount += quantity * unit_price

            order_items.append([
                f"ITEM{item_id:06d}",
                f"ORD{order_id:06d}",
                pid,
                quantity,
                unit_price
            ])

            item_id += 1

        orders.append([
            f"ORD{order_id:06d}",
            customer["customer_id"],
            order_date.date(),
            order_status,
            random.choice(["UPI", "Card", "NetBanking", "COD"]),
            total_amount
        ])

        order_id += 1

# Convert
orders = pd.DataFrame(orders, columns=[
    "order_id",
    "customer_id",
    "order_date",
    "order_status",
    "payment_method",
    "total_amount"
])

order_items = pd.DataFrame(order_items, columns=[
    "order_item_id",
    "order_id",
    "product_id",
    "quantity",
    "unit_price"
])

# ============================================================
# 4. UPDATE CUSTOMER METRICS
# ============================================================

completed_orders = orders[
    orders["order_status"] == "completed"
]

customer_metrics = completed_orders.groupby(
    "customer_id"
).agg(
    total_orders=("order_id", "count"),
    total_spend=("total_amount", "sum"),
    last_order_date=("order_date", "max")
).reset_index()

customers = customers.drop(
    columns=["total_orders", "total_spend", "last_order_date"]
)

customers = customers.merge(
    customer_metrics,
    on="customer_id",
    how="left"
)

customers["total_orders"] = customers["total_orders"].fillna(0)
customers["total_spend"] = customers["total_spend"].fillna(0)
customers["last_order_date"] = customers["last_order_date"].fillna(
    customers["signup_date"]
)

# ============================================================
# 5. CAMPAIGNS
# ============================================================

campaigns = pd.DataFrame([
    [
        "CAMP001",
        "Monsoon Audio Campaign",
        "Cross-sell",
        "Earbud Buyers",
        "2026-06-01",
        "2026-06-15",
        5000,
        4200,
        18000,
        1200,
        85,
        115000
    ],
    [
        "CAMP002",
        "Summer Accessories",
        "Cross-sell",
        "All Customers",
        "2026-05-01",
        "2026-05-15",
        8000,
        7600,
        25000,
        1500,
        100,
        95000
    ],
    [
        "CAMP003",
        "Repeat Buyer Rewards",
        "Retention",
        "Repeat Buyer",
        "2026-07-01",
        "2026-07-15",
        6000,
        5100,
        16000,
        1400,
        130,
        142000
    ],
    [
        "CAMP004",
        "Smart Watch Launch",
        "Product",
        "All Customers",
        "2026-07-15",
        "2026-08-01",
        12000,
        11000,
        35000,
        2200,
        170,
        310000
    ],
], columns=[
    "campaign_id",
    "campaign_name",
    "campaign_type",
    "target_segment",
    "start_date",
    "end_date",
    "budget",
    "spend",
    "impressions",
    "clicks",
    "conversions",
    "revenue"
])

# ============================================================
# 6. CUSTOMER SEGMENTS
# ============================================================

customer_segments = customers.groupby(
    "customer_segment"
).agg(
    customer_count=("customer_id", "count"),
    total_revenue=("total_spend", "sum"),
    average_orders=("total_orders", "mean"),
    average_spend=("total_spend", "mean")
).reset_index()

# ============================================================
# 7. SAVE
# ============================================================

products.to_csv(OUTPUT_DIR / "products.csv", index=False)
customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
orders.to_csv(OUTPUT_DIR / "orders.csv", index=False)
order_items.to_csv(OUTPUT_DIR / "order_items.csv", index=False)
campaigns.to_csv(OUTPUT_DIR / "campaigns.csv", index=False)
customer_segments.to_csv(
    OUTPUT_DIR / "customer_segments.csv",
    index=False
)

print("=" * 60)
print("MAYA SYNTHETIC DATA GENERATED")
print("=" * 60)

print(f"Customers:      {len(customers):,}")
print(f"Orders:         {len(orders):,}")
print(f"Order Items:    {len(order_items):,}")
print(f"Products:       {len(products):,}")
print(f"Campaigns:      {len(campaigns):,}")

print("\nFiles created:")
for file in OUTPUT_DIR.glob("*.csv"):
    print(" -", file)

print("\nDataset ready for MAYA.")