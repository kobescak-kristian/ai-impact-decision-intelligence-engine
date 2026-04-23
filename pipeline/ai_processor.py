from typing import List
from models.schemas import ImpactResponse
from pipeline.impact_evaluator import evaluate_impact
from pipeline.impact_analyzer import analyze_impact
from utils.logger import get_logger

logger = get_logger(__name__)


def run_impact_pipeline(leads: List[dict]) -> ImpactResponse:
    """
    Orchestrates the full impact pipeline:
      1. Deterministic evaluation (no LLM)
      2. AI analysis + recommendations (LLM or simulation)

    Keeps layers explicitly separated.
    """
    logger.info(f"Running impact pipeline on {len(leads)} leads")

    # Step 1 — deterministic metrics
    metrics, enriched = evaluate_impact(leads)

    # Step 2 — AI interpretation (receives metrics only, not raw lead data)
    analysis, recommendations = analyze_impact(metrics)

    return ImpactResponse(
        metrics=metrics,
        analysis=analysis,
        recommendations=recommendations,
    )
