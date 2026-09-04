def calculate_financial_impact(
    eligible_customers,
    conversion_rate,
    average_order_value,
    expected_lift,
    campaign_cost
):
    expected_additional_customers = (
        eligible_customers
        * conversion_rate
        * expected_lift
    )

    incremental_revenue = (
        expected_additional_customers
        * average_order_value
    )

    expected_profit = (
        incremental_revenue
        - campaign_cost
    )

    roi = (
        expected_profit / campaign_cost
        if campaign_cost > 0
        else 0
    )

    return {
        "eligible_customers": eligible_customers,
        "conversion_rate": conversion_rate,
        "expected_lift": expected_lift,
        "average_order_value": average_order_value,
        "campaign_cost": campaign_cost,
        "expected_additional_customers": round(
            expected_additional_customers,
            2
        ),
        "incremental_revenue": round(
            incremental_revenue,
            2
        ),
        "expected_profit": round(
            expected_profit,
            2
        ),
        "expected_roi": round(
            roi,
            2
        )
    }


def design_experiment(
    eligible_customers,
    financial_impact
):
    control_size = eligible_customers // 2

    treatment_size = (
        eligible_customers - control_size
    )

    return {
        "experiment_name":
            "Earbud → USB-C Cable Cross-Sell Test",

        "target":
            "High-value/repeat/high-engagement Earbud customers",

        "eligible_customers":
            eligible_customers,

        "control_size":
            control_size,

        "treatment_size":
            treatment_size,

        "offer":
            "5% USB-C Cable cross-sell incentive",

        "budget":
            financial_impact["campaign_cost"],

        "duration_days":
            7,

        "success_metric":
            "Treatment conversion lift",

        "success_threshold":
            "≥ 3 percentage-point improvement",

        "expected_incremental_revenue":
            financial_impact["incremental_revenue"],

        "expected_roi":
            financial_impact["expected_roi"]
    }


def evaluate_experiment(financial_impact):

    revenue = financial_impact["incremental_revenue"]
    roi = financial_impact["expected_roi"]

    if roi >= 2:
        decision = "STRONG_GO"
    elif roi >= 1:
        decision = "GO"
    elif roi >= 0:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    return {
        "decision": decision,
        "reason": (
            f"Expected incremental revenue ₹{revenue:,.0f}, "
            f"with estimated ROI {roi:.2f}x."
        )
    }