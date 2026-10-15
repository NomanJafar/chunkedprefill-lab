| config | interactive ITL p50 | p95 | p99 | p99/p50 | interactive TTFT p50 | long-prompt TTFT p50 | p95 | out tok/s (both) | errors |
|---|---|---|---|---|---|---|---|---|---|
| budget=512 | 35.9 ms | 102.5 ms | 632.9 ms | 17.64x | 124 ms | 3564.3 ms | 4246.4 ms | 202 | 0 |
| budget=1024 | 35 ms | 68.9 ms | 878.6 ms | 25.09x | 120.2 ms | 3550.2 ms | 4018.6 ms | 202 | 0 |
| budget=2048 | 35.2 ms | 56.7 ms | 1462.4 ms | 41.57x | 123 ms | 3515.4 ms | 4040.1 ms | 201 | 0 |
| budget=4096 | 35.3 ms | 55.6 ms | 151.7 ms | 4.3x | 120.2 ms | 3480.1 ms | 4231.9 ms | 201 | 0 |
| budget=8192 | 35.1 ms | 55.1 ms | 150.8 ms | 4.29x | 123.2 ms | 3474.5 ms | 4077.4 ms | 201 | 0 |
| budget=4096, chunked off | 35.1 ms | 55.2 ms | 152.4 ms | 4.34x | 121 ms | 3457.3 ms | 4091.6 ms | 201 | 0 |
| interactive only, budget=2048 | 33.5 ms | 52.1 ms | 62.5 ms | 1.86x | 111.5 ms | – | – | 199 | 0 |
| interactive only, budget=512 | 33.6 ms | 52.6 ms | 61.3 ms | 1.83x | 112.5 ms | – | – | 199 | 0 |
