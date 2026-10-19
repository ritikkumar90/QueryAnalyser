from sqlalchemy import inspect, text
from database import engine
from datetime import datetime, date


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM orders LIMIT 3"))
#     rows = result.fetchall()
    
# for row in rows:
#     print(row)
def clean(value):
    if isinstance(value, (date, datetime)):
        str(value)
        return value
    else:
        return value

def build_schema_context(engine):
    ins = inspect(engine)
    table_names = ins.get_table_names()
    lines = []
    with engine.connect() as conn:
        for table in table_names:
            lines.append(f"TABLE {table}")
            for col in ins.get_columns(table):
                add_column=f" -- {col['name']}  {col['type']}"
                lines.append(add_column)
            lines.append("  Sample rows: ")
            result = conn.execute(text(f"SELECT * FROM {table} LIMIT 2"))
            rows = result.fetchall()
            for row in rows:
                cleaned = tuple(clean(item) for item in row)
                lines.append(str(cleaned))
            
            
    return  "\n".join(lines)

if __name__ == "__main__":
    schema_structure = build_schema_context(engine)
    print(schema_structure)

