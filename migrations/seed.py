import json
import logging
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from review_system.models import Reviewer, Conversation, Review, Rating, Approval
from evaluation.config import EvaluationConfig

logger = logging.getLogger("stayza.migrations.seed")

SEED_REVIEWERS = [
    {"name": "Ravi Sharma", "languages": ["English", "Hindi"]},
    {"name": "Priya Patel", "languages": ["Hindi", "Marathi"]},
    {"name": "Aisha Khan", "languages": ["Hinglish", "English"]},
    {"name": "Venkatesh Rao", "languages": ["Telugu", "English"]},
    {"name": "Lakshmi Nair", "languages": ["Malayalam", "English"]},
]


def seed_reviewers(db: Session) -> list[Reviewer]:
    reviewers = []
    for data in SEED_REVIEWERS:
        existing = db.query(Reviewer).filter(Reviewer.name == data["name"]).first()
        if existing:
            reviewers.append(existing)
            continue
        reviewer = Reviewer(name=data["name"], languages=data["languages"])
        db.add(reviewer)
        reviewers.append(reviewer)
    db.commit()
    for r in reviewers:
        db.refresh(r)
    logger.info("Seeded %d reviewers", len(reviewers))
    return reviewers


def seed_benchmark_conversations(db: Session, reviewers: list[Reviewer], datasets_dir: str = "datasets"):
    config = EvaluationConfig()
    supported = config.supported_languages
    created = 0

    for lang in supported:
        filepath = Path(datasets_dir) / f"{lang.lower()}.json"
        if not filepath.exists():
            logger.warning("Dataset not found: %s", filepath)
            continue

        with open(filepath, encoding="utf-8") as f:
            items = json.load(f)

        reviewer = next((r for r in reviewers if lang in r.languages), reviewers[0])
        for item in items[:10]:
            text = item.get("text", item.get("utterance", ""))
            if not text:
                continue
            conv = Conversation(
                conversation_id=f"seed_{lang.lower()}_{created}",
                reviewer_id=reviewer.id,
                language=lang,
                original_text=text,
                normalized_text=text.lower().strip(),
                detected_language=lang,
                detected_intent=item.get("intent", item.get("expected_intent", "unknown")),
                entities=item.get("entities", {}),
                expected_intent=item.get("expected_intent", item.get("intent", "unknown")),
                evaluation_score=item.get("evaluation_score", 85.0),
                latency_ms=item.get("latency_ms", 100.0),
            )
            db.add(conv)
            created += 1

    db.commit()
    logger.info("Seeded %d benchmark conversations", created)
    return created


def seed_evaluation_history(db: Session, engine):
    from datetime import datetime, timezone
    results = engine._last_results
    if not results:
        logger.info("No evaluation results to seed")
        return

    per_language = results.get("per_language", {})
    status_data = results.get("status", {}).get("per_language", {})
    for lang, scores in per_language.items():
        lang_status = status_data.get(lang, {})
        record = {
            "language": lang,
            "intent_accuracy_pct": scores.get("intent_accuracy_pct", 0),
            "wer_pct": scores.get("wer_pct", 0),
            "flow_completion_pct": scores.get("flow_completion_pct", 0),
            "avg_latency_ms": scores.get("avg_latency_ms", 0),
            "final_score": scores.get("final_score", 0),
            "status": lang_status.get("status", "UNKNOWN"),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
        logger.info("Evaluation history: %s -> score=%.1f status=%s", lang, record["final_score"], record["status"])
