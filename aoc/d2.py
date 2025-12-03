"""2D coordinate and grid utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Iterator


@dataclass(frozen=True)
class Coord:
    """Immutable 2D coordinate with x and y components."""

    x: int
    y: int

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
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coord) -> Coord:
        """Subtract two coordinates component-wise."""
        return Coord(self.x - other.x, self.y - other.y)

    @classmethod
    def from_rc(cls, row: int, col: int) -> Coord:
        """Create coordinate from row,col (grid) format."""
        return cls(x=col, y=row)

    @property
    def row(self) -> int:
        """Get row coordinate (y)."""
        return self.y

    @property
    def col(self) -> int:
        """Get column coordinate (x)."""
        return self.x

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

    def squared_distance(self, other: Coord) -> int:
        return (self.row - other.row) ** 2 + (self.col - other.col) ** 2

    def euclidean_distance(self, other: Coord) -> float:
        return (self.squared_distance(other)) ** 0.5

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
Coord.UP = Coord(0, -1)
Coord.RIGHT = Coord(1, 0)
Coord.DOWN = Coord(0, 1)
Coord.LEFT = Coord(-1, 0)
Coord.UP_LEFT = Coord(-1, -1)
Coord.DOWN_LEFT = Coord(-1, 1)
Coord.UP_RIGHT = Coord(1, -1)
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


@dataclass
class Grid:
    """
    2D grid wrapper with coordinate-based access.

    Provides clean syntax for grid operations:
    - grid[coord] to access values
    - coord in grid to check bounds
    - Integrates seamlessly with Coord class
    """

    data: list[list[Any]]

    def __getitem__(self, coord: Coord) -> Any:
        """Access grid value using coordinate: grid[coord]."""
        return self.data[coord.row][coord.col]

    def __setitem__(self, coord: Coord, value: Any) -> None:
        """Set grid value using coordinate: grid[coord] = value."""
        self.data[coord.row][coord.col] = value

    def __contains__(self, coord: Coord) -> bool:
        """Check if coordinate is within bounds: coord in grid."""
        return coord.in_bounds(self.max_bounds)

    @property
    def size(self) -> Dimension:
        """Return size of grid as Dimensions(width, height)."""
        return Dimension(
            width=len(self.data[0]) if self.data else 0, height=len(self.data)
        )

    @property
    def max_bounds(self) -> Coord:
        """Return maximum valid indices as Dimensions(max_col, max_row)."""
        size = self.size
        return Coord.from_rc(col=size.width - 1, row=size.height - 1)

    def coords(self) -> Iterator[tuple[Coord, Any]]:
        """
        Iterate over (coordinate, value) pairs in grid.

        Yields:
            Tuples of (Coord, value) for each cell in the grid
        """
        for r, row in enumerate(self.data):
            for c, value in enumerate(row):
                yield Coord.from_rc(r, c), value

    def find_first(self, value: Any) -> Coord | None:
        """Find first occurrence of value in grid, return coordinate or None."""
        for coord, cell_value in self.coords():
            if cell_value == value:
                return coord
        return None

    def find_all(self, value: Any) -> list[Coord]:
        """Find all occurrences of value in grid, return list of coordinates."""
        return [coord for coord, cell_value in self.coords() if cell_value == value]

    def group_by_value(self, exclude: Any | None = None) -> dict[Any, list[Coord]]:
        """
        Group coordinates by their cell values.

        Args:
            exclude: Optional value to exclude from grouping

        Returns:
            Dictionary mapping values to lists of coordinates with that value
        """
        result = {}
        for coord, value in self.coords():
            if value != exclude:
                result.setdefault(value, []).append(coord)
        return result

    def search_in_direction(self, start: Coord, direction: Coord, target: str) -> bool:
        """
        Search for a string in the grid following a specific direction.

        Args:
            start: Starting coordinate
            direction: Direction vector to follow
            target: String to search for

        Returns:
            True if the target string is found in the specified direction
        """
        for i, char in enumerate(target):
            coord = Coord(start.x + i * direction.x, start.y + i * direction.y)
            if coord not in self or self[coord] != char:
                return False
        return True

    @staticmethod
    def create(size: Dimension, initial_value: Any) -> Grid:
        """
        Create a grid filled with initial value.

        Args:
            size: Size of the grid as Dimension(width, height)
            initial_value: Value to fill the grid with

        Returns:
            Grid instance initialized with the specified value
        """
        data = [[initial_value] * size.width for _ in range(size.height)]
        return Grid(data)


__all__ = [
    "Coord",
    "Dimension",
    "filter_coords_in_bounds",
    "Grid",
]
