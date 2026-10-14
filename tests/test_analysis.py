import json

import pytest

from chunkedprefill_lab.analysis import build_rows, interference_ratio, render_markdown, server_args


def test_server_args_sets_budget_and_chunked_prefill_flag():
    assert server_args(2048, chunked=True) == ["--max-num-batched-tokens", "2048", "--enable-chunked-prefill"]
    assert server_args(2048, chunked=False) == ["--max-num-batched-tokens", "2048", "--no-enable-chunked-prefill"]


def test_interference_ratio_is_p99_over_p50():
    assert interference_ratio({"itl": {"p50": 0.02, "p99": 0.1}}) == pytest.approx(5.0)
    assert interference_ratio({"itl": {"p50": None, "p99": 0.1}}) is None


def _level(ttft, itl50, itl95, itl99, tps, n=100):
    return {"requests": n, "errors": 0, "output_tokens_per_s": tps,
            "ttft": {"p50": ttft, "p95": ttft * 1.5, "p99": ttft * 2, "n": n},
            "itl": {"p50": itl50, "p95": itl95, "p99": itl99, "n": n * 100}}


def test_build_rows_pairs_interactive_and_long_streams_per_config():
    runs = [
        {"config": "budget=512", "budget": 512, "chunked": True,
         "interactive": _level(0.05, 0.02, 0.03, 0.04, 300), "long": _level(1.2, 0.03, 0.05, 0.06, 40)},
        {"config": "budget=8192", "budget": 8192, "chunked": True,
         "interactive": _level(0.06, 0.02, 0.09, 0.3, 320), "long": _level(0.4, 0.03, 0.05, 0.06, 45)},
    ]
    rows = build_rows(runs)
    assert [r["config"] for r in rows] == ["budget=512", "budget=8192"]
    r = rows[1]
    assert r["interactive_itl_p50_ms"] == 20 and r["interactive_itl_p99_ms"] == 300
    assert r["interference_ratio"] == pytest.approx(15.0)
    assert r["long_ttft_p50_ms"] == 400 and r["total_tokens_per_s"] == 365


def test_build_rows_tolerates_a_failed_stream():
    runs = [{"config": "off", "budget": 2048, "chunked": False, "interactive": _level(0.05, 0.02, 0.03, 0.04, 300), "long": None}]
    r = build_rows(runs)[0]
    assert r["long_ttft_p50_ms"] is None and r["total_tokens_per_s"] == 300


def test_render_markdown_has_one_row_per_config():
    runs = [{"config": "a", "budget": 512, "chunked": True, "interactive": _level(0.05, 0.02, 0.03, 0.04, 300), "long": _level(1.0, 0.03, 0.05, 0.06, 40)}]
    md = render_markdown(build_rows(runs))
    assert md.count("\n| ") == 1 and "p99" in md and "TTFT" in md
