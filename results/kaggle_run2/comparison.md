| config | interactive ITL p50 | p95 | p99 | p99/p50 | interactive TTFT p50 | long-prompt TTFT p50 | p95 | out tok/s (both) | errors |
|---|---|---|---|---|---|---|---|---|---|
| budget=512 | 184.4 ms | 621.2 ms | 711.1 ms | 3.86x | 19766.1 ms | 15914.4 ms | 26542 ms | 325 | 0 |
| budget=1024 | 121.1 ms | 1149.4 ms | 1321.7 ms | 10.91x | 16905 ms | 15001.2 ms | 23754 ms | 330 | 0 |
| budget=2048 | 121.9 ms | 1752.8 ms | 2330.7 ms | 19.11x | 15468.9 ms | 14510.7 ms | 22069.5 ms | 330 | 0 |
| budget=4096 | 121.5 ms | 2031.8 ms | 3924.1 ms | 32.31x | 20281.5 ms | 19187.2 ms | 27384.7 ms | 310 | 0 |
| budget=8192 | 121.9 ms | 203.2 ms | 7311 ms | 59.99x | 18652.3 ms | 17558.9 ms | 27622.6 ms | 319 | 0 |
| budget=4096, chunked off | 121.7 ms | 1466.6 ms | 3986.4 ms | 32.76x | 19068.4 ms | 16611.1 ms | 26213.4 ms | 310 | 0 |
| interactive only, budget=2048 | 44.1 ms | 60.2 ms | 90.5 ms | 2.05x | 134.4 ms | – | – | 452 | 0 |
| interactive only, budget=512 | 44.1 ms | 60.6 ms | 91.9 ms | 2.08x | 132.4 ms | – | – | 452 | 0 |
