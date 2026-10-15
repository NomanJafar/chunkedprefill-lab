| config | interactive ITL p50 | p95 | p99 | p99/p50 | interactive TTFT p50 | long-prompt TTFT p50 | p95 | out tok/s (both) | errors |
|---|---|---|---|---|---|---|---|---|---|
| budget=512 | 44.5 ms | 80.7 ms | 100.9 ms | 2.27x | 141.5 ms | 186.4 ms | 220.5 ms | 464 | 0 |
| budget=1024 | 43.6 ms | 79.5 ms | 94.4 ms | 2.17x | 139.5 ms | 185.8 ms | 218.3 ms | 464 | 0 |
| budget=2048 | 43.9 ms | 79.5 ms | 103.1 ms | 2.35x | 143.2 ms | 184.7 ms | 229.3 ms | 464 | 0 |
| budget=4096 | 43.9 ms | 79.7 ms | 93.8 ms | 2.14x | 141.1 ms | 178.8 ms | 224 ms | 464 | 0 |
| budget=8192 | 43.8 ms | 79.5 ms | 91.4 ms | 2.09x | 140.8 ms | 186.9 ms | 217.8 ms | 464 | 0 |
| interactive only, budget=2048 | 41.1 ms | 45.2 ms | 47.1 ms | 1.15x | 113.9 ms | – | – | 454 | 0 |
| interactive only, budget=512 | 41.1 ms | 46 ms | 48 ms | 1.17x | 112.2 ms | – | – | 453 | 0 |
