import React, { useState } from "react";
import "./QueryPage.css";

export default function QueryPage() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/query/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question.trim() }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.detail || "Something went wrong.");
      }
    } catch (err) {
      setError("Could not reach the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const exampleQuestions = [
    "How many canceled orders are there?",
    "Top 5 cities by number of customers",
    "Average review score by product category",
    "Total revenue from credit card payments",
  ];

  return (
    <section className="query-page">
      {/* -------- Header -------- */}
      <div className="query-header">
        <h1 className="query-title">
          Ask your <span className="gradient-text">Data</span>
        </h1>
        <p className="query-subtitle">
          Type a question in plain English and get instant SQL‑powered answers
          from the database.
        </p>
      </div>

      {/* -------- Input -------- */}
      <form className="query-form" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <svg
            className="search-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            id="query-input"
            type="text"
            placeholder="e.g. How many orders were delivered in 2018?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            autoComplete="off"
          />
          <button
            type="submit"
            className="query-submit"
            disabled={loading || !question.trim()}
          >
            {loading ? (
              <span className="spinner" />
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                width="20"
                height="20"
              >
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            )}
          </button>
        </div>
      </form>

      {/* -------- Quick prompts -------- */}
      {!result && !error && (
        <div className="example-chips">
          {exampleQuestions.map((q) => (
            <button
              key={q}
              className="chip"
              onClick={() => {
                setQuestion(q);
              }}
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* -------- Error -------- */}
      {error && (
        <div className="query-error">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
          <span>{error}</span>
        </div>
      )}

      {/* -------- Results -------- */}
      {result && (
        <div className="query-results">
          {/* AI Answer */}
          {result.answer && (
            <div className="answer-card">
              <div className="answer-card-header">
                <span className="answer-badge">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6z" />
                  </svg>
                  AI Answer
                </span>
              </div>
              <div className="answer-body">
                {result.answer}
              </div>
            </div>
          )}

          {/* SQL card */}
          <div className="sql-card">
            <div className="sql-card-header">
              <span className="sql-badge">Generated SQL</span>
              <span className="row-count">{result.row_count} row{result.row_count !== 1 ? "s" : ""}</span>
            </div>
            <pre className="sql-code"><code>{result.generated_sql}</code></pre>
          </div>

          {/* Data table */}
          {result.rows.length > 0 ? (
            <div className="table-wrapper">
              <table className="result-table">
                <thead>
                  <tr>
                    {result.columns.map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.rows.map((row, i) => (
                    <tr key={i}>
                      {result.columns.map((col) => (
                        <td key={col}>{row[col] != null ? String(row[col]) : "—"}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="no-rows">Query executed successfully but returned no rows.</p>
          )}
        </div>
      )}
    </section>
  );
}
