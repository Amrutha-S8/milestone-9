# StayZa Milestone 9: API Specification

## Endpoints Summary

| Method | Path | Summary | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/language/analyze` | Analyze Utterance | Classifies text for language, intent, confidence, and next action |
| `GET` | `/language/supported` | List Languages | Returns active supported language flow handlers |
| `GET` | `/language/evaluate` | Run Evaluation | Benchmarks accuracy over dataset |
| `GET` | `/language/review/flagged` | Review Audit Queue | Retrieves low-confidence or unknown intent utterances |
| `GET` | `/health` | Health Check | System health check |

---

## Endpoint Details

### 1. `POST /language/analyze`

**Request Body (`application/json`):**
```json
{
  "text": "I want to book a room",
  "session_id": "sess_10293",
  "current_state": "idle"
}
```

**Response Body (`200 OK`):**
```json
{
  "language": "English",
  "intent": "booking",
  "confidence": 0.95,
  "next_action": "ask_checkin_date",
  "session_id": "sess_10293",
  "slots": {
    "room_type": "standard"
  }
}
```

**Error Response (`400 Bad Request`):**
```json
{
  "detail": "Text field cannot be empty."
}
```
