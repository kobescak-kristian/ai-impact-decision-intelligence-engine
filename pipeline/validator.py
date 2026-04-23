from typing import Tuple, List
from models.schemas import LeadRecord, Decision, Outcome
from utils.logger import get_logger

logger = get_logger(__name__)

VALID_DECISIONS = {d.value for d in Decision}
VALID_OUTCOMES = {o.value for o in Outcome}


def validate_lead(record: dict) -> Tuple[bool, List[str]]:
    """
    Validate a raw lead dict before ingestion.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # Required fields
    for field in ("lead_id", "decision", "confidence_score", "outcome", "lead_value"):
        if field not in record or record[field] is None:
            errors.append(f"Missing required field: {field}")

    if errors:
        return False, errors

    # Decision must be known
    if record["decision"] not in VALID_DECISIONS:
        errors.append(
            f"Invalid decision '{record['decision']}'. Must be one of: {VALID_DECISIONS}"
        )

    # Outcome must be known
    if record["outcome"] not in VALID_OUTCOMES:
        errors.append(
            f"Invalid outcome '{record['outcome']}'. Must be one of: {VALID_OUTCOMES}"
        )

    # Confidence score must be 0–1
    try:
        score = float(record["confidence_score"])
        if not (0.0 <= score <= 1.0):
            errors.append(
                f"confidence_score must be between 0.0 and 1.0, got {score}"
            )
    except (ValueError, TypeError):
        errors.append("confidence_score must be a number")

    # Lead value must be positive
    try:
        value = float(record["lead_value"])
        if value <= 0:
            errors.append(f"lead_value must be greater than 0, got {value}")
    except (ValueError, TypeError):
        errors.append("lead_value must be a number")

    is_valid = len(errors) == 0
    if not is_valid:
        logger.warning(f"Validation failed for lead {record.get('lead_id')}: {errors}")

    return is_valid, errors


def validate_batch(records: List[dict]) -> Tuple[List[dict], List[dict]]:
    """
    Validate a list of lead records.
    Returns (valid_records, invalid_records_with_errors).
    """
    valid = []
    invalid = []

    for record in records:
        is_valid, errors = validate_lead(record)
        if is_valid:
            valid.append(record)
        else:
            invalid.append({"record": record, "errors": errors})

    logger.info(f"Batch validation: {len(valid)} valid, {len(invalid)} invalid")
    return valid, invalid
