from sqlalchemy import text
from app.database import engine


def get_customer_count():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM customers")
        )
        return result.scalar()


def get_order_count():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM orders")
        )
        return result.scalar()


def get_product_count():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM products")
        )
        return result.scalar()


def get_revenue():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT COALESCE(SUM(total_amount), 0)
                FROM orders
                WHERE order_status = 'completed'
            """)
        )
        return float(result.scalar())


def get_customer_segments():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM customer_segments
            """)
        )

        return [dict(row._mapping) for row in result]


def get_product_catalog():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM products
            """)
        )

        return [dict(row._mapping) for row in result]


def get_database_summary():
    return {
        "customers": get_customer_count(),
        "orders": get_order_count(),
        "products": get_product_count(),
        "revenue": get_revenue()
    }


def get_maya_context():
    """
    Controlled read-only context exposed to MAYA.
    The agent never receives unrestricted database access.
    """

    return {
        "database_summary": get_database_summary(),
        "customer_segments": get_customer_segments(),
        "product_catalog": get_product_catalog()
    }