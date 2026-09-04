import pandas as pd

from analytics.opportunity import (
    discover_cross_sell_opportunity
)

customers = pd.read_csv("../data/customers.csv")
orders = pd.read_csv("../data/orders.csv")
items = pd.read_csv("../data/order_items.csv")

result = discover_cross_sell_opportunity(
    customers,
    orders,
    items
)

print("\n==============================")
print("MAYA OPPORTUNITY DISCOVERY")
print("==============================")

for key, value in result.items():
    print(f"{key}: {value}")