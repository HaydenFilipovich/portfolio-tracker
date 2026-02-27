import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent / "portfolio.db"


def _get_conn() -> sqlite3.Connection:
    """Return a connection to the SQLite database (one per call)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create the holdings table if it doesn't exist."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS holdings (
                ticker    TEXT PRIMARY KEY,
                shares    REAL NOT NULL,
                avg_cost  REAL NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)


def load_holdings() -> list[dict]:
    """Read all holdings from the DB into a list of dicts."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT ticker, shares, avg_cost FROM holdings ORDER BY ticker"
        ).fetchall()
    return [
        {"ticker": r[0], "shares": r[1], "cost_basis": r[2]}
        for r in rows
    ]


def upsert_holding(ticker: str, shares: float, cost: float) -> None:
    """Insert or merge a holding using weighted-average cost."""
    now = pd.Timestamp.now().isoformat()
    with _get_conn() as conn:
        existing = conn.execute(
            "SELECT shares, avg_cost FROM holdings WHERE ticker = ?", (ticker,)
        ).fetchone()
        if existing:
            old_shares, old_cost = existing
            new_shares = old_shares + shares
            new_avg = (old_shares * old_cost + shares * cost) / new_shares
            conn.execute(
                "UPDATE holdings SET shares = ?, avg_cost = ?, updated_at = ? WHERE ticker = ?",
                (new_shares, new_avg, now, ticker),
            )
        else:
            conn.execute(
                "INSERT INTO holdings (ticker, shares, avg_cost, updated_at) VALUES (?, ?, ?, ?)",
                (ticker, shares, cost, now),
            )


def remove_holding(ticker: str) -> None:
    """Delete a ticker from the DB."""
    with _get_conn() as conn:
        conn.execute("DELETE FROM holdings WHERE ticker = ?", (ticker,))
