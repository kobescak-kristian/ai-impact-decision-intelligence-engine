# AI Impact & Decision Intelligence Engine — v1.0

Most AI systems make decisions.

Very few know if those decisions were actually correct.

Even fewer measure what those decisions actually cost.

This system measures the financial impact of AI lead routing decisions and recommends how to improve them.

**System design | AI evaluation pipeline | FastAPI + Python**

---

![Impact Overview](impact_overview.png)

---

## The Problem

AI systems route leads (send to sales, archive, manual review), but almost no system measures the **financial consequence of those decisions**.

As a result:

- False positives waste sales effort  
- Missed opportunities lose revenue silently  
- No feedback loop exists to improve decision thresholds  

**Who has this problem:**

- Revenue operations teams  
- AI automation builders  
- Sales ops managing lead qualification pipelines  

---

## Why This Matters

Most AI systems optimise accuracy.

This system optimises **business impact**.

It shows:

- What decisions generated revenue  
- What decisions lost money  
- Where thresholds are misaligned  
- What to change to improve outcomes  

---

## What This System Does

This system acts as a **decision intelligence layer** on top of an existing AI pipeline.

It connects:

**Decision → Outcome → Financial Impact → Recommendation**

It does NOT make business decisions.

It evaluates them and translates them into measurable financial consequences.

---

## Outcome (Simulated)

- 75 leads processed  
- Revenue generated: €165,170  
- Revenue lost: €49,060  
- Net impact: €116,110  

- Conversion rate: 41.3%  
- False positive rate: 45.2%  
- Missed opportunity rate: 44.4%  

- 4 structured recommendations generated  

**Note:**  
Dataset intentionally constructed to produce both positive and negative outcomes for evaluation demonstration.

---

## Architecture

![Impact Architecture](impact_architecture.png)

---

## How It Works

Pipeline:

1. Input validation  
2. Impact classification (maps decision + outcome → financial category)  
3. Per-lead financial calculation  
4. Aggregate metrics computation  
5. AI interpretation (metrics only)  
6. Recommendation generation  
7. API response  

---

## Business Value

- Makes hidden revenue loss visible  
- Quantifies cost of wrong AI decisions  
- Enables threshold optimisation  
- Reduces reliance on manual analysis  
- Creates a continuous feedback loop  

---

## Example

### Input

```json
{
  "decision": "archived",
  "confidence": 0.38,
  "outcome": "later_converted",
  "lead_value": 5500
}

---

## Known Limitations

### Financial multipliers are not calibrated from real data**
False positive cost (15% of lead value) and delay penalty (10%) are fixed constants defined in `config/settings.py`. All financial output, including the net impact figure, is calculated against these assumed values. In production, these would need to be derived from actual sales cycle costs per customer segment.

### Outcome data reliability**
The `later_converted` and `converted_delayed` outcome types require a feedback loop that does not exist in this system. In production, outcome data is partial, delayed, and often absent. The missed opportunity value (the largest loss figure in the demo) is therefore the least reliable metric.
### Recommendations are not anchored to current system state**
The impact analyzer recommends threshold changes (e.g. increase from 0.60 to 0.68) without knowing what the actual upstream threshold is set to. In simulation mode, the `from_value` in recommendations is an illustrative default, not read from system config.

### No coverage gate**
The evaluator runs full analysis regardless of how many leads have outcomes recorded. A system with 10% outcome coverage will produce the same confident-looking metrics as one with 90% coverage. A coverage gate (returning `insufficient_data` below a defined threshold) is not implemented in v1.

### Not production-ready**
- No authentication on API endpoints
- SQLite is not suitable for concurrent writes at scale
- No date range filtering on `/impact` — runs over full dataset
- Dataset is simulated and intentionally constructed to demonstrate both strong and weak decision performance
