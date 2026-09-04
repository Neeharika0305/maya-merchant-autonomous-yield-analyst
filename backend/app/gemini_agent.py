import os
import json

from dotenv import load_dotenv
from google import genai

from app.tools import MAYA_TOOLS


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=API_KEY,
    http_options={
        "timeout": 10000,
    },
)


SYSTEM_PROMPT = """
You are MAYA — Merchant Autonomous Yield Analyst.

You are an autonomous merchant growth analyst.

Rules:

1. Never invent merchant data.
2. Use only information returned by approved MAYA tools.
3. Never access PostgreSQL directly.
4. Challenge assumptions before recommending experiments.
5. Prefer high-intent customer segments.
6. Optimize for incremental profit.
7. Respect MAYA experiment guardrails.
8. Never recommend a discount above 10%.
9. Never recommend a budget above ₹10,000.
10. Never recommend an audience above 1,500 customers.

Reasoning loop:

DISCOVER → HYPOTHESIZE → CHALLENGE → EXPERIMENT → MEASURE → ADAPT
"""


def get_merchant_context():

    return {
        "merchant_summary": MAYA_TOOLS["get_merchant_summary"](),
        "customer_segments": MAYA_TOOLS["get_customer_segments"](),
        "product_catalog": MAYA_TOOLS["get_product_catalog"](),
    }


def ask_gemini():

    context = get_merchant_context()

    prompt = f"""
{SYSTEM_PROMPT}

Here is verified merchant information obtained through
approved MAYA tools:

{json.dumps(context, indent=2, default=str)}

Analyze the merchant and identify the strongest
growth opportunity.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "strongest_segment": "...",
    "strongest_product_signal": "...",
    "growth_opportunity": "...",
    "hypothesis": "...",
    "challenge": "...",
    "recommended_experiment": "...",
    "reasoning": "...",
    "confidence": 0,
    "discount": 0,
    "budget": 0,
    "audience_size": 0
}}

IMPORTANT:

- strongest_segment MUST use an actual segment from the verified data.
- discount MUST be between 0 and 10.
- budget MUST be between 0 and 10000.
- audience_size MUST be between 0 and 1500.
- Do not invent customer segments.
- Do not return markdown.
- Return JSON only.
"""

    # =========================================================
    # GEMINI RESILIENCE
    # =========================================================

    last_error = None

    # Give Gemini one attempt.
    # If unavailable, immediately use MAYA's deterministic fallback.
    for attempt in range(1):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            text = response.text.strip()

            # Remove accidental markdown fences if Gemini
            # ever returns them despite the JSON-only instruction.
            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            recommendation = json.loads(text)

            print(
                "Gemini recommendation generated successfully."
            )

            return recommendation

        except Exception as e:

            last_error = str(e)

            print(
                f"Gemini attempt {attempt + 1}/1 failed: "
                f"{last_error}"
            )


    # =========================================================
    # SAFE FALLBACK
    # =========================================================

    print(
        "Gemini unavailable. MAYA will use deterministic fallback."
    )

    return {
        "ai_status": "UNAVAILABLE",
        "error": last_error,
        "fallback_required": True
    }


if __name__ == "__main__":

    recommendation = ask_gemini()

    print(
        json.dumps(
            recommendation,
            indent=2
        )
    )