import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = "impact_engine.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                lead_id         TEXT PRIMARY KEY,
                decision        TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                outcome         TEXT NOT NULL,
                lead_value      REAL NOT NULL,
                customer_type   TEXT,
                value_tier      TEXT,
                source          TEXT,
                timestamp       TEXT,
                created_at      TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
        logger.info("Database initialised — leads table ready")
    finally:
        conn.close()


def insert_lead(lead: dict) -> None:
    conn = get_connection()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO leads
                (lead_id, decision, confidence_score, outcome, lead_value,
                 customer_type, value_tier, source, timestamp)
            VALUES
                (:lead_id, :decision, :confidence_score, :outcome, :lead_value,
                 :customer_type, :value_tier, :source, :timestamp)
        """, lead)
        conn.commit()
    finally:
        conn.close()


def get_all_leads() -> List[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM leads ORDER BY timestamp ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_lead_by_id(lead_id: str) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM leads WHERE lead_id = ?", (lead_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_lead_count() -> int:
    conn = get_connection()
    try:
        result = conn.execute("SELECT COUNT(*) FROM leads").fetchone()
        return result[0]
    finally:
        conn.close()
