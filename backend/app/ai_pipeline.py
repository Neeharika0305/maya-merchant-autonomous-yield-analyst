from app.gemini_agent import ask_gemini
from app.ai_validator import validate_ai_recommendation


def run_ai_pipeline():
    """
    MAYA AI decision pipeline.

    Gemini proposes.
    MAYA validates.
    Only validated recommendations continue.
    """

    recommendation = ask_gemini()

    # Gemini temporarily unavailable
    if recommendation.get("fallback_required"):
        return {
            "ai_status": "UNAVAILABLE",
            "decision": "FALLBACK",
            "reason": "Gemini was temporarily unavailable. MAYA deterministic engine should continue.",
            "recommendation": recommendation,
        }

    validation = validate_ai_recommendation(
        recommendation
    )

    return {
        "ai_status": "AVAILABLE",
        "decision": validation["decision"],
        "approved": validation["approved"],
        "validation": validation,
        "recommendation": recommendation,
    }


if __name__ == "__main__":

    import pprint

    result = run_ai_pipeline()

    pprint.pp(result)