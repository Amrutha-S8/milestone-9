"""FastAPI Router for StayZa Milestone 9.

Endpoints:
- POST /language/analyze: NLU endpoint returning language, intent, entities, next_action, confidence.
- POST /language/detect: Standalone language detection endpoint.
- GET  /language/session/{session_id}: Retrieves multi-turn session context.
- GET  /language/supported: Returns list of supported languages.
- GET  /language/evaluate: Runs evaluation suite against benchmark datasets.
- POST /evaluation/run: Runs full evaluation engine with scoring, pass/fail, and reporting.
- GET  /evaluation/results: Returns latest evaluation results.
- GET  /languages/status: Returns pass/fail status for all languages.
- GET  /review/flagged: Returns low-confidence utterances logged for manual review.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import (
    get_entity_extractor,
    get_evaluation_engine,
    get_intent_classifier,
    get_language_detector,
    get_language_registry,
    get_normalization_service,
    get_review_auditor,
    get_session_manager,
)
from api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    EvaluationRunResponse,
    LanguageDetectRequest,
    LanguageDetectResponse,
    LanguageStatusResponse,
    LanguageSupportInfo,
    SessionContextResponse,
)
from datasets.loader import DatasetLoader
from detection.detector import LanguageDetector
from entities.extractor import EntityExtractor
from evaluation.accuracy import IntentAccuracyEvaluator
from evaluation.engine import EvaluationEngine
from intent.classifier import IntentClassifier
from languages.registry import LanguageRegistry
from normalization.service import TextNormalizationService
from review_system.auditor import ReviewAuditor
from session.manager import SessionManager

router = APIRouter(prefix="/language", tags=["Language Flows & NLU Engine"])


@router.post(
    "/detect",
    response_model=LanguageDetectResponse,
    status_code=status.HTTP_200_OK,
    summary="Automatic Language Detection Service",
    description="Detects language and confidence score for any input text."
)
async def detect_language(
    request: LanguageDetectRequest,
    detector: LanguageDetector = Depends(get_language_detector)
) -> LanguageDetectResponse:
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field cannot be empty."
        )

    res = detector.detect(request.text)
    return LanguageDetectResponse(
        language=res["language"],
        confidence=res["confidence"]
    )


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Utterance with NLU Engine (Language, Intent, Entities, Action)",
    description="Processes STT transcription text, classifies intent, extracts booking entities, manages session state, and outputs next dialog action."
)
async def analyze_language(
    request: AnalyzeRequest,
    registry: LanguageRegistry = Depends(get_language_registry),
    intent_engine: IntentClassifier = Depends(get_intent_classifier),
    extractor: EntityExtractor = Depends(get_entity_extractor),
    session_mgr: SessionManager = Depends(get_session_manager),
    auditor: ReviewAuditor = Depends(get_review_auditor),
    normalizer: TextNormalizationService = Depends(get_normalization_service)
) -> AnalyzeResponse:
    """
    Day 4 Upgraded Primary NLU Endpoint.

    Pipeline (in order):
        0. Text Normalization  — lowercase, noise removal, abbreviation expansion.
        1. Language & Flow     — detect language, advance dialog state.
        2. Entity Extraction   — extract structured booking slots.
        3. Session Management  — accumulate slots across turns.
        4. Audit Logging       — flag low-confidence turns for review.

    Accepts:
        {"text": "Book a A/C room in Bengaluru tmrw for 2 guests"}

    Returns:
        {
          "language": "English",
          "intent": "booking",
          "entities": {"room_type": "ac", "guests": 2, "check_in": "tomorrow"},
          "next_action": "ask_checkin_date",
          "confidence": 0.97,
          "normalized_text": "book a ac room in bangalore tomorrow for 2 guests"
        }
    """
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field cannot be empty."
        )

    # ── Step 0: Text Normalization ─────────────────────────────────────────
    # Normalize BEFORE any NLU so all downstream modules receive clean text.
    # We keep the original text only for the audit log.
    norm_result = normalizer.normalize(request.text)
    normalized_text = norm_result.normalized_text

    # ── Step 1: Language Detection & Flow Transition ───────────────────────
    flow_result = registry.detect_and_process(
        text=normalized_text,
        current_state=request.current_state
    )

    # ── Step 2: Entity Extraction (on normalized text) ─────────────────────
    extracted_entities = extractor.extract(normalized_text)
    # Merge slots surfaced by the flow engine (e.g. response_template)
    for k, v in flow_result.slots.items():
        if k != "response_template" and k not in extracted_entities:
            extracted_entities[k] = v

    # ── Step 3: Session State & Multi-Turn Slot Accumulation ──────────────
    sess_id = request.session_id or "sess_default"
    session_state = session_mgr.update_session_turn(
        session_id=sess_id,
        user_text=request.text,          # store raw text in history
        detected_language=flow_result.language,
        intent=flow_result.intent,
        next_action=flow_result.next_action,
        new_entities=extracted_entities
    )

    # Merge current turn entities into accumulated session memory
    combined_entities = {**session_state.slot_memory}

    # ── Step 4: Audit Log ─────────────────────────────────────────────────
    auditor.inspect_and_log(
        text=request.text,               # audit against original
        language=flow_result.language,
        intent=flow_result.intent,
        confidence=flow_result.confidence,
        next_action=flow_result.next_action,
        session_id=sess_id
    )

    return AnalyzeResponse(
        language=flow_result.language,
        intent=flow_result.intent,
        entities=combined_entities,
        next_action=flow_result.next_action,
        confidence=flow_result.confidence,
        flow=flow_result.intent,
        session_id=sess_id,
        response_template=flow_result.slots.get("response_template"),
        normalized_text=normalized_text
    )


@router.get(
    "/session/{session_id}",
    response_model=SessionContextResponse,
    summary="Get Conversation Session State",
    description="Retrieves active session state, accumulated slot memory, and conversation turn history."
)
async def get_session_context(
    session_id: str,
    session_mgr: SessionManager = Depends(get_session_manager)
) -> SessionContextResponse:
    state = session_mgr.get_or_create_session(session_id)
    return SessionContextResponse(
        session_id=state.session_id,
        active_language=state.active_language,
        active_flow=state.active_flow,
        current_intent=state.current_intent,
        slot_memory=state.slot_memory,
        history=[h.dict() for h in state.history]
    )


@router.get(
    "/supported",
    response_model=list[LanguageSupportInfo],
    summary="List Supported Languages",
    description="Returns metadata for currently active language flow modules."
)
async def list_supported_languages(
    registry: LanguageRegistry = Depends(get_language_registry)
) -> list[LanguageSupportInfo]:
    supported = registry.list_supported_languages()
    info_list = []
    
    for lang_name in supported:
        flow = registry.get_flow(lang_name)
        info_list.append(
            LanguageSupportInfo(
                code=flow.language_code if flow else "en",
                name=lang_name,
                status="active",
                supported_intents=[
                    "greeting", "booking", "availability", "price_enquiry",
                    "cancellation", "modify_booking", "check_status", "goodbye", "unknown"
                ]
            )
        )
    return info_list


@router.get(
    "/evaluate",
    summary="Run Benchmark Evaluation Suite",
    description="Executes automated accuracy evaluation on ground truth benchmark dataset."
)
async def run_benchmark_evaluation(
    registry: LanguageRegistry = Depends(get_language_registry)
) -> dict[str, Any]:
    loader = DatasetLoader()
    items = loader.load()
    evaluator = IntentAccuracyEvaluator(registry)
    return evaluator.evaluate(items)


@router.get(
    "/review/flagged",
    summary="Get Flagged Utterances for Manual Review",
    description="Retrieves low-confidence or unknown intent utterances for human audit."
)
async def get_flagged_reviews(
    auditor: ReviewAuditor = Depends(get_review_auditor)
) -> list[dict[str, Any]]:
    return auditor.get_flagged_utterances()


# ══════════════════════════════════════════════════════════════════════════════
# Day 5: Evaluation Engine Endpoints
# ══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/evaluation/run",
    response_model=EvaluationRunResponse,
    summary="Run Full Evaluation Engine",
    description="Executes complete evaluation pipeline: accuracy, WER, flow completion, latency, scoring, and pass/fail."
)
async def run_full_evaluation(
    engine: EvaluationEngine = Depends(get_evaluation_engine)
) -> dict[str, Any]:
    results = engine.run_full_evaluation()
    return {
        "summary": results["summary"],
        "per_language": results["per_language"],
        "report_path": results["report_path"],
        "status": results["status"]
    }


@router.get(
    "/evaluation/results",
    summary="Get Latest Evaluation Results",
    description="Returns the most recent evaluation engine results."
)
async def get_evaluation_results(
    engine: EvaluationEngine = Depends(get_evaluation_engine)
) -> dict[str, Any]:
    results = engine.get_last_results()
    if results is None:
        return {"message": "No evaluation has been run yet. POST /language/evaluation/run first."}
    return results


@router.get(
    "/languages/status",
    response_model=dict[str, LanguageStatusResponse],
    summary="Get Language Pass/Fail Status",
    description="Returns evaluation pass/fail status for every supported language."
)
async def get_languages_status(
    engine: EvaluationEngine = Depends(get_evaluation_engine)
) -> dict[str, Any]:
    results = engine.get_last_results()
    if results is None:
        return {}
    statuses = {}
    for lang in engine.config.supported_languages:
        status_data = engine.get_language_status(lang)
        if status_data:
            statuses[lang] = LanguageStatusResponse(**status_data)
    return statuses
