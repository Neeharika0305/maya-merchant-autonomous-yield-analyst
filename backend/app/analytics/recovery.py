def diagnose_failure(experiment_result):
    """
    Diagnose the failure of the actual AI-selected experiment.

    MAYA does not assume a specific product or segment.
    It uses the experiment metadata supplied by the execution engine.
    """

    target = experiment_result.get(
        "experiment_target",
        "selected audience"
    )

    audience_size = experiment_result.get(
        "audience_size",
        0
    )

    treatment_conversion = experiment_result.get(
        "treatment_conversion",
        0
    )

    control_conversion = experiment_result.get(
        "control_conversion",
        0
    )

    conversion_lift = experiment_result.get(
        "conversion_lift",
        0
    )

    success_threshold = experiment_result.get(
        "success_threshold",
        0.03
    )

    if experiment_result.get("success"):

        return {
            "diagnosis": (
                f"The {target} experiment succeeded. "
                "No recovery action was required."
            ),
            "evidence": [
                "Treatment conversion exceeded the control.",
                f"Observed lift was {conversion_lift:.1%}.",
                f"Required lift was {success_threshold:.1%}."
            ],
            "adaptation": (
                "Continue monitoring the winning experiment "
                "before wider rollout."
            )
        }

    # ---------------------------------------------------------
    # FAILURE DIAGNOSIS
    # ---------------------------------------------------------

    diagnosis = (
        f"The treatment underperformed because the "
        f"{target} audience contained lower-intent customers."
    )

    evidence = [
        (
            f"Treatment conversion was "
            f"{treatment_conversion:.1%}, versus "
            f"{control_conversion:.1%} in control."
        ),
        (
            f"Observed lift was only "
            f"{conversion_lift:.1%}, below the "
            f"{success_threshold:.1%} success threshold."
        ),
        (
            f"The original {target} audience contained "
            f"{audience_size:,} customers, indicating "
            "the audience was too broad for the first test."
        )
    ]

    adaptation = (
        f"Narrow the {target} audience to the highest-intent "
        "customers within the segment and retest before "
        "scaling the campaign."
    )

    return {
        "diagnosis": diagnosis,
        "evidence": evidence,
        "adaptation": adaptation
    }