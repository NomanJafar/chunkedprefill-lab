# chunkedprefill-lab

Chunked prefill scheduling experiments: how long-context prefill starves decode, and how chunk size trades TTFT against ITL under mixed load.

Project 8 of 15 in [inference-infra-portfolio](https://github.com/NomanJafar/inference-infra-portfolio).

## What this builds

Configure chunked prefill and measure TTFT and ITL under mixed prefill/decode load as chunk size changes.

## Why it matters

Long-context requests starve decode without scheduling control.

## Status

Scaffolded. Concept notes and the first implementation are in progress; results land in `results/` once the GPU runs are done.

## Layout

```
CONCEPTS.md     the theory behind the project, written before the code
src/chunkedprefill_lab/   implementation
tests/          CPU-only tests, runnable on a laptop
notebooks/      GPU notebooks (Kaggle / Colab) that run the experiments and write results/
results/        measured numbers and plots
```

## Running

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

GPU experiments run from `notebooks/`; each notebook clones this repo, installs it and writes its outputs to `results/`.

## Hardware notes

Developed against free-tier GPUs (Kaggle and Colab T4, 16 GB). Where a T4 limits what can be measured (no FP8, Turing-era kernels), the README says so rather than papering over it.

## License

MIT
