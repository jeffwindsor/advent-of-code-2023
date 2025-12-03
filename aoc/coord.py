"""Coordinate class and coordinate utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Coord:
    """Immutable 2D coordinate with row and column components."""

    row: int
    col: int

    # Class-level direction constants (defined after class for proper initialization)
    ZERO: ClassVar[Coord]
    UP: ClassVar[Coord]
    RIGHT: ClassVar[Coord]
    DOWN: ClassVar[Coord]
    LEFT: ClassVar[Coord]
    UP_LEFT: ClassVar[Coord]
    DOWN_LEFT: ClassVar[Coord]
    UP_RIGHT: ClassVar[Coord]
    DOWN_RIGHT: ClassVar[Coord]
    DIRECTIONS_CARDINAL: ClassVar[list[Coord]]
    DIRECTIONS_INTERCARDINAL: ClassVar[list[Coord]]
    DIRECTIONS_ALL: ClassVar[list[Coord]]
    TURN_CLOCKWISE: ClassVar[dict[Coord, Coord]]
    TURN_COUNTER_CLOCKWISE: ClassVar[dict[Coord, Coord]]

    def __add__(self, other: Coord) -> Coord:
        """Add two coordinates component-wise."""
        return Coord(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Coord) -> Coord:
        """Subtract two coordinates component-wise."""
        return Coord(self.row - other.row, self.col - other.col)

    def in_bounds(self, max_bounds: Coord, min_bounds: Coord | None = None) -> bool:
        """Check if coordinate is within bounds (inclusive)."""
        min_bounds = min_bounds or Coord(0, 0)
        return (
            min_bounds.row <= self.row <= max_bounds.row
            and min_bounds.col <= self.col <= max_bounds.col
        )

    def manhattan_distance(self, other: Coord) -> int:
        """Calculate Manhattan distance to another coordinate."""
        return abs(self.row - other.row) + abs(self.col - other.col)

    def neighbors(
        self, max_bounds: Coord, directions: list[Coord] | None = None
    ) -> list[Coord]:
        """
        Get valid neighbors within bounds.

        Args:
            max_bounds: Maximum coordinate bounds
            directions: List of direction vectors (default: DIRECTIONS_CARDINAL)

        Returns:
            List of valid neighbor coordinates
        """
        directions = directions or Coord.DIRECTIONS_CARDINAL
        return [
            neighbor for d in directions if (neighbor := self + d).in_bounds(max_bounds)
        ]


@dataclass(frozen=True)
class Dimension:
    """Immutable 2D grid dimensions representing width and height."""

    width: int  # number of columns
    height: int  # number of rows


# Direction constants as class attributes
Coord.ZERO = Coord(0, 0)
Coord.UP = Coord(-1, 0)
Coord.RIGHT = Coord(0, 1)
Coord.DOWN = Coord(1, 0)
Coord.LEFT = Coord(0, -1)
Coord.UP_LEFT = Coord(-1, -1)
Coord.DOWN_LEFT = Coord(1, -1)
Coord.UP_RIGHT = Coord(-1, 1)
Coord.DOWN_RIGHT = Coord(1, 1)

Coord.DIRECTIONS_CARDINAL = [Coord.UP, Coord.RIGHT, Coord.DOWN, Coord.LEFT]
Coord.DIRECTIONS_INTERCARDINAL = [
    Coord.UP_LEFT,
    Coord.UP_RIGHT,
    Coord.DOWN_LEFT,
    Coord.DOWN_RIGHT,
]
Coord.DIRECTIONS_ALL = Coord.DIRECTIONS_CARDINAL + Coord.DIRECTIONS_INTERCARDINAL
Coord.TURN_CLOCKWISE = {
    Coord.UP: Coord.RIGHT,
    Coord.RIGHT: Coord.DOWN,
    Coord.DOWN: Coord.LEFT,
    Coord.LEFT: Coord.UP,
}
Coord.TURN_COUNTER_CLOCKWISE = {
    Coord.UP: Coord.LEFT,
    Coord.LEFT: Coord.DOWN,
    Coord.DOWN: Coord.RIGHT,
    Coord.RIGHT: Coord.UP,
}


def filter_coords_in_bounds(
    coords: list[Coord], max_bounds: Coord, min_bounds: Coord | None = None
) -> list[Coord]:
    """Filter coordinates to only those within bounds."""
    return [c for c in coords if c.in_bounds(max_bounds, min_bounds)]


__all__ = [
    "Coord",
    "Dimension",
    "filter_coords_in_bounds",
]
