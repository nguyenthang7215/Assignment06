from __future__ import annotations

from domain.models import Candidate, RankedResult


class RankingService:
    """Ranks retrieved candidates using relevance and small business signals."""

    def rank(
        self,
        candidates: list[Candidate],
        text_weight: float,
        image_weight: float,
        top_k: int = 5,
    ) -> list[RankedResult]:
        # Relevance has the dominant weight; business signals can still reorder
        # candidates whose relevance scores are sufficiently close.
        business_weight = 0.02
        relevance_scale = max(text_weight + image_weight, 1e-9)
        ranked: list[RankedResult] = []
        for candidate in candidates:
            stock_score = min(candidate.product.stock / 20.0, 1.0)
            business_score = 0.7 * candidate.product.popularity + 0.3 * stock_score
            relevance = (
                text_weight * candidate.text_score
                + image_weight * candidate.image_score
            ) / relevance_scale
            score = (1.0 - business_weight) * relevance + business_weight * business_score
            reasons = []
            if candidate.text_score:
                reasons.append(f"text={candidate.text_score:.3f}")
            if candidate.image_score:
                reasons.append(f"image={candidate.image_score:.3f}")
            reasons.append(f"business={business_score:.3f}")
            ranked.append(
                RankedResult(
                    product=candidate.product,
                    score=score,
                    text_score=candidate.text_score,
                    image_score=candidate.image_score,
                    business_score=business_score,
                    reason=", ".join(reasons),
                )
            )
        ranked.sort(key=lambda result: (-result.score, result.product.id))
        return ranked[:top_k]

