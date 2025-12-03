"""Grid utility functions and Grid class."""

from __future__ import annotations

from typing import Any, Iterator
from dataclasses import dataclass
from .coord import Coord, Dimension


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
        return Coord(col=size.width - 1, row=size.height - 1)

    def coords(self) -> Iterator[tuple[Coord, Any]]:
        """
        Iterate over (coordinate, value) pairs in grid.

        Yields:
            Tuples of (Coord, value) for each cell in the grid
        """
        for r, row in enumerate(self.data):
            for c, value in enumerate(row):
                yield Coord(r, c), value

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


__all__ = ["Grid"]
