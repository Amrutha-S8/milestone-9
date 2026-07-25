# StayZa Native Voice Review System — API Documentation

## Overview

The StayZa Native Voice Review System enables native language reviewers to evaluate multilingual conversations across 6 Indian languages: English, Hindi, Hinglish, Telugu, Marathi, and Malayalam.

Reviewers can rate conversations on 6 categories, provide feedback, and drive the approval workflow (Pending → Approved / Rejected / Needs Improvement). The system generates analytics and JSON reports automatically.

---

## Folder Structure

```
review_system/
├── __init__.py           # Package exports
├── database.py           # SQLAlchemy engine & session setup
├── models.py             # Reviewer, Conversation, Review, Rating, Approval, ApprovalHistory
├── schemas.py            # Pydantic v2 request/response schemas
├── service.py            # Business logic layer (CRUD, approval workflow)
├── router.py             # FastAPI router with 12 endpoints
├── analytics.py          # Analytics engine (averages, breakdowns, rates)
├── auditor.py            # Auto-flagging of low-confidence utterances (Day 4)
└── auditor.py            # Auto-flagging of low-confidence utterances
```

---

## Complete API Reference

### 1. Create Reviewer

Registers a new native language reviewer.

**POST** `/reviews/reviewers`

**Input:**
```json
{
  "name": "Ravi Sharma",
  "languages": ["English", "Hindi"]
}
```

**Output (201):**
```json
{
  "id": 1,
  "name": "Ravi Sharma",
  "languages": ["English", "Hindi"],
  "created_at": "2026-01-15T10:30:00+00:00"
}
```

**Error Responses:**
- `422`: Validation error (name empty, invalid language format)

---

### 2. List Reviewers

Returns all registered reviewers.

**GET** `/reviews/reviewers`

**Output (200):**
```json
[
  {
    "id": 1,
    "name": "Ravi Sharma",
    "languages": ["English", "Hindi"],
    "created_at": "2026-01-15T10:30:00+00:00"
  }
]
```

---

### 3. Create Conversation

Stores a conversation for review with full audio pipeline metadata.

**POST** `/reviews/conversations`

**Input:**
```json
{
  "conversation_id": "conv_001",
  "reviewer_id": 1,
  "language": "English",
  "original_text": "I need a deluxe room for 2 adults",
  "normalized_text": "i need a deluxe room for 2 adults",
  "detected_language": "English",
  "detected_intent": "booking",
  "entities": {"room_type": "deluxe", "guests": 2},
  "expected_intent": "booking",
  "evaluation_score": 95.0,
  "latency_ms": 120.0
}
```

**Output (201):**
```json
{
  "id": 1,
  "conversation_id": "conv_001",
  "reviewer_id": 1,
  "language": "English",
  "original_text": "I need a deluxe room for 2 adults",
  "normalized_text": "i need a deluxe room for 2 adults",
  "detected_language": "English",
  "detected_intent": "booking",
  "entities": {"room_type": "deluxe", "guests": 2},
  "expected_intent": "booking",
  "evaluation_score": 95.0,
  "latency_ms": 120.0,
  "timestamp": "2026-01-15T10:30:00+00:00"
}
```

**Error Responses:**
- `422`: Validation error

---

### 4. Create Review

Creates a review for a conversation with ratings and approval status.

**POST** `/reviews/create`

**Input:**
```json
{
  "conversation_id": 1,
  "reviewer_id": 1,
  "feedback": "Good pronunciation, but intent was off.",
  "ratings": {
    "pronunciation": 8.5,
    "language_accuracy": 9.0,
    "intent_accuracy": 8.0,
    "naturalness": 7.5,
    "conversation_quality": 8.5,
    "overall_rating": 8.3
  },
  "approval": {
    "status": "Pending",
    "reviewer_notes": "Awaiting final check."
  }
}
```

**Output (201):**
```json
{
  "id": 1,
  "conversation_id": 1,
  "reviewer_id": 1,
  "feedback": "Good pronunciation, but intent was off.",
  "reviewer_feedback": null,
  "created_at": "2026-01-15T10:30:00+00:00",
  "updated_at": "2026-01-15T10:30:00+00:00",
  "conversation": { ... },
  "reviewer": { ... },
  "ratings": {
    "id": 1,
    "review_id": 1,
    "pronunciation": 8.5,
    "language_accuracy": 9.0,
    "intent_accuracy": 8.0,
    "naturalness": 7.5,
    "conversation_quality": 8.5,
    "overall_rating": 8.3
  },
  "approval": {
    "id": 1,
    "review_id": 1,
    "status": "Pending",
    "reviewer_notes": "Awaiting final check.",
    "approved_by": null,
    "created_at": "2026-01-15T10:30:00+00:00",
    "updated_at": "2026-01-15T10:30:00+00:00"
  }
}
```

