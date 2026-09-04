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


# Load merchant data
customers = pd.read_csv("../data/customers.csv")
orders = pd.read_csv("../data/orders.csv")
items = pd.read_csv("../data/order_items.csv")


# STEP 1 — DISCOVER
opportunity = discover_cross_sell_opportunity(
    customers,
    orders,
    items
)


# STEP 2 — HYPOTHESIZE
hypotheses = generate_hypotheses(
    opportunity
)


# STEP 3 — CHALLENGE
challenged = challenge_hypotheses(
    opportunity,
    hypotheses
)


print("\n")
print("=" * 60)
print("                    MAYA AGENT")
print("=" * 60)

print("\n🔎 OPPORTUNITY DISCOVERED")
print(opportunity["title"])

print(
    f"\nOverall affinity: "
    f"{opportunity['overall_affinity']}%"
)

print("\n🧠 COMPETING HYPOTHESES")

for h in hypotheses:
    print(
        f"\n{h['id']} — {h['title']}"
    )
    print(h["hypothesis"])


print("\n⚔️ EVIDENCE CHALLENGE")

for result in challenged:

    print(
        f"\n{result['hypothesis_id']} — "
        f"{result['title']}"
    )

    print(
        "Supporting:",
        result["supporting_evidence"]
    )

    print(
        "Contradicting:",
        result["contradictory_evidence"]
    )

    print(
        "Updated confidence:",
        result["updated_confidence"]
    )


winner = challenged[0]

print("\n")
print("=" * 60)
print("🏆 MAYA'S CURRENT BEST HYPOTHESIS")
print("=" * 60)

print(winner["title"])
print(winner["updated_confidence"])

print("\nMAYA DECISION:")
print(
    "Prioritize high-value/repeat/high-engagement "
    "Earbud customers for the experiment."
)