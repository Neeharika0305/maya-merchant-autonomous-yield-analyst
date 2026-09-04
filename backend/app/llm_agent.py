import json

from app.agent_tools import build_agent_context, get_tool_catalog


SYSTEM_PROMPT = """
You are MAYA — Merchant Autonomous Yield Analyst.

Your job is to identify profitable growth opportunities for an e-commerce merchant.

You operate under strict rules:

1. Use only approved tools.
2. Never invent merchant data.
3. Never access the database directly.
4. Challenge assumptions before recommending an experiment.
5. Prefer high-intent customer segments.
6. Respect merchant guardrails.
7. Every recommendation must be explainable.
8. Optimize for incremental profit, not vanity metrics.

Your reasoning loop is:

DISCOVER → HYPOTHESIZE → CHALLENGE → EXPERIMENT → MEASURE → ADAPT
"""


def build_llm_prompt():
    """
    Build a structured prompt from MAYA's approved tool context.
    """

    context = build_agent_context()
    tools = get_tool_catalog()

    return {
        "system": SYSTEM_PROMPT,
        "tools": tools,
        "merchant_context": context,
        "instruction": """
Analyze the merchant context.

Identify:
- the strongest customer segment
- the strongest product opportunity
- the most promising hypothesis
- why the hypothesis should be challenged
- what experiment should be tested
- what guardrails should apply

Return your reasoning as structured JSON.
"""
    }


def get_agent_prompt_json():
    """
    Return the complete structured AI context.
    """
    return json.dumps(
        build_llm_prompt(),
        indent=2,
        default=str
    )