Run 1 (2026-10-15): completed, but a null result for the wrong reason. The long-prompt stream used one fixed 3,500-token
prompt, and vLLM 0.31's default prefix caching served every prefill after the first from cache (long-prompt TTFT ~185 ms,
impossible for a real 3,500-token prefill on a T4), so `max-num-batched-tokens` had nothing to chunk: all five budgets
measured identically (interactive ITL p50/p95/p99 44/80/95 ms; long TTFT p50 ~185 ms; 464 tok/s). Two findings do stand:
the long stream still raised interactive ITL p95 from 45 to 80 ms (long-context decode attention, not prefill), and vLLM
V1 refuses `--no-enable-chunked-prefill` when the budget is below `max-model-len`. Run 2 uses tokenbench's `unique`
prompts (no shared prefix) and a valid chunked-off configuration (budget 4096 = max-model-len).
