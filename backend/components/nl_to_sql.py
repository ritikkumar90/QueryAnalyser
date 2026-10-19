"""
nl_to_sql.py
------------
Converts a natural-language user question into a SQL query
by sending it to an LLM with the database schema as context.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

from components.schema_builder import build_schema_context

load_dotenv()

REQUESTY_API_KEY = os.getenv("REQUESTY_API_KEY")


def _build_system_prompt(engine) -> str:
    """Build the system prompt containing the live database schema."""
    schema = build_schema_context(engine)
    return f"""You are an expert SQL generator for a MySQL database.

DATABASE SCHEMA:
{schema}

NOTES:
- order_status values: delivered, shipped, canceled, invoiced, ...
- Data covers 2016-09 to 2018-10. Never use today's date for "this month" or "last year".

RULES:
- Output ONLY one SQL query, no explanation, no markdown.
- Use ONLY the tables and columns listed in the schema.
- SELECT statements only.
- Add LIMIT 100 unless the query is an aggregate.
- If the question can't be answered from this schema, output: UNANSWERABLE

EXAMPLES:
Q: How many canceled orders are there?
SQL: SELECT COUNT(*) FROM orders WHERE order_status = 'canceled';
"""


def get_llm_client() -> OpenAI:
    """Return a configured OpenAI-compatible client pointing at Requesty."""
    return OpenAI(
        api_key=REQUESTY_API_KEY,
        base_url="https://router.requesty.ai/v1",
    )


def convert_to_sql(user_query: str, engine) -> str | None:
    """
    Send *user_query* to the LLM and return the generated SQL string,
    or ``None`` on failure.
    """
    client = get_llm_client()
    system_prompt = _build_system_prompt(engine)

    try:
        response = client.chat.completions.create(
            model="google/gemma-4-31b-it",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"[nl_to_sql] Error: {e}")
        return None
