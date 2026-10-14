"""Rows and tables for the chunked-prefill budget sweep (CONCEPTS.md section 4).

Each run has two tokenbench levels measured at the same time: an interactive
stream (short prompts; its ITL tail is the interference signal) and a long-prompt
stream (its TTFT is the price of protecting the interactive users)."""

from __future__ import annotations


def server_args(max_num_batched_tokens: int, chunked: bool) -> list[str]:
    return ["--max-num-batched-tokens", str(max_num_batched_tokens),
            "--enable-chunked-prefill" if chunked else "--no-enable-chunked-prefill"]


def interference_ratio(level: dict) -> float | None:
    p50, p99 = level["itl"].get("p50"), level["itl"].get("p99")
    return p99 / p50 if p50 and p99 else None


def _ms(x):
    return None if x is None else round(x * 1000, 1)


def build_rows(runs: list[dict]) -> list[dict]:
    rows = []
    for r in runs:
        it, lg = r.get("interactive"), r.get("long")
        rows.append({
            "config": r["config"], "budget": r.get("budget"), "chunked": r.get("chunked"),
            "interactive_requests": it["requests"] if it else None,
            "interactive_itl_p50_ms": _ms(it["itl"]["p50"]) if it else None,
            "interactive_itl_p95_ms": _ms(it["itl"]["p95"]) if it else None,
            "interactive_itl_p99_ms": _ms(it["itl"]["p99"]) if it else None,
            "interactive_ttft_p50_ms": _ms(it["ttft"]["p50"]) if it else None,
            "interference_ratio": round(interference_ratio(it), 2) if it and interference_ratio(it) else None,
            "long_requests": lg["requests"] if lg else None,
            "long_ttft_p50_ms": _ms(lg["ttft"]["p50"]) if lg else None,
            "long_ttft_p95_ms": _ms(lg["ttft"]["p95"]) if lg else None,
            "total_tokens_per_s": round((it["output_tokens_per_s"] if it else 0) + (lg["output_tokens_per_s"] if lg else 0)),
            "errors": (it["errors"] if it else 0) + (lg["errors"] if lg else 0),
        })
    return rows


def _f(x, suffix=""):
    return "–" if x is None else f"{x:g}{suffix}"


def render_markdown(rows: list[dict]) -> str:
    head = ["config", "interactive ITL p50", "p95", "p99", "p99/p50", "interactive TTFT p50", "long-prompt TTFT p50", "p95", "out tok/s (both)", "errors"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        lines.append("| " + " | ".join([
            r["config"], _f(r["interactive_itl_p50_ms"], " ms"), _f(r["interactive_itl_p95_ms"], " ms"), _f(r["interactive_itl_p99_ms"], " ms"),
            _f(r["interference_ratio"], "x"), _f(r["interactive_ttft_p50_ms"], " ms"), _f(r["long_ttft_p50_ms"], " ms"), _f(r["long_ttft_p95_ms"], " ms"),
            _f(r["total_tokens_per_s"]), str(r["errors"]),
        ]) + " |")
    return "\n".join(lines) + "\n"
