
from threading import Lock

_lock = Lock()

_usage = {
    "total_requests": 0,
    "requests_with_token_data": 0,
    "prompt_tokens": 0,
    "response_tokens": 0,
    "total_tokens": 0,
    "estimated_cost_usd": 0.0,
    "cost_available": False,
}


def record_usage(
    usage_metadata,
    prompt_cost_per_million: float | None = None,
    response_cost_per_million: float | None = None,
) -> None:
    prompt_tokens = int(
        getattr(usage_metadata, "prompt_token_count", 0) or 0
    )
    response_tokens = int(
        getattr(usage_metadata, "candidates_token_count", 0) or 0
    )
    total_tokens = int(
        getattr(usage_metadata, "total_token_count", 0) or 0
    )

    cost_available = (
        prompt_cost_per_million is not None
        and response_cost_per_million is not None
    )

    estimated_cost = 0.0

    if cost_available:
        estimated_cost = (
            prompt_tokens * prompt_cost_per_million
            + response_tokens * response_cost_per_million
        ) / 1_000_000

    with _lock:
        _usage["total_requests"] += 1

        if usage_metadata is not None:
            _usage["requests_with_token_data"] += 1

        _usage["prompt_tokens"] += prompt_tokens
        _usage["response_tokens"] += response_tokens
        _usage["total_tokens"] += total_tokens

        if cost_available:
            _usage["estimated_cost_usd"] += estimated_cost
            _usage["cost_available"] = True


def get_usage_summary() -> dict:
    with _lock:
        return {
            **_usage,
            "estimated_cost_usd": (
                round(_usage["estimated_cost_usd"], 8)
                if _usage["cost_available"]
                else None
            ),
        }
