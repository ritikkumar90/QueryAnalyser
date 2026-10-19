"""
data_summarizer.py
------------------
Takes the user's original question, the generated SQL, and the query
result rows, then asks an LLM to produce a clear, human-readable
English answer.
"""

import json
from components.nl_to_sql import get_llm_client


SUMMARIZER_SYSTEM_PROMPT = """You are a helpful data analyst assistant.

You will receive:
1. The user's original question
2. The SQL query that was executed
3. The result rows returned by the database

Your job is to answer the user's question in clear, natural English based on the data.

RULES:
- Be concise but informative. Use bullet points or numbered lists for multiple items.
- Include specific numbers from the data.
- If the data is empty, say so clearly.
- Do NOT output any SQL or code.
- Do NOT make up information not present in the data.
- Format numbers nicely (e.g. 1,234 instead of 1234, round decimals to 2 places).
"""


def summarize_results(
    question: str,
    sql: str,
    columns: list[str],
    rows: list[dict],
) -> str | None:
    """
    Send the question + query results to the LLM and return a
    human-readable English summary, or ``None`` on failure.
    """
    # Build a compact representation of the data for the prompt
    # Limit to first 50 rows to avoid token overflow
    display_rows = rows[:50]
    data_text = json.dumps(
        {"columns": columns, "rows": display_rows},
        indent=2,
        default=str,
    )

    user_message = f"""QUESTION: {question}

SQL EXECUTED:
{sql}

RESULT DATA ({len(rows)} row{"s" if len(rows) != 1 else ""} total{", showing first 50" if len(rows) > 50 else ""}):
{data_text}

Please answer the question above in plain English based on this data."""

    client = get_llm_client()

    try:
        response = client.chat.completions.create(
            model="google/gemma-4-31b-it",
            temperature=0.3,
            messages=[
                {"role": "system", "content": SUMMARIZER_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"[data_summarizer] Error: {e}")
        return None
