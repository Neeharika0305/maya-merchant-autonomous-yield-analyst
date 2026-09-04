from app.tools import execute_tool


def build_agent_context():
    """
    Build the structured merchant context available to MAYA.
    MAYA receives data through approved tools only.
    """

    merchant = execute_tool("get_merchant_summary")
    segments = execute_tool("get_customer_segments")
    products = execute_tool("get_product_catalog")

    return {
        "merchant": merchant,
        "segments": segments,
        "products": products,
    }


def get_tool_catalog():
    """
    Describes the capabilities MAYA is allowed to use.
    """

    return [
        {
            "name": "get_merchant_summary",
            "description": "Get high-level merchant metrics."
        },
        {
            "name": "get_customer_segments",
            "description": "Get customer segment performance."
        },
        {
            "name": "get_product_catalog",
            "description": "Get product price, cost and inventory information."
        }
    ]