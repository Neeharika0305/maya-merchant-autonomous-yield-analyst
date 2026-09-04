import pandas as pd


def discover_cross_sell_opportunity(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    items: pd.DataFrame
):

    # Validate required columns
    required_orders = {
        "order_id",
        "customer_id"
    }

    required_items = {
        "order_id",
        "product_id"
    }

    required_customers = {
        "customer_id",
        "customer_segment",
        "high_engagement"
    }

    missing_orders = required_orders - set(orders.columns)
    missing_items = required_items - set(items.columns)
    missing_customers = required_customers - set(customers.columns)

    if missing_orders:
        raise ValueError(
            f"Missing columns in orders.csv: {missing_orders}"
        )

    if missing_items:
        raise ValueError(
            f"Missing columns in order_items.csv: {missing_items}"
        )

    if missing_customers:
        raise ValueError(
            f"Missing columns in customers.csv: {missing_customers}"
        )

    # Connect order items to customers
    merged = items.merge(
        orders[["order_id", "customer_id"]],
        on="order_id",
        how="inner"
    )

    # Determine which products each customer purchased
    customer_products = merged.groupby(
        ["customer_id", "product_id"]
    ).size().unstack(fill_value=0)

    # P001 = Wireless Earbuds
    customer_products["earbuds"] = (
        customer_products.get("P001", 0) > 0
    )

    # P004 = USB-C Cable
    customer_products["cable"] = (
        customer_products.get("P004", 0) > 0
    )

    # Add customer segment information
    analysis = customer_products.merge(
        customers[
            [
                "customer_id",
                "customer_segment",
                "high_engagement"
            ]
        ],
        left_index=True,
        right_on="customer_id",
        how="inner"
    )

    # Customers who purchased Earbuds
    earbud_buyers = analysis[
        analysis["earbuds"]
    ]

    # Overall cable affinity
    affinity = earbud_buyers["cable"].mean()

    # High-value segment
    high_value = earbud_buyers[
        earbud_buyers["customer_segment"]
        == "High Value"
    ]["cable"].mean()

    # Repeat buyers
    repeat = earbud_buyers[
        earbud_buyers["customer_segment"]
        == "Repeat Buyer"
    ]["cable"].mean()

    # Highly engaged customers
    high_engagement = earbud_buyers[
        earbud_buyers["high_engagement"]
    ]["cable"].mean()

    return {
        "opportunity_type": "PRODUCT_CROSS_SELL",

        "title":
            "Earbud -> USB-C Cable Cross-Sell Opportunity",

        "earbud_buyers":
            len(earbud_buyers),

        "overall_affinity":
            round(affinity * 100, 2),

        "high_value_affinity":
            round(high_value * 100, 2),

        "repeat_buyer_affinity":
            round(repeat * 100, 2),

        "high_engagement_affinity":
            round(high_engagement * 100, 2),

        "confidence":
            82,

        "status":
            "DISCOVERED"
    }