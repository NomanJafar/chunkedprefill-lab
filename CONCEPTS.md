# Concepts: chunked prefill, or how to stop long prompts from stalling everyone else

`chunkedprefill-lab` measures what happens to interactive users' token stream when long-prompt requests arrive, and how vLLM's chunked prefill and its `max-num-batched-tokens` budget change that. The earlier projects saw the symptom (kvcalc: ITL p99 at 145 ms against a p50 of 73 ms with 1,024-token prompts); this one isolates the cause and the control.

## 1. Prefill and decode want opposite things from the GPU

A decode step is small and memory-bound: one token per sequence, the whole weight set streamed once, 15–40 ms on a T4 for the models here. A prefill is large and compute-bound: a 4,000-token prompt through a 3B model is ~24 TFLOP of matrix multiplies, 300+ ms on a T4 even at good utilisation.

A continuous-batching scheduler runs *one* forward pass per iteration for everything it has admitted. If a new request's full prefill is put into the same iteration as 32 decoding sequences, that iteration takes as long as the prefill, and every one of the 32 users waits 300+ ms for their next token instead of 30. From the user's side the stream freezes, then resumes. In latency percentiles it appears as a fat ITL tail: the p50 is fine, the p99 is ten times larger. That tail *is* prefill interference.

The original vLLM scheduler (V0 default) handled this by prioritising prefills: new requests were prefilled in their own iterations, decode paused. Good for TTFT, bad for ITL. Alternatives that prioritise decode starve new requests: good ITL, terrible TTFT under load. Either way one side pays.

## 2. Chunked prefill

Chunked prefill (Sarathi, Agrawal et al. 2023; vLLM's `enable_chunked_prefill`, on by default in V1) splits a long prefill into chunks and schedules **one chunk per iteration alongside the decode batch**. Each iteration now contains all the decode tokens plus up to `max-num-batched-tokens` − (decode tokens) of prefill work. The iteration gets somewhat longer than a pure decode step but never as long as a full prefill, and the long prompt finishes a few iterations later than it would have alone.

The effect is a dial, and the dial is **`max-num-batched-tokens`** (the token budget per iteration):

- **Small budget (e.g. 512):** each iteration carries little prefill; decode ITL stays close to its unloaded value; a 4k prompt needs ~8 iterations of prefill, so its TTFT grows by 8 × (iteration time). Interactive users protected, long prompts slowed.
- **Large budget (e.g. 8192):** a 4k prompt prefills in one iteration; that iteration is long; decode users see the stall. TTFT for long prompts minimal, ITL tail fat.
- The V1 default (2048 on most GPUs, lower when memory is tight) is a compromise.

There is also a second, subtler benefit: a chunk of prefill and a batch of decode in the same forward pass make better use of the GPU than either alone (the decode part is memory-bound, the prefill part compute-bound; together they overlap). This is why chunked prefill often raises total throughput, not just smooths latency.

## 3. What the budget cannot fix

- **The work is conserved.** Prefill FLOPs do not disappear; chunking spreads them over iterations. If long prompts arrive faster than the GPU can prefill them at *any* chunk size, the queue grows and TTFT explodes regardless of the setting (tokenbench's saturation point).
- **Very small chunks waste efficiency.** Attention over a chunk must still read the KV of all previous chunks; with tiny chunks the prefill does more total memory traffic. Below a few hundred tokens the overhead is visible.
- **`max-num-seqs` is a separate cap** (on sequences per iteration); both limits apply.

## 4. Measuring it honestly

The experiment needs two populations at once, because interference is a property of the mix:

- **Interactive stream:** short prompts (~64 tokens), medium outputs (~128 tokens), arriving steadily (open loop, tokenbench) so that their ITL distribution is the measurement.
- **Long-prompt stream:** 3,000–4,000-token prompts, short outputs, arriving at a lower steady rate, so that their TTFT is the other measurement.

Then sweep `max-num-batched-tokens` over 512, 1024, 2048, 4096, 8192 with chunked prefill on, plus one run with chunked prefill off, and plot:

1. interactive **ITL p50 / p95 / p99** vs budget (the interference tail should shrink as the budget shrinks);
2. long-prompt **TTFT p50** vs budget (should grow as the budget shrinks);
3. total **output tokens/s** vs budget (the overlap benefit, if any).

The honest result is a trade-off curve, not a winner. The write-up names the budget at which interactive p99 is within, say, 2× its p50 while long-prompt TTFT is still under a second, for this hardware and this mix.

## 5. Where this sits in the stack

This is the scheduling layer of the KV cache picture: kvcalc sized the cache, PagedAttention (project 9) manages its blocks under pressure, chunked prefill decides how much new work to admit per iteration. Prefix caching (project 4) reduces prefill work altogether when prompts share a prefix. Disaggregated serving (project 10) removes the interference by giving prefill its own GPUs, at the cost of moving KV between machines; the numbers here are the baseline that architecture must beat.

## 6. What the experiment will show

1. Baseline interference: interactive ITL percentiles with and without a concurrent long-prompt stream, default settings.
2. The budget sweep with chunked prefill on: three curves as in section 4.
3. Chunked prefill off at the default budget for comparison.
4. The `/metrics` timelines (`num_requests_running`, `num_requests_waiting`) for one small-budget and one large-budget run, so the queueing side is visible too.

## Further reading

- Agrawal et al., *SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills* (2023), and *Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve* (OSDI 2024).
- vLLM docs: *Optimization and Tuning* (chunked prefill, `max_num_batched_tokens`, `max_num_seqs`).
- Zhong et al., *DistServe* (OSDI 2024): the case for separating the two phases entirely.