**Error Responses:**
- `404`: Conversation not found
- `422`: Validation error (rating bounds, invalid status)

---

### 5. List Reviews (Paginated)

Returns paginated reviews ordered by creation date (newest first).

**GET** `/reviews?page=1&page_size=20`

**Output (200):**
```json
{
  "total": 42,
  "page": 1,
  "page_size": 20,
  "reviews": [ ... ]
}
```

**Error Responses:**
- `422`: Invalid page or page_size

---

### 6. Get Review by ID

Returns a single review with full details.

**GET** `/reviews/{review_id}`

**Output (200):** Single review object with conversation, reviewer, ratings, and approval.

**Error Responses:**
- `404`: Review not found

---

### 7. Update Review

Updates feedback, ratings, and/or approval status.

**PUT** `/reviews/{review_id}`

**Input (partial update supported):**
```json
{
  "feedback": "Updated feedback text.",
  "ratings": {
    "pronunciation": 9.0,
    "language_accuracy": 9.5,
    "intent_accuracy": 8.5,
    "naturalness": 8.0,
    "conversation_quality": 9.0,
    "overall_rating": 8.8
  },
  "approval": {
    "status": "Approved",
    "reviewer_notes": "All good after re-evaluation.",
    "approved_by": "Senior Reviewer"
  }
}
```

**Output (200):** Updated review object.

**Error Responses:**
- `404`: Review not found
- `422`: Validation error

---

### 8. Delete Review

Deletes a review and all associated ratings, approvals, and approval history.

**DELETE** `/reviews/{review_id}`

**Output:** `204 No Content`

**Error Responses:**
- `404`: Review not found

---

### 9. Get Reviews by Language

Returns all reviews for conversations in a specific language.

**GET** `/reviews/language/{language}`

**Output (200):**
```json
[
  { ... review with full details ... }
]
```

---

### 10. Get Review Analytics

Returns comprehensive analytics.

**GET** `/reviews/analytics`

**Output (200):**
```json
{
  "average_rating": 8.5,
  "total_reviews": 42,
  "language_breakdown": {
    "English": {
      "review_count": 15,
      "average_rating": 8.7,
      "average_pronunciation": 8.5,
      "average_language_accuracy": 9.0,
      "average_intent_accuracy": 8.2,
      "average_naturalness": 7.8,
      "average_conversation_quality": 8.6
    },
    "Hindi": { ... }
  },
  "reviewer_statistics": {
    "total_reviewers": 5,
    "per_reviewer": [
      {
        "id": 1,
        "name": "Ravi Sharma",
        "review_count": 12,
        "average_rating": 8.5
      }
    ]
  },
  "approval_rate": 65.0,
  "rejection_rate": 15.0,
  "needs_improvement_rate": 10.0,
  "pending_rate": 10.0,
  "rating_distribution": {
    "0-2": 0.0,
    "2-4": 2.5,
    "4-6": 10.0,
    "6-8": 35.0,
    "8-10": 52.5
  }
}
```

---

### 11. Generate Review Report

Generates and stores a JSON review report with full analytics and recent reviews.

**GET** `/reviews/reports/generate`

**Output (200):**
```json
{
  "report_id": "report_20260115_103000",
  "generated_at": "2026-01-15T10:30:00+00:00",
  "total_reviews": 42,
  "analytics": { ... },
  "recent_reviews": [ ... ]
}
```

Reports are stored in `review_data/reports/report_*.json`.

---

## Rating Categories

| Category | Range | Description |
|----------|-------|-------------|
| Pronunciation | 0.0 – 10.0 | Clarity and accuracy of pronunciation |
| Language Accuracy | 0.0 – 10.0 | Correctness of language usage |
| Intent Accuracy | 0.0 – 10.0 | How well the detected intent matches expected intent |
| Naturalness | 0.0 – 10.0 | How natural the conversation sounds |
| Conversation Quality | 0.0 – 10.0 | Overall quality of conversation flow |
| Overall Rating | 0.0 – 10.0 | Weighted overall impression |

---

## Approval Workflow

Statuses (4 states):
1. **Pending** — Initial state, awaiting review
2. **Approved** — Review passed
3. **Rejected** — Review failed
4. **Needs Improvement** — Review requires changes

Each status change is tracked in `ApprovalHistory` with timestamp, previous status, new status, and reviewer notes.

---

## Data Model

```
Reviewer (1) ──── (N) Conversation
Reviewer (1) ──── (N) Review
Conversation (1) ──── (N) Review
Review (1) ──── (1) Rating
Review (1) ──── (1) Approval
Approval (1) ──── (N) ApprovalHistory
```

---

## Error Response Format

```json
{
  "detail": "Review with id 999 not found."
}
```

HTTP status codes:
- `201`: Resource created
- `200`: Success
- `204`: Deleted (no content)
- `404`: Resource not found
- `422`: Validation error (invalid input)