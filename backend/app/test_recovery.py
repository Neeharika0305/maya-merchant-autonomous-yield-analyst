import pandas as pd

from analytics.opportunity import (
    discover_cross_sell_opportunity
)

from analytics.hypothesis import (
    generate_hypotheses
)

from analytics.challenger import (
    challenge_hypotheses
)

from analytics.experiment import (
    calculate_financial_impact,
    design_experiment,
    evaluate_experiment
)

from analytics.guardrails import (
    validate_experiment
)

from analytics.simulator import (
    simulate_experiment,
    simulate_recovery_experiment
)

from analytics.recovery import (
    diagnose_failure
)


# ============================================================
# LOAD DATA
# ============================================================

customers = pd.read_csv("../data/customers.csv")
orders = pd.read_csv("../data/orders.csv")
items = pd.read_csv("../data/order_items.csv")


# ============================================================
# 1. DISCOVER
# ============================================================

opportunity = discover_cross_sell_opportunity(
    customers,
    orders,
    items
)


# ============================================================
# 2. HYPOTHESIZE
# ============================================================

hypotheses = generate_hypotheses(
    opportunity
)


# ============================================================
# 3. CHALLENGE
# ============================================================

challenged = challenge_hypotheses(
    opportunity,
    hypotheses
)

winner = challenged[0]


# ============================================================
# 4. FINANCIAL IMPACT
# ============================================================

financial = calculate_financial_impact(
    eligible_customers=310,
    conversion_rate=0.10,
    average_order_value=1299,
    expected_lift=0.30,
    campaign_cost=5000
)

economic_decision = evaluate_experiment(
    financial
)


# ============================================================
# 5. EXPERIMENT
# ============================================================

experiment = design_experiment(
    310,
    financial
)


# ============================================================
# 6. GUARDRAILS
# ============================================================

guardrails = validate_experiment(
    budget=5000,
    discount=5,
    audience_size=310
)


# ============================================================
# 7. SIMULATE FIRST EXPERIMENT
# ============================================================

result = simulate_experiment(
    experiment
)


# ============================================================
# 8. FAILURE DIAGNOSIS
# ============================================================

diagnosis = diagnose_failure(
    result
)


# ============================================================
# 9. RECOVERY EXPERIMENT
# ============================================================

recovery_result = simulate_recovery_experiment(experiment)


# ============================================================
# PRINT MAYA'S COMPLETE JOURNEY
# ============================================================

print("\n")
print("=" * 70)
print("                    MAYA AUTONOMOUS LOOP")
print("=" * 70)


print("\n🔎 1. OPPORTUNITY DISCOVERED")

print(opportunity["title"])

print(
    f"Overall affinity: "
    f"{opportunity['overall_affinity']}%"
)


print("\n🧠 2. BEST HYPOTHESIS")

print(winner["title"])

print(
    "Confidence:",
    winner["updated_confidence"]
)


print("\n💰 3. FINANCIAL ANALYSIS")

print(
    f"Expected revenue: "
    f"₹{financial['incremental_revenue']:,.0f}"
)

print(
    f"Campaign cost: "
    f"₹{financial['campaign_cost']:,.0f}"
)

print(
    f"Expected ROI: "
    f"{financial['expected_roi']}x"
)

print(
    "Economic decision:",
    economic_decision["decision"]
)


print("\n🧪 4. EXPERIMENT")

print(
    "Audience:",
    experiment["eligible_customers"]
)

print(
    "Control:",
    experiment["control_size"]
)

print(
    "Treatment:",
    experiment["treatment_size"]
)

print(
    "Offer:",
    experiment["offer"]
)


print("\n🔐 5. GUARDRAILS")

print(
    "Approved:",
    guardrails["approved"]
)


print("\n🚀 6. EXPERIMENT LAUNCHED")


print("\n⚠️ 7. EXPERIMENT RESULT")

print(
    "Expected conversion:",
    result["expected_conversion"] * 100,
    "%"
)

print(
    "Actual treatment conversion:",
    result["treatment_conversion"] * 100,
    "%"
)

print(
    "Status:",
    result["status"]
)


print("\n🔬 8. FAILURE INVESTIGATION")

print(
    "Diagnosis:",
    diagnosis["diagnosis"]
)

print(
    "Adaptation:",
    diagnosis["adaptation"]
)


print("\n🔄 9. RECOVERY EXPERIMENT")

print(
    "New audience:",
    "Repeat Earbud + High Engagement"
)

print(
    "Expected conversion:",
    recovery_result["expected_conversion"] * 100,
    "%"
)

print(
    "Actual conversion:",
    recovery_result["treatment_conversion"] * 100,
    "%"
)

print(
    "Status:",
    recovery_result["status"]
)


print("\n")
print("=" * 70)
print("                  MAYA FINAL OUTCOME")
print("=" * 70)

print(
    "❌ Initial strategy failed"
)

print(
    "🔬 Root cause identified"
)

print(
    "🔄 Strategy adapted"
)

print(
    "✅ Recovery experiment succeeded"
)

print("\nMAYA LEARNED FROM THE FAILED INTERVENTION.")
recovery_result = simulate_recovery_experiment(experiment)

# ============================================================
# PYTEST TESTS
# ============================================================

def test_opportunity_discovered():
    assert opportunity is not None
    assert opportunity["title"]
    assert opportunity["overall_affinity"] > 0


def test_hypothesis_challenger():
    assert len(challenged) > 0
    assert winner["updated_confidence"] > 0


def test_financial_impact():
    assert financial["incremental_revenue"] > 0
    assert financial["campaign_cost"] == 5000


def test_guardrails_approved():
    assert guardrails["approved"] is True


def test_first_experiment_fails():
    assert result["success"] is False
    assert result["status"] == "FAILED"


def test_failure_diagnosis():
    assert diagnosis is not None


def test_recovery_succeeds():
    assert recovery_result["success"] is True
    assert recovery_result["status"] == "RECOVERED"
    assert recovery_result["conversion_lift"] >= recovery_result["success_threshold"]
