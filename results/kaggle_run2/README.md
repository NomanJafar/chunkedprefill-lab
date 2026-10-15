Run 2 (2026-10-15): unique prompts, so prefill is paid every time. Load: interactive 4 req/s (64-token prompts, 128 out) +
long 0.4 req/s (3,500-token prompts, 32 out), 60 s per configuration. The T4 saturated under this mix (both streams
queued 15–20 s, up to 99 waiting, 310–330 tok/s vs 452 interactive-only), so long-prompt TTFT is dominated by queueing and
cannot show the chunk-size cost. The interference side is clear: interactive ITL p99 0.7 s (budget 512) → 1.3 s (1024) →
2.3 s (2048) → 3.9 s (4096) → 7.3 s (8192); chunked-off at 4096 ≈ budget 4096. Run 3 repeats at a quarter of the load.
