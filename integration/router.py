import time

from fastapi import APIRouter, HTTPException, Request, status

from integration.cache import get_cache
from integration.logging import get_integration_logger
from integration.service import IntegrationService

router = APIRouter(prefix="/api/v1", tags=["Integration"])


def get_integration_service(request: Request) -> IntegrationService:
    service = getattr(request.app.state, "integration_service", None)
    if service is None:
        engine = getattr(request.app.state, "evaluation_engine", None)
        service = IntegrationService(engine=engine)
        request.app.state.integration_service = service
    return service


@router.post("/analyze", summary="Analyze a single utterance")
async def analyze_utterance(
    request: Request,
    body: dict,
):
    logger = get_integration_logger()
    start = time.perf_counter()

    text = body.get("text", "")
    if not text or not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text field cannot be empty")
    if len(text) > 10000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text exceeds maximum length of 10000 characters")

    logger.info("ANALYZE language=%s text_length=%d", body.get("language"), len(text))

    service = get_integration_service(request)
    result = service.analyze_utterance(
        text=text,
        language=body.get("language"),
        reference_text=body.get("reference_text"),
        intent_label=body.get("intent_label"),
        entities=body.get("entities"),
        critical_fields=body.get("critical_fields"),
        tool_name=body.get("tool_name"),
        conversation_id=body.get("conversation_id"),
        utterance_id=body.get("utterance_id"),
    )

    duration = (time.perf_counter() - start) * 1000
    logger.performance("analyze", duration)
    logger.request("POST", "/api/v1/analyze", 200, duration)

    return result


@router.post("/evaluate", summary="Run a full evaluation")
async def evaluate(
    request: Request,
    body: dict,
):
    logger = get_integration_logger()
    start = time.perf_counter()

    lang = body.get("language")
    count = min(body.get("count", 50), 1000)

    logger.info("EVALUATE language=%s count=%d", lang or "all", count)

    service = get_integration_service(request)
    result = service.run_evaluation(
        language=lang,
        count=count,
        stt_model_id=body.get("stt_model_id", ""),
        llm_model_id=body.get("llm_model_id", ""),
        tts_voice_id=body.get("tts_voice_id", ""),
        prompt_version=body.get("prompt_version", ""),
        flow_version=body.get("flow_version", ""),
        dataset_hash=body.get("dataset_hash", ""),
        provider_mode=body.get("provider_mode", "simulated"),
        audio_sample_rate=body.get("audio_sample_rate", 8000),
    )

    duration = (time.perf_counter() - start) * 1000
    logger.performance("evaluate", duration)
    logger.request("POST", "/api/v1/evaluate", 200, duration)
    logger.evaluation_result(result["run_id"], result["overall_passed"], lang or "all")

    return result


@router.get("/languages", summary="List supported languages")
async def list_languages(request: Request):
    logger = get_integration_logger()
    start = time.perf_counter()

    cache = get_cache()
    cached = cache.get("languages:list")
    if cached is not None:
        return cached

    service = get_integration_service(request)
    languages = service.list_languages()
    result = {"languages": languages, "total": len(languages)}

    cache.set("languages:list", result, ttl_seconds=300)

    duration = (time.perf_counter() - start) * 1000
    logger.performance("list_languages", duration)

    return result


@router.get("/health", summary="Integration service health")
async def integration_health(request: Request):
    return {
        "service": "stayza-milestone9-integration",
        "status": "healthy",
        "version": "1.0.0",
    }
