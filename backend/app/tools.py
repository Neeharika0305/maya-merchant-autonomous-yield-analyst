from app.db_tools import (
    get_database_summary,
    get_customer_segments,
    get_product_catalog,
)


# ---------------------------------------------------------
# MAYA CONTROLLED TOOL REGISTRY
# ---------------------------------------------------------

def tool_get_merchant_summary():
    return get_database_summary()


def tool_get_customer_segments():
    return get_customer_segments()


def tool_get_product_catalog():
    return get_product_catalog()


MAYA_TOOLS = {
    "get_merchant_summary": tool_get_merchant_summary,
    "get_customer_segments": tool_get_customer_segments,
    "get_product_catalog": tool_get_product_catalog,
}


def execute_tool(tool_name: str):
    """
    Execute only tools explicitly registered with MAYA.
    No arbitrary SQL or database access is allowed.
    """

    if tool_name not in MAYA_TOOLS:
        raise ValueError(f"Tool '{tool_name}' is not allowed")

    return MAYA_TOOLS[tool_name]()