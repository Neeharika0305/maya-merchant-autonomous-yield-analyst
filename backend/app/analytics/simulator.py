def simulate_experiment(experiment):
    """
    Simulate the first experiment using the AI-selected experiment.

    The simulator intentionally produces a weak first result so MAYA
    can demonstrate failure detection and autonomous adaptation.
    """

    audience_size = experiment["eligible_customers"]
    target = experiment.get("target", "selected audience")
    offer = experiment.get(
        "offer",
        "targeted cross-sell incentive"
    )

    expected_conversion = 0.10
    control_conversion = 0.068
    treatment_conversion = 0.072

    conversion_lift = (
        treatment_conversion - control_conversion
    )

    success_threshold = 0.03

    success = conversion_lift >= success_threshold

    if success:

        status = "SUCCESS"
        failure_reason = None

    else:

        status = "FAILED"

        failure_reason = (
            f"The {target} audience was too broad for the "
            f"{offer}; lower-intent customers diluted "
            f"treatment performance."
        )

    return {
        "experiment_target": target,
        "audience_size": audience_size,
        "offer": offer,
        "expected_conversion": expected_conversion,
        "control_conversion": control_conversion,
        "treatment_conversion": treatment_conversion,
        "conversion_lift": conversion_lift,
        "success_threshold": success_threshold,
        "success": success,
        "status": status,
        "failure_reason": failure_reason,
    }


def simulate_recovery_experiment(experiment):
    """
    Simulate MAYA's adapted second experiment.

    Recovery is derived from the failed AI-selected experiment,
    rather than from a hardcoded product or customer segment.
    """

    original_audience = experiment["eligible_customers"]
    target = experiment.get(
        "target",
        "selected audience"
    )

    # MAYA narrows the original audience to the
    # highest-intent customers inside the selected segment.
    recovery_audience = max(
        1,
        int(original_audience * 0.60)
    )

    expected_conversion = 0.125
    control_conversion = 0.068
    treatment_conversion = 0.151

    conversion_lift = (
        treatment_conversion - control_conversion
    )

    success_threshold = 0.03

    success = conversion_lift >= success_threshold

    return {
        "experiment_target": target,
        "original_audience_size": original_audience,
        "recovery_audience_size": recovery_audience,
        "expected_conversion": expected_conversion,
        "control_conversion": control_conversion,
        "treatment_conversion": treatment_conversion,
        "conversion_lift": conversion_lift,
        "success_threshold": success_threshold,
        "success": success,
        "status": (
            "RECOVERED"
            if success
            else "FAILED"
        ),
        "failure_reason": None if success else (
            "The adapted audience still did not meet "
            "the required conversion threshold."
        ),
    }