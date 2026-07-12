from __future__ import annotations

REVIEWER_ROLES = frozenset(
    {"Media Buyer", "Creative Ops Manager", "Approver", "Account Manager"}
)

DECISIONS_BY_STATUS = {
    "confirmed_ready": frozenset(
        {"approved_for_dry_run_export", "bulk_approved_for_dry_run_export"}
    ),
    "needs_fix": frozenset({"requires_fix", "bulk_requires_fix"}),
    "blocked": frozenset({"blocked_from_export", "bulk_blocked_from_export"}),
}


class ReviewPolicyError(ValueError):
    """Raised when a review-state transition violates the shared domain policy."""


def validate_review_transition(
    *,
    batch_state: str,
    review_status: str,
    decision: str,
    actor_role: str,
    note: str,
) -> None:
    if actor_role not in REVIEWER_ROLES:
        raise ReviewPolicyError(f"unknown reviewer role: {actor_role}")
    allowed_decisions = DECISIONS_BY_STATUS.get(review_status)
    if allowed_decisions is None:
        raise ReviewPolicyError(f"review status is not actionable: {review_status}")
    if decision not in allowed_decisions:
        raise ReviewPolicyError(
            f"decision {decision!r} is not valid for status {review_status!r}"
        )
    if review_status == "confirmed_ready" and batch_state == "blocked":
        raise ReviewPolicyError(
            "blocked rows cannot be approved before deterministic blockers are resolved"
        )
    if len(note) > 2_000:
        raise ReviewPolicyError("review note exceeds 2000 characters")
