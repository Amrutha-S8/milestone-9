"""
Word Error Rate (WER) Metrics Evaluator.
WER = (Substitutions + Deletions + Insertions) / Total_Reference_Words
"""

from typing import Dict, Any, List


class WEREvaluator:

    @staticmethod
    def calculate(reference: str, hypothesis: str) -> Dict[str, Any]:
        ref_words = reference.lower().strip().split()
        hyp_words = hypothesis.lower().strip().split()

        n = len(ref_words)
        m = len(hyp_words)

        if n == 0:
            return {
                "wer": 0.0 if m == 0 else 1.0,
                "substitutions": 0,
                "deletions": 0,
                "insertions": m,
                "reference_words": 0
            }

        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if ref_words[i - 1] == hyp_words[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    sub = dp[i - 1][j - 1] + 1
                    delete = dp[i - 1][j] + 1
                    insert = dp[i][j - 1] + 1
                    dp[i][j] = min(sub, delete, insert)

        edit_distance = dp[n][m]
        wer_score = round(edit_distance / n, 4)

        return {
            "wer": wer_score,
            "edit_distance": edit_distance,
            "reference_word_count": n,
            "hypothesis_word_count": m
        }

    @staticmethod
    def evaluate_all(reference_map: Dict[str, str], hypothesis_map: Dict[str, str]) -> Dict[str, Any]:
        results = {}
        languages = sorted(set(list(reference_map.keys()) + list(hypothesis_map.keys())))
        for lang in languages:
            ref = reference_map.get(lang, "")
            hyp = hypothesis_map.get(lang, "")
            results[lang] = WEREvaluator.calculate(ref, hyp)
        return {
            "per_language": results
        }