import os
from dotenv import load_dotenv
from openai import OpenAI
from test3 import build_schema_context
from database import engine
load_dotenv()

REQUESTY_API_KEY = os.getenv("REQUESTY_API_KEY")
SYSTEM_PROMPT = f"""You are an expert SQL generator for a MySQL database.

DATABASE SCHEMA:
{build_schema_context(engine)}

NOTES:
- order_status values: deslivered, shipped, canceled, invoiced, ...
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
client = OpenAI(
    api_key=REQUESTY_API_KEY,
    base_url="https://router.requesty.ai/v1"
)

def convert_to_sql(user_query:str)-> str:
    try: 
        response = client.chat.completions.create(
            model="google/gemma-4-31b-it",
            temperature=0,
            messages=[
                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },
                {
                    "role":"user",
                    "content":user_query
                }
            ]
        )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Unknown Error {e}")
        return None

if __name__ == "__main__":
    user_query = "select the cancelled order august 2018"
    response = convert_to_sql(user_query)
    print(f"User Prompt: {user_query}")
    print(f"Model response : {response}")
