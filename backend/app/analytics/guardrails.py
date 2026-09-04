MAX_BUDGET = 10000
MAX_DISCOUNT = 10
MAX_AUDIENCE = 1500


def validate_experiment(
    budget,
    discount,
    audience_size
):

    violations = []

    if budget > MAX_BUDGET:
        violations.append(
            f"Budget exceeds ₹{MAX_BUDGET}"
        )

    if discount > MAX_DISCOUNT:
        violations.append(
            f"Discount exceeds {MAX_DISCOUNT}%"
        )

    if audience_size > MAX_AUDIENCE:
        violations.append(
            f"Audience exceeds {MAX_AUDIENCE} customers"
        )

    return {
        "approved": len(violations) == 0,
        "violations": violations,
        "limits": {
            "max_budget": MAX_BUDGET,
            "max_discount": MAX_DISCOUNT,
            "max_audience": MAX_AUDIENCE
        }
    }