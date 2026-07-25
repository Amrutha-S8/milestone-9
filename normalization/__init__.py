"""
Text Normalization Package for StayZa Milestone 9.

Exposes the TextNormalizationService as the public interface.
"""

from normalization.service import TextNormalizationService, normalization_service

__all__ = ["TextNormalizationService", "normalization_service"]
