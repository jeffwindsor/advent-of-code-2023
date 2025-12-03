"""Testing utilities for Advent of Code puzzles."""

import os
import inspect
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Any


# ========== Configuration ==========


def _is_perf_enabled() -> bool:
    """Check if performance metrics should be collected via AOC_PERF env var."""
    value = os.getenv('AOC_PERF', '').lower()
    return value in ('1', 'true', 'yes')


# Cache at module load time for zero per-test overhead
PERF_ENABLED = _is_perf_enabled()


# ========== Colors ==========

TITLE_COLOR = "\033[34m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


# ========== Formatting ==========


def format_time(seconds: float) -> str:
    """Format time duration for display."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.0f}µs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def format_memory(bytes_used: int) -> str:
    """Format memory usage for display."""
    if bytes_used < 1024:
        return f"{bytes_used}B"
    elif bytes_used < 1024 * 1024:
        return f"{bytes_used / 1024:.1f}KB"
    else:
        return f"{bytes_used / (1024 * 1024):.1f}MB"


# ========== Test Framework ==========


@dataclass
class TestCase:
    """A single test case with function arguments and expected output.

    Args can be:
    - A single string (file path): TestCase("data/01_example_01", expected=42)
    - A list of arguments: TestCase(["data/01_example_01", 10], expected=42)
    """

    args: str | list[Any]
    expected: Any = None


def run(func: Callable[..., Any], test_cases: list[TestCase]) -> None:
    """
    Execute test cases for a given function and report results with performance metrics.

    Args:
        func: Function to test (takes variadic arguments, returns any value)
        test_cases: List of TestCase objects

    The function prints colored output:
    - Green for passing tests showing the actual result with time and memory
    - Red for failing tests showing expected vs actual
    - Summary line showing total pass/fail count
    """
    filename = os.path.basename(inspect.stack()[1].filename)
    print(f"{TITLE_COLOR}{func.__name__}{END_COLOR}")

    passed = 0
    failed = 0

    for test_case in test_cases:
        try:
            # Start performance tracking (if enabled)
            if PERF_ENABLED:
                tracemalloc.start()
                start_time = time.perf_counter()

            # Execute test
            args = [test_case.args] if isinstance(test_case.args, str) else test_case.args
            actual = func(*args)

            # Capture and format metrics (if enabled)
            if PERF_ENABLED:
                elapsed_time = time.perf_counter() - start_time
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                time_str = format_time(elapsed_time)
                mem_str = format_memory(peak_mem)
                metrics = f" ({time_str}, {mem_str})"
            else:
                metrics = ""

            # Report results
            display_path = test_case.args if isinstance(test_case.args, str) else test_case.args[0]
            if test_case.expected == actual:
                print(f"  {display_path}: {TRUE_COLOR}{actual}{metrics}{END_COLOR}")
                passed += 1
            else:
                print(
                    f"  {display_path}: {FALSE_COLOR}Expected {test_case.expected} but actual is {actual}{metrics}{END_COLOR}"
                )
                failed += 1
        except Exception as e:
            # Stop tracking on error (if enabled)
            if PERF_ENABLED and tracemalloc.is_tracing():
                tracemalloc.stop()
            display_path = test_case.args if isinstance(test_case.args, str) else test_case.args[0]
            print(
                f"  {display_path}: {FALSE_COLOR}ERROR: {type(e).__name__}: {e}{END_COLOR}"
            )
            failed += 1

    # Print summary
    total = passed + failed
    summary_color = TRUE_COLOR if failed == 0 else FALSE_COLOR
    print(f"{summary_color}  {passed}/{total} tests passed{END_COLOR}")
    print()


__all__ = [
    "TestCase",
    "run",
    "PERF_ENABLED",
    "format_time",
    "format_memory",
]
