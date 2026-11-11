"""Shared baseline measurement for the intake harnesses.

Each harness builds its workload first, then calls ``run_repeated`` so the
reported figure is only the function under test. Peak memory is the
tracemalloc high-water mark of one call (allocations made before the call,
including the input buffer, are not counted). Runtime is wall time for one
call. The spread is the full range of the repeated samples as a percentage of
their median: (max - min) / median * 100.
"""

from __future__ import annotations

import statistics
import time
import tracemalloc
from collections.abc import Callable
from typing import Any


def peak_bytes(fn: Callable[[], Any]) -> int:
    tracemalloc.start(1)
    tracemalloc.reset_peak()
    try:
        fn()
    finally:
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    return peak


def elapsed_ms(fn: Callable[[], Any]) -> float:
    start = time.perf_counter()
    fn()
    return (time.perf_counter() - start) * 1000.0


def run_repeated(
    measure: Callable[[], float], *, warmup: Callable[[], Any], repeats: int = 5
) -> None:
    warmup()
    samples = [measure() for _ in range(repeats)]
    median = statistics.median(samples)
    spread = (max(samples) - min(samples)) / median * 100.0 if median else 0.0
    print("samples=" + ",".join(repr(sample) for sample in samples))
    print(f"spread_pct={spread:.4f}")
    print(median)
