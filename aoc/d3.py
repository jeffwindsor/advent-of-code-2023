"""3D coordinate and grid utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Iterator


@dataclass(frozen=True)
class Coord:
    """Immutable 3D coordinate with x, y, and z components."""

    x: int
    y: int
    z: int

    # Class-level direction constants (defined after class for proper initialization)
    ZERO: ClassVar[Coord]
    UP: ClassVar[Coord]
    DOWN: ClassVar[Coord]
    LEFT: ClassVar[Coord]
    RIGHT: ClassVar[Coord]
    FORWARD: ClassVar[Coord]
    BACK: ClassVar[Coord]
    DIRECTIONS_CARDINAL: ClassVar[list[Coord]]

    def __add__(self, other: Coord) -> Coord:
        """Add two coordinates component-wise."""
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Coord) -> Coord:
        """Subtract two coordinates component-wise."""
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def in_bounds(self, max_bounds: Coord, min_bounds: Coord | None = None) -> bool:
        """Check if coordinate is within bounds (inclusive)."""
        min_bounds = min_bounds or Coord(0, 0, 0)
        return (
            min_bounds.x <= self.x <= max_bounds.x
            and min_bounds.y <= self.y <= max_bounds.y
            and min_bounds.z <= self.z <= max_bounds.z
        )

    def manhattan_distance(self, other: Coord) -> int:
        """Calculate 3D Manhattan distance to another coordinate."""
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def squared_distance(self, other: Coord) -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

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
    """Immutable 3D grid dimensions representing width, height, and depth."""

    width: int  # x dimension
    height: int  # y dimension
    depth: int  # z dimension


# Direction constants as class attributes
Coord.ZERO = Coord(0, 0, 0)
Coord.UP = Coord(0, -1, 0)
Coord.DOWN = Coord(0, 1, 0)
Coord.LEFT = Coord(-1, 0, 0)
Coord.RIGHT = Coord(1, 0, 0)
Coord.FORWARD = Coord(0, 0, 1)
Coord.BACK = Coord(0, 0, -1)

Coord.DIRECTIONS_CARDINAL = [
    Coord.UP,
    Coord.DOWN,
    Coord.LEFT,
    Coord.RIGHT,
    Coord.FORWARD,
    Coord.BACK,
]


def filter_coords_in_bounds(
    coords: list[Coord], max_bounds: Coord, min_bounds: Coord | None = None
) -> list[Coord]:
    """Filter coordinates to only those within bounds."""
    return [c for c in coords if c.in_bounds(max_bounds, min_bounds)]


@dataclass
class Grid:
    """
    3D grid wrapper with coordinate-based access.

    Provides clean syntax for 3D grid operations:
    - grid[coord] to access values
    - coord in grid to check bounds
    - Integrates seamlessly with Coord class
    """

    data: list[list[list[Any]]]

    def __getitem__(self, coord: Coord) -> Any:
        """Access grid value using coordinate: grid[coord]."""
        return self.data[coord.z][coord.y][coord.x]

    def __setitem__(self, coord: Coord, value: Any) -> None:
        """Set grid value using coordinate: grid[coord] = value."""
        self.data[coord.z][coord.y][coord.x] = value

    def __contains__(self, coord: Coord) -> bool:
        """Check if coordinate is within bounds: coord in grid."""
        return coord.in_bounds(self.max_bounds)

    @property
    def size(self) -> Dimension:
        """Return size of grid as Dimension(width, height, depth)."""
        if not self.data:
            return Dimension(0, 0, 0)
        if not self.data[0]:
            return Dimension(0, 0, len(self.data))
        if not self.data[0][0]:
            return Dimension(0, len(self.data[0]), len(self.data))
        return Dimension(
            width=len(self.data[0][0]),
            height=len(self.data[0]),
            depth=len(self.data),
        )

    @property
    def max_bounds(self) -> Coord:
        """Return maximum valid indices as Coord(max_x, max_y, max_z)."""
        size = self.size
        return Coord(x=size.width - 1, y=size.height - 1, z=size.depth - 1)

    def coords(self) -> Iterator[tuple[Coord, Any]]:
        """
        Iterate over (coordinate, value) pairs in grid.

        Yields:
            Tuples of (Coord, value) for each cell in the 3D grid
        """
        for x, plane in enumerate(self.data):
            for y, row in enumerate(plane):
                for z, value in enumerate(row):
                    yield Coord(x, y, z), value

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

    @staticmethod
    def create(size: Dimension, initial_value: Any) -> Grid:
        """
        Create a 3D grid filled with initial value.

        Args:
            size: Size of the grid as Dimension(width, height, depth)
            initial_value: Value to fill the grid with

        Returns:
            Grid instance initialized with the specified value
        """
        data = [
            [[initial_value] * size.width for _ in range(size.height)]
            for _ in range(size.depth)
        ]
        return Grid(data)


__all__ = [
    "Coord",
    "Dimension",
    "filter_coords_in_bounds",
    "Grid",
]
