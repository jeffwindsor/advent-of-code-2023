"""Range and interval operations for AOC puzzles.

Common operations for working with ranges and intervals, frequently used in
AOC puzzles for scheduling, overlaps, and coverage problems.
"""

from typing import Iterable


def merge_ranges(ranges: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping or adjacent ranges.

    Args:
        ranges: Iterable of (start, end) tuples (inclusive)

    Returns:
        List of merged non-overlapping ranges, sorted by start position

    Examples:
        >>> merge_ranges([(1, 5), (3, 7), (10, 15)])
        [(1, 7), (10, 15)]
        >>> merge_ranges([(1, 3), (4, 6), (7, 9)])
        [(1, 9)]
        >>> merge_ranges([(5, 10), (1, 3)])
        [(1, 3), (5, 10)]
    """
    if not ranges:
        return []

    # Sort by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if ranges overlap or are adjacent
        if start <= last_end + 1:
            # Merge by extending the last range
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))

    return merged


def intersect_ranges(range1: tuple[int, int], range2: tuple[int, int]) -> tuple[int, int] | None:
    """Find the intersection of two ranges.

    Args:
        range1: First range as (start, end) tuple (inclusive)
        range2: Second range as (start, end) tuple (inclusive)

    Returns:
        Intersection range, or None if ranges don't overlap

    Examples:
        >>> intersect_ranges((1, 5), (3, 7))
        (3, 5)
        >>> intersect_ranges((1, 3), (5, 7))
        None
        >>> intersect_ranges((1, 10), (3, 5))
        (3, 5)
    """
    start1, end1 = range1
    start2, end2 = range2

    # Find the intersection
    intersect_start = max(start1, start2)
    intersect_end = min(end1, end2)

    # Check if there's a valid intersection
    if intersect_start <= intersect_end:
        return (intersect_start, intersect_end)
    return None


def subtract_range(range1: tuple[int, int], range2: tuple[int, int]) -> list[tuple[int, int]]:
    """Subtract range2 from range1.

    Args:
        range1: Range to subtract from (start, end) inclusive
        range2: Range to subtract (start, end) inclusive

    Returns:
        List of remaining ranges after subtraction (0, 1, or 2 ranges)

    Examples:
        >>> subtract_range((1, 10), (5, 7))
        [(1, 4), (8, 10)]
        >>> subtract_range((1, 10), (5, 15))
        [(1, 4)]
        >>> subtract_range((1, 10), (11, 15))
        [(1, 10)]
        >>> subtract_range((5, 7), (1, 10))
        []
    """
    start1, end1 = range1
    start2, end2 = range2

    # No overlap - return original range
    if end2 < start1 or start2 > end1:
        return [(start1, end1)]

    # Complete overlap - nothing remains
    if start2 <= start1 and end2 >= end1:
        return []

    # Partial overlap - return remaining parts
    result = []

    # Left part remains
    if start1 < start2:
        result.append((start1, start2 - 1))

    # Right part remains
    if end1 > end2:
        result.append((end2 + 1, end1))

    return result


def range_contains(outer: tuple[int, int], inner: tuple[int, int]) -> bool:
    """Check if outer range completely contains inner range.

    Args:
        outer: Outer range (start, end) inclusive
        inner: Inner range (start, end) inclusive

    Returns:
        True if outer contains inner, False otherwise

    Examples:
        >>> range_contains((1, 10), (3, 7))
        True
        >>> range_contains((1, 10), (5, 15))
        False
        >>> range_contains((5, 10), (5, 10))
        True
    """
    return outer[0] <= inner[0] and outer[1] >= inner[1]


def range_overlaps(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    """Check if two ranges overlap.

    Args:
        range1: First range (start, end) inclusive
        range2: Second range (start, end) inclusive

    Returns:
        True if ranges overlap, False otherwise

    Examples:
        >>> range_overlaps((1, 5), (3, 7))
        True
        >>> range_overlaps((1, 3), (5, 7))
        False
        >>> range_overlaps((1, 5), (5, 7))
        True
    """
    return range1[0] <= range2[1] and range2[0] <= range1[1]


def range_length(range_tuple: tuple[int, int]) -> int:
    """Calculate the length of a range.

    Args:
        range_tuple: Range as (start, end) tuple (inclusive)

    Returns:
        Length of the range (number of integers in range)

    Examples:
        >>> range_length((1, 5))
        5
        >>> range_length((10, 10))
        1
        >>> range_length((0, 99))
        100
    """
    start, end = range_tuple
    return end - start + 1


def total_coverage(ranges: Iterable[tuple[int, int]]) -> int:
    """Calculate total coverage of ranges (after merging overlaps).

    Args:
        ranges: Iterable of (start, end) tuples (inclusive)

    Returns:
        Total number of integers covered by all ranges

    Examples:
        >>> total_coverage([(1, 5), (3, 7)])
        7
        >>> total_coverage([(1, 3), (5, 7), (10, 12)])
        9
        >>> total_coverage([(1, 5), (10, 15)])
        11
    """
    merged = merge_ranges(ranges)
    return sum(range_length(r) for r in merged)


__all__ = [
    "merge_ranges",
    "intersect_ranges",
    "subtract_range",
    "range_contains",
    "range_overlaps",
    "range_length",
    "total_coverage",
]
