from analytics.experiment import (
    calculate_financial_impact,
    design_experiment,
    evaluate_experiment
)

from analytics.guardrails import (
    validate_experiment
)

eligible_customers = 310

financial = calculate_financial_impact(
    eligible_customers=eligible_customers,
    conversion_rate=0.10,
    average_order_value=1299,
    expected_lift=0.30,
    campaign_cost=5000
)

experiment = design_experiment(
    eligible_customers,
    financial
)

decision = evaluate_experiment(financial)

guardrails = validate_experiment(
    budget=experiment["budget"],
    discount=5,
    audience_size=experiment["eligible_customers"]
)

print("\n")
print("=" * 60)
print("💰 MAYA FINANCIAL IMPACT")
print("=" * 60)

for key, value in financial.items():
    print(f"{key}: {value}")

print("\n")
print("=" * 60)
print("🧪 MAYA EXPERIMENT")
print("=" * 60)

for key, value in experiment.items():
    print(f"{key}: {value}")

print("\n")
print("=" * 60)
print("🧠 MAYA ECONOMIC DECISION")
print("=" * 60)

print("Decision:", decision["decision"])
print("Reason:", decision["reason"])

print("\n")
print("=" * 60)
print("🔐 MAYA GUARDRAILS")
print("=" * 60)

print("Approved:", guardrails["approved"])

if guardrails["violations"]:
    print("Violations:")
    for violation in guardrails["violations"]:
        print("-", violation)
else:
    print("All guardrails passed.")
