"""
schema_builder.py
-----------------
Introspects the database schema and builds a text representation
that is injected into the LLM system prompt so the model knows
which tables / columns / sample rows are available.
"""

from sqlalchemy import inspect, text
from datetime import datetime, date


def clean(value):
    """Convert date/datetime objects to strings for readable sample rows."""
    if isinstance(value, (date, datetime)):
        return str(value)
    return value


def build_schema_context(engine):
    """
    Return a multi-line string describing every table in the database:
      TABLE <name>
       -- <column>  <type>
       ...
       Sample rows:
       (val, val, ...)
    """
    ins = inspect(engine)
    table_names = ins.get_table_names()
    lines = []

    with engine.connect() as conn:
        for table in table_names:
            lines.append(f"TABLE {table}")

            for col in ins.get_columns(table):
                lines.append(f"  -- {col['name']}  {col['type']}")

            lines.append("  Sample rows:")
            result = conn.execute(text(f"SELECT * FROM {table} LIMIT 2"))
            rows = result.fetchall()
            for row in rows:
                cleaned = tuple(clean(item) for item in row)
                lines.append(f"  {cleaned}")

    return "\n".join(lines)
