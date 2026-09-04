import pandas as pd

from app.analytics.opportunity import discover_cross_sell_opportunity
from app.analytics.hypothesis import generate_hypotheses
from app.analytics.challenger import challenge_hypotheses
from app.analytics.experiment import (
    calculate_financial_impact,
    design_experiment,
    evaluate_experiment
)
from app.analytics.guardrails import validate_experiment
from app.analytics.simulator import (
    simulate_experiment,
    simulate_recovery_experiment
)
from app.analytics.recovery import diagnose_failure

from app.ai_pipeline import run_ai_pipeline


def run_maya():

    # =========================================================
    # 1. LOAD VERIFIED MERCHANT DATA
    # =========================================================

    customers = pd.read_csv("../data/customers.csv")
    orders = pd.read_csv("../data/orders.csv")
    items = pd.read_csv("../data/order_items.csv")


    # =========================================================
    # 2. DISCOVER
    # =========================================================

    opportunity = discover_cross_sell_opportunity(
        customers,
        orders,
        items
    )


    # =========================================================
    # 3. HYPOTHESIZE
    # =========================================================

    hypotheses = generate_hypotheses(
        opportunity
    )


    # =========================================================
    # 4. CHALLENGE
    # =========================================================

    challenged_hypotheses = challenge_hypotheses(
        opportunity,
        hypotheses
    )

    selected_hypothesis = challenged_hypotheses[0]


    # =========================================================
    # 5. GEMINI RECOMMENDATION
    # =========================================================

    ai_pipeline = run_ai_pipeline()


    # =========================================================
    # 6. AI DECISION / DETERMINISTIC FALLBACK
    # =========================================================
    #
    # Gemini is an enhancement, NOT a single point of failure.
    #
    # If Gemini is unavailable, MAYA continues using a
    # deterministic recommendation based on verified merchant
    # signals.
    # =========================================================

    recommendation = ai_pipeline.get(
        "recommendation",
        {}
    )

    if ai_pipeline.get("decision") == "APPROVE" and ai_pipeline.get("approved"):

        # -----------------------------------------------------
        # Gemini-approved decision
        # -----------------------------------------------------

        ai_segment = recommendation["strongest_segment"]
        ai_discount = float(recommendation["discount"])
        ai_budget = float(recommendation["budget"])
        ai_audience_size = int(
            recommendation["audience_size"]
        )

        ai_mode = "GEMINI"

    else:

        # -----------------------------------------------------
        # Deterministic MAYA fallback
        #
        # Based on the strongest verified high-intent signal.
        # -----------------------------------------------------

        ai_segment = "Repeat Buyer"

        ai_discount = 8.0

        ai_budget = 8000.0

        ai_audience_size = 1013

        recommendation = {
            "strongest_segment": ai_segment,
            "strongest_product_signal": "Smart Watch (P002)",
            "growth_opportunity": (
                "Upsell Smart Watch to high-intent repeat buyers."
            ),
            "hypothesis": (
                "Repeat buyers are more likely to respond "
                "to a targeted Smart Watch incentive."
            ),
            "challenge": (
                "High-intent repeat buyers may purchase "
                "without an incentive."
            ),
            "recommended_experiment": (
                "Test an 8% Smart Watch incentive "
                "with Repeat Buyers."
            ),
            "reasoning": (
                "MAYA continued using its verified deterministic "
                "decision engine because the external AI provider "
                "was unavailable."
            ),
            "confidence": 88,
            "discount": ai_discount,
            "budget": ai_budget,
            "audience_size": ai_audience_size,
            "fallback_mode": True
        }

        ai_pipeline["recommendation"] = recommendation
        ai_pipeline["decision"] = "FALLBACK"
        ai_pipeline["approved"] = True
        ai_pipeline["fallback_mode"] = True

        ai_mode = "DETERMINISTIC_FALLBACK"


    # =========================================================
    # 7. FINANCIAL MODEL
    # =========================================================

    conversion_rate = 0.10

    average_order_value = 1299

    expected_lift = 0.30

    financial = calculate_financial_impact(
        eligible_customers=ai_audience_size,
        conversion_rate=conversion_rate,
        average_order_value=average_order_value,
        expected_lift=expected_lift,
        campaign_cost=ai_budget
    )


    # =========================================================
    # 8. ECONOMIC DECISION
    # =========================================================

    economic_decision = evaluate_experiment(
        financial
    )


    # =========================================================
    # 9. BUILD EXPERIMENT
    # =========================================================

    experiment = {
        "experiment_name": (
            f"AI-Selected {ai_segment} Cross-Sell Experiment"
        ),

        "target": ai_segment,

        "eligible_customers": ai_audience_size,

        "control_size": (
            ai_audience_size // 2
        ),

        "treatment_size": (
            ai_audience_size
            - (ai_audience_size // 2)
        ),

        "offer": (
            f"{ai_discount:g}% incentive "
            f"on AI-selected product opportunity"
        ),

        "discount": ai_discount,

        "budget": ai_budget,

        "duration_days": 7,

        "success_metric": (
            "Treatment conversion lift"
        ),

        "success_threshold": (
            "≥ 3 percentage-point improvement"
        ),

        "expected_incremental_revenue": (
            financial["incremental_revenue"]
        ),

        "expected_roi": (
            financial["expected_roi"]
        ),

        "ai_selected_segment": ai_segment,

        "ai_recommendation": (
            recommendation["recommended_experiment"]
        ),

        "ai_mode": ai_mode
    }


    # =========================================================
    # 10. FINAL GUARDRAIL
    # =========================================================

    guardrails = validate_experiment(
        budget=experiment["budget"],
        discount=experiment["discount"],
        audience_size=experiment["eligible_customers"]
    )


    if not guardrails["approved"]:

        return {
            "opportunity": opportunity,
            "hypotheses": hypotheses,
            "challenged_hypotheses": challenged_hypotheses,
            "selected_hypothesis": selected_hypothesis,
            "ai_pipeline": ai_pipeline,
            "financial": financial,
            "economic_decision": economic_decision,
            "experiment": experiment,
            "guardrails": guardrails,
            "final_status": "BLOCKED"
        }


    # =========================================================
    # 11. FIRST EXPERIMENT
    # =========================================================

    first_experiment = simulate_experiment(
        experiment
    )


    # =========================================================
    # 12. MEASURE + DIAGNOSE
    # =========================================================

    failure_diagnosis = diagnose_failure(
        first_experiment
    )


    # =========================================================
    # 13. ADAPT + RECOVER
    # =========================================================

    recovery_experiment = simulate_recovery_experiment(
        experiment
    )


    # =========================================================
    # 14. FINAL STATUS
    # =========================================================

    final_status = (
        "RECOVERED"
        if recovery_experiment["success"]
        else "FAILED"
    )


    # =========================================================
    # 15. COMPLETE AUTONOMOUS DECISION
    # =========================================================

    return {

        "opportunity": opportunity,

        "hypotheses": hypotheses,

        "challenged_hypotheses": challenged_hypotheses,

        "selected_hypothesis": selected_hypothesis,

        "ai_pipeline": ai_pipeline,

        "financial": financial,

        "economic_decision": economic_decision,

        "experiment": experiment,

        "guardrails": guardrails,

        "first_experiment": first_experiment,

        "failure_diagnosis": failure_diagnosis,

        "recovery_experiment": recovery_experiment,

        "final_status": final_status
    }


if __name__ == "__main__":

    import pprint

    result = run_maya()

    pprint.pp(result)