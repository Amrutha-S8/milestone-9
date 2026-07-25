"""
Load Testing Suite for StayZa Milestone 9 using Locust.
Tests: 10, 50, 100, 250, 500 concurrent users.
Measures: latency, error rate, success rate, throughput.
"""

import json
import random
from locust import HttpUser, task, between, events
from datetime import datetime

TEST_TEXTS = [
    ("English", "I want to book a deluxe room for two guests tomorrow morning"),
    ("Hindi", "mujhe ek deluxe kamra do guest ke liye kal subah book karna hai"),
    ("Hinglish", "mujhe ek deluxe room do guests ke liye kal subah book karna hai"),
    ("Telugu", "naaku oka deluxe room rendu athithulaku repu podduna kavali"),
    ("Marathi", "mala ek deluxe room dona pahunakarita udya sakali book karaycha ahe"),
    ("Malayalam", "enikku oru deluxe room randu athithikalkku naale ravile venam"),
]

INTENTS = ["greeting", "booking", "availability", "price_enquiry", "cancellation", "modify_booking", "check_status", "goodbye"]

REVIEWER_NAMES = ["Ravi Sharma", "Priya Patel", "Aisha Khan", "Venkatesh Rao", "Lakshmi Nair"]


class StayZaLoadTest(HttpUser):
    wait_time = between(0.5, 2.0)

    def on_start(self):
        self.reviewer_id = None

    @task(3)
    def detect_language(self):
        lang, text = random.choice(TEST_TEXTS)
        with self.client.post("/language/detect", json={"text": text}, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Language detection failed: {resp.status_code}")

    @task(3)
    def analyze_utterance(self):
        lang, text = random.choice(TEST_TEXTS)
        with self.client.post("/language/analyze", json={"text": text}, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Analyze failed: {resp.status_code}")

    @task(1)
    def health_check(self):
        with self.client.get("/health", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Health check failed: {resp.status_code}")

    @task(1)
    def monitoring_health(self):
        with self.client.get("/monitoring/health", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Monitoring health failed: {resp.status_code}")

    @task(1)
    def list_supported_languages(self):
        with self.client.get("/language/supported", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Supported languages failed: {resp.status_code}")

    @task(1)
    def run_evaluation(self):
        with self.client.post("/language/evaluation/run", json={}, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Evaluation failed: {resp.status_code}")

    @task(1)
    def review_analytics(self):
        with self.client.get("/reviews/analytics", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Review analytics failed: {resp.status_code}")

    @task(1)
    def create_reviewer(self):
        name = random.choice(REVIEWER_NAMES) + str(random.randint(1, 10000))
        lang = random.choice(["English", "Hindi", "Telugu"])
        with self.client.post("/reviews/reviewers", json={"name": name, "languages": [lang]}, catch_response=True) as resp:
            if resp.status_code == 201:
                self.reviewer_id = resp.json()["id"]
                resp.success()
            else:
                resp.failure(f"Create reviewer failed: {resp.status_code}")

    @task(1)
    def list_reviews(self):
        with self.client.get("/reviews", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"List reviews failed: {resp.status_code}")

    @task(1)
    def metrics_endpoint(self):
        with self.client.get("/monitoring/metrics", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Metrics endpoint failed: {resp.status_code}")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(f"\n{'='*60}")
    print(f"StayZa Load Test Starting at {datetime.now().isoformat()}")
    print(f"Host: {environment.host}")
    print(f"User count: {environment.runner.target_user_count}")
    print(f"{'='*60}\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.runner.stats
    print(f"\n{'='*60}")
    print(f"StayZa Load Test Complete at {datetime.now().isoformat()}")
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Failures: {stats.total.num_failures}")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"P95 response time: {stats.total.get_response_time_percentile(0.95):.2f}ms")
    print(f"P99 response time: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    print(f"RPS: {stats.total.current_rps:.2f}")
    print(f"{'='*60}\n")
