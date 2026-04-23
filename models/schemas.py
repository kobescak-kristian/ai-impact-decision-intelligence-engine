from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


# ── Enums ──────────────────────────────────────────────────────────────────────

class Decision(str, Enum):
    send_to_sales = "send_to_sales"
    archived = "archived"
    manual_review = "manual_review"


class Outcome(str, Enum):
    converted = "converted"
    not_converted = "not_converted"
    later_converted = "later_converted"
    converted_delayed = "converted_delayed"
    pending = "pending"


class ValueTier(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class CustomerType(str, Enum):
    enterprise = "enterprise"
    smb = "smb"
    individual = "individual"


# ── Input / Storage ────────────────────────────────────────────────────────────

class LeadRecord(BaseModel):
    lead_id: str
    decision: Decision
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    outcome: Outcome
    lead_value: float = Field(..., gt=0)
    customer_type: Optional[CustomerType] = None
    value_tier: Optional[ValueTier] = None
    source: Optional[str] = None
    timestamp: Optional[datetime] = None


# ── Impact Metrics (deterministic) ────────────────────────────────────────────

class ImpactMetrics(BaseModel):
    total_leads: int
    total_revenue_generated: float
    total_revenue_lost: float
    missed_opportunity_value: float
    false_positive_cost: float
    delayed_opportunity_value: float
    net_impact: float

    # Supporting ratios
    conversion_rate: float
    false_positive_rate: float
    missed_opportunity_rate: float
    avg_confidence_converted: float
    avg_confidence_not_converted: float

    # Counts
    converted_count: int
    not_converted_count: int
    archived_later_converted_count: int
    manual_review_converted_count: int


# ── AI Analysis ────────────────────────────────────────────────────────────────

class Recommendation(BaseModel):
    action: str
    from_value: Optional[float] = None
    to_value: Optional[float] = None
    reason: str
    expected_effect: str
    tradeoff: str


class ImpactAnalysis(BaseModel):
    summary: str
    key_issues: List[str]
    root_causes: List[str]
    simulated: bool = False


# ── API Response ───────────────────────────────────────────────────────────────

class ImpactResponse(BaseModel):
    metrics: ImpactMetrics
    analysis: ImpactAnalysis
    recommendations: List[Recommendation]


class LeadImpactResponse(BaseModel):
    lead_id: str
    decision: str
    outcome: str
    lead_value: float
    confidence_score: float
    financial_impact: float
    impact_type: str
    notes: str
