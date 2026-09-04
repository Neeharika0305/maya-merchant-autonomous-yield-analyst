def challenge_hypotheses(opportunity, hypotheses):

    results = []

    overall = opportunity["overall_affinity"]
    high_value = opportunity["high_value_affinity"]
    repeat = opportunity["repeat_buyer_affinity"]
    engagement = opportunity["high_engagement_affinity"]

    for h in hypotheses:

        if h["id"] == "H1":
            supporting = (
                "Cable affinity exists, but the available behavioral "
                "signal does not show that awareness is the dominant cause."
            )

            contradictory = (
                f"Overall Earbud → Cable affinity is already "
                f"{overall}%, suggesting customers are aware enough "
                "to purchase the product."
            )

            score = 0.42

        elif h["id"] == "H2":
            supporting = (
                "Price may influence accessory purchases."
            )

            contradictory = (
                "The dataset shows substantially stronger affinity "
                "among high-value customers, suggesting segmentation "
                "may matter more than price alone."
            )

            score = 0.48

        elif h["id"] == "H3":
            supporting = (
                "Some customers may purchase accessories separately "
                "from their original Earbud order."
            )

            contradictory = (
                "Strong product affinity exists among Earbud buyers, "
                "so timing alone does not explain the opportunity."
            )

            score = 0.55

        else:
            supporting = (
                f"High-value customers show {high_value}% cable affinity, "
                f"while repeat buyers show {repeat}%."
            )

            contradictory = (
                f"High engagement affinity is {engagement}%, so the "
                "opportunity still requires more precise audience targeting."
            )

            score = 0.88

        results.append({
            "hypothesis_id": h["id"],
            "title": h["title"],
            "supporting_evidence": supporting,
            "contradictory_evidence": contradictory,
            "updated_confidence": score
        })

    results.sort(
        key=lambda x: x["updated_confidence"],
        reverse=True
    )

    return results