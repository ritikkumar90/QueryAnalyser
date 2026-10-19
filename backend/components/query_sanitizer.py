"""
query_sanitizer.py
------------------
Utilities for cleaning and validating SQL queries returned by the LLM
before they are executed against the database.
"""


def sanitize_query(query: str) -> str:
    """
    Strip leading/trailing whitespace and remove a trailing semicolon
    so the query can be safely wrapped in a SQLAlchemy `text()` call.
    """
    return query.strip().rstrip(";").strip()
