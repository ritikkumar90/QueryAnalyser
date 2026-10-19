from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from database import engine
from scheme import QueryRequest
from components.nl_to_sql import convert_to_sql
from components.query_sanitizer import sanitize_query
from components.data_summarizer import summarize_results


router = APIRouter(prefix="/query")


@router.post("/")
def run_query(body: QueryRequest):
    """Accept a natural-language question, convert it to SQL, execute it, and return the results."""

    # Step 1 — LLM generates SQL from the question
    sql = convert_to_sql(body.question, engine)

    if sql is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="LLM failed to generate a response.",
        )

    if sql.strip().upper() == "UNANSWERABLE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The question cannot be answered from the available data.",
        )

    # Step 2 — sanitize and execute
    safe_sql = sanitize_query(sql)

    try:
        with engine.connect() as conn:
            result = conn.execute(text(safe_sql))
            columns = list(result.keys())
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Generated SQL failed to execute: {e}",
        )

    # Step 3 — LLM summarizes the results into plain English
    answer = summarize_results(
        question=body.question,
        sql=sql,
        columns=columns,
        rows=rows,
    )

    return {
        "question": body.question,
        "generated_sql": sql,
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "answer": answer,
    }

