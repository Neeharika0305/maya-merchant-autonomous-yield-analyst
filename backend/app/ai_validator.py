from app.analytics.guardrails import validate_experiment


REQUIRED_FIELDS = [
    "strongest_segment",
    "strongest_product_signal",
    "growth_opportunity",
    "hypothesis",
    "challenge",
    "recommended_experiment",
    "reasoning",
    "confidence",
]


VALID_SEGMENTS = {
    "Dormant",
    "High Value",
    "New Customer",
    "Price Sensitive",
    "Repeat Buyer",
    "Window Shopper",
}


def validate_ai_recommendation(recommendation):
    """
    MAYA safety and factual validation layer.

    Gemini can recommend.
    MAYA validates before accepting the recommendation.
    """

    # ---------------------------------------------------------
    # 1. Check required AI fields
    # ---------------------------------------------------------

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if field not in recommendation
        or recommendation[field] in (None, "")
    ]

    if missing_fields:
        return {
            "approved": False,
            "decision": "REJECT",
            "reason": "AI response is incomplete.",
            "missing_fields": missing_fields,
        }

    # ---------------------------------------------------------
    # 2. Validate customer segment
    # ---------------------------------------------------------

    segment = recommendation["strongest_segment"]

    segment_valid = any(
        valid_segment.lower() in segment.lower()
        for valid_segment in VALID_SEGMENTS
    )

    if not segment_valid:
        return {
            "approved": False,
            "decision": "REJECT",
            "reason": "AI recommended a customer segment that does not exist in MAYA's verified merchant data.",
            "invalid_segment": segment,
            "valid_segments": sorted(VALID_SEGMENTS),
        }

    # ---------------------------------------------------------
    # 3. Extract experiment parameters
    # ---------------------------------------------------------

    discount = recommendation.get("discount", 0)
    budget = recommendation.get("budget", 0)
    audience_size = recommendation.get("audience_size", 0)

    # ---------------------------------------------------------
    # 4. Apply MAYA business guardrails
    # ---------------------------------------------------------

    guardrails = validate_experiment(
        budget=budget,
        discount=discount,
        audience_size=audience_size,
    )

    if not guardrails["approved"]:
        return {
            "approved": False,
            "decision": "REJECT",
            "reason": "AI recommendation violates MAYA experiment guardrails.",
            "violations": guardrails["violations"],
            "limits": guardrails["limits"],
        }

    # ---------------------------------------------------------
    # 5. Recommendation passed all checks
    # ---------------------------------------------------------

    return {
        "approved": True,
        "decision": "APPROVE",
        "reason": "AI recommendation passed MAYA factual validation and experiment guardrails.",
        "limits": guardrails["limits"],
    }