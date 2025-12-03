"""Graph algorithms (BFS, DFS, Dijkstra, max clique)."""

from typing import Any, Callable
from collections import deque
from heapq import heappush, heappop
from .d2 import Coord, Grid


def bfs(
    start: Any,
    neighbors_func: Callable[[Any], list[Any]],
    goal_func: Callable[[Any], bool] | None = None,
) -> dict[Any, int] | list[Any]:
    """
    Generic breadth-first search algorithm.

    Args:
        start: Starting state (Coord, tuple, or any hashable type)
        neighbors_func: Function that returns valid neighbors for a state
        goal_func: Optional function to check if goal is reached

    Returns:
        If goal_func is None: dict mapping states to distances from start
        If goal_func provided: list of states forming path to goal, or empty list if no path

    Examples:
        # Find all distances
        >>> distances = bfs(start_coord, neighbors_func)

        # Find path to goal
        >>> path = bfs(start_coord, neighbors_func, lambda c: c == goal)
    """
    queue = deque([start])
    visited = {start}
    distances = {start: 0}
    parents = {start: None}

    while queue:
        current = queue.popleft()

        if goal_func and goal_func(current):
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parents[node]
            return list(reversed(path))

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                parents[neighbor] = current
                queue.append(neighbor)

    return distances if not goal_func else []


def dfs(
    start: Any,
    neighbors_func: Callable[[Any], list[Any]],
    goal_func: Callable[[Any], bool],
) -> list[Any] | None:
    """
    Generic depth-first search algorithm.
    Optimized with parent tracking for O(n) time and memory complexity.

    Args:
        start: Starting state (Coord, tuple, or any hashable type)
        neighbors_func: Function that returns valid neighbors for a state
        goal_func: Function to check if goal is reached

    Returns:
        List of states forming path to goal, or None if no path found

    Note:
        Uses parent tracking and backtracking for efficient O(n) path construction,
        avoiding the O(n²) cost of incrementally building paths during search.
    """
    stack = [(start, None)]  # (current, parent)
    parent_map = {}
    visited = set()

    while stack:
        current, parent = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        parent_map[current] = parent

        if goal_func(current):
            # Reconstruct path by backtracking from goal to start
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent_map[node]
            return list(reversed(path))

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                stack.append((neighbor, current))

    return None


def _create_grid_search_functions(
    grid: Grid,
    end: Coord,
    walkable_values: set[Any],
) -> tuple[Callable[[Coord], list[Coord]], Callable[[Coord], bool]]:
    """
    Create neighbor and goal functions for grid pathfinding.

    Shared logic extracted from bfs_grid_path and dfs_grid_path.

    Args:
        grid: Grid instance to search through
        end: Goal coordinate
        walkable_values: Set of grid values that can be traversed

    Returns:
        Tuple of (neighbors_func, goal_func) for use with generic search algorithms
    """
    def neighbors_func(coord: Coord) -> list[Coord]:
        """Get valid neighboring coordinates in the grid."""
        return [
            neighbor
            for direction in Coord.DIRECTIONS_CARDINAL
            if (neighbor := coord + direction) in grid
            and grid[neighbor] in walkable_values
        ]

    def goal_func(coord: Coord) -> bool:
        """Check if we've reached the goal."""
        return coord == end

    return neighbors_func, goal_func


def bfs_grid_path(
    grid: Grid,
    start: Coord,
    end: Coord,
    walkable_values: set[Any],
) -> list[Coord]:
    """
    Convenience wrapper for breadth-first search through a grid maze.

    This is a specialized interface to the generic bfs() function,
    optimized for grid-based shortest pathfinding problems.

    Args:
        grid: Grid instance to search through
        start: Starting coordinate
        end: Goal coordinate
        walkable_values: Set of grid values that can be traversed

    Returns:
        List of coordinates forming shortest path from start to end, or empty list if no path found

    Example:
        >>> maze = Grid([['#', '.', '#'], ['.', '.', '.'], ['#', '.', '#']])
        >>> path = bfs_grid_path(maze, Coord(0,1), Coord(2,1), {'.'}  )
        >>> len(path) > 0
        True

    Note:
        BFS guarantees the shortest path in unweighted graphs.
    """
    neighbors_func, goal_func = _create_grid_search_functions(grid, end, walkable_values)
    result = bfs(start, neighbors_func, goal_func)
    return result if result else None


def dfs_grid_path(
    grid: Grid,
    start: Coord,
    end: Coord,
    walkable_values: set[Any],
) -> list[Coord]:
    """
    Convenience wrapper for depth-first search through a grid maze.

    This is a specialized interface to the generic dfs() function,
    optimized for grid-based pathfinding problems.

    Args:
        grid: Grid instance to search through
        start: Starting coordinate
        end: Goal coordinate
        walkable_values: Set of grid values that can be traversed

    Returns:
        List of coordinates forming path from start to end, or empty list if no path found

    Example:
        >>> maze = Grid([['#', '.', '#'], ['.', '.', '.'], ['#', '.', '#']])
        >>> path = dfs_grid_path(maze, Coord(0,1), Coord(2,1), {'.'}  )
        >>> len(path) > 0
        True

    Note:
        DFS does not guarantee the shortest path. Use bfs_grid_path for shortest paths.
        This wrapper uses the generic dfs() implementation with parent tracking
        for efficient O(n) time and memory complexity.
    """
    neighbors_func, goal_func = _create_grid_search_functions(grid, end, walkable_values)
    result = dfs(start, neighbors_func, goal_func)
    return result if result is not None else []


def dijkstra(
    start: Any,
    neighbors_func: Callable[[Any], list[tuple[Any, int]]],
    goal: Any | None = None,
) -> dict[Any, int]:
    """
    Dijkstra's shortest path algorithm (generalized for any hashable state).

    Args:
        start: Starting state (can be Coord, tuple, or any hashable type)
        neighbors_func: Function returning list of (neighbor_state, cost) tuples
        goal: Optional goal state (returns early if found)

    Returns:
        Dictionary mapping states to shortest distances from start

    Examples:
        # Original usage with Coord
        >>> distances = dijkstra(Coord(0,0), neighbors_func)

        # New usage with state tuples (coord, direction)
        >>> distances = dijkstra((Coord(0,0), 0), state_neighbors_func)
    """
    counter = 0
    pq = [(0, counter, start)]
    distances = {start: 0}
    visited = set()

    while pq:
        dist, _, current = heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if goal and current == goal:
            return distances

        for neighbor, cost in neighbors_func(current):
            new_dist = dist + cost
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                counter += 1
                heappush(pq, (new_dist, counter, neighbor))

    return distances


def flood_fill(
    grid: Grid,
    start: Coord,
    walkable_values: set[Any],
    directions: list[Coord] | None = None,
) -> set[Coord]:
    """
    Non-destructive flood fill that returns all reachable coordinates.

    Uses BFS to explore all cells reachable from start position through
    walkable cells. Does not modify the grid.

    Args:
        grid: Grid instance to search through
        start: Starting coordinate for flood fill
        walkable_values: Set of grid values that can be traversed
        directions: Direction vectors to use (default: DIRECTIONS_CARDINAL for 4-way)

    Returns:
        Set of all coordinates reachable from start (empty set if start invalid)

    Example:
        >>> grid = Grid([['#', '.', '#'], ['.', '.', '.'], ['#', '.', '#']])
        >>> visited = flood_fill(grid, Coord(1, 1), {'.'})
        >>> len(visited)
        5

    Note:
        For in-place marking of visited cells, use flood_fill_mark() instead.
    """
    if start not in grid or grid[start] not in walkable_values:
        return set()

    directions = directions or Coord.DIRECTIONS_CARDINAL

    def neighbors_func(coord: Coord) -> list[Coord]:
        return [
            neighbor
            for direction in directions
            if (neighbor := coord + direction) in grid
            and grid[neighbor] in walkable_values
        ]

    distances = bfs(start, neighbors_func)
    return set(distances.keys())


def flood_fill_mark(
    grid: Grid,
    start: Coord,
    mark_value: Any,
    walkable_values: set[Any],
    directions: list[Coord] | None = None,
) -> int:
    """
    Destructive flood fill that marks all reachable coordinates in-place.

    Uses flood_fill() to find reachable cells, then modifies the grid by
    setting all visited cells to mark_value.

    Args:
        grid: Grid instance to modify
        start: Starting coordinate for flood fill
        mark_value: Value to mark visited cells with
        walkable_values: Set of grid values that can be traversed
        directions: Direction vectors to use (default: DIRECTIONS_CARDINAL for 4-way)

    Returns:
        Count of cells marked (0 if start invalid or no cells reachable)

    Example:
        >>> grid = Grid([['#', '.', '#'], ['.', '.', '.'], ['#', '.', '#']])
        >>> count = flood_fill_mark(grid, Coord(1, 1), 'X', {'.'})
        >>> count
        5
        >>> grid[Coord(1, 1)]
        'X'

    Note:
        This modifies the grid in-place. For non-destructive analysis,
        use flood_fill() instead.
    """
    visited = flood_fill(grid, start, walkable_values, directions)

    for coord in visited:
        grid[coord] = mark_value

    return len(visited)


def count_paths_dag(
    start: Any,
    neighbors_func: Callable[[Any], list[Any]],
    goal_func: Callable[[Any], bool],
) -> int:
    """
    Count all paths from start to goal in a directed acyclic graph (DAG).

    Uses memoization for efficient counting. Assumes the graph is acyclic.

    Args:
        start: Starting node
        neighbors_func: Function that returns list of neighbor nodes
        goal_func: Function that returns True when goal is reached

    Returns:
        Number of distinct paths from start to goal

    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
        >>> count_paths_dag('A', lambda n: graph.get(n, []), lambda n: n == 'D')
        2
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def count(current):
        if goal_func(current):
            return 1
        return sum(count(neighbor) for neighbor in neighbors_func(current))

    return count(start)


def count_paths_cyclic(
    start: Any,
    neighbors_func: Callable[[Any], list[Any]],
    goal_func: Callable[[Any], bool],
) -> int:
    """
    Count all paths from start to goal in a graph that may contain cycles.

    Uses backtracking to avoid revisiting nodes within the same path.

    Args:
        start: Starting node
        neighbors_func: Function that returns list of neighbor nodes
        goal_func: Function that returns True when goal is reached

    Returns:
        Number of distinct paths from start to goal

    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['C'], 'C': ['A', 'D'], 'D': []}
        >>> count_paths_cyclic('A', lambda n: graph.get(n, []), lambda n: n == 'D')
        2
    """
    def count(current, visited):
        if goal_func(current):
            return 1
        visited.add(current)
        total = sum(
            count(neighbor, visited)
            for neighbor in neighbors_func(current)
            if neighbor not in visited
        )
        visited.remove(current)
        return total

    return count(start, set())


def find_max_clique(graph: dict[Any, set[Any]]) -> set[Any]:
    """
    Find the largest clique (fully-connected subgraph) using Bron-Kerbosch algorithm.

    A clique is a subset of nodes where every node is connected to every other node.
    This uses the Bron-Kerbosch algorithm to efficiently enumerate all maximal cliques.

    Args:
        graph: Adjacency graph (dict mapping nodes to sets of neighbors)

    Returns:
        Set of nodes forming the largest clique

    Example:
        >>> graph = {'a': {'b', 'c'}, 'b': {'a', 'c'}, 'c': {'a', 'b'}}
        >>> find_max_clique(graph)
        {'a', 'b', 'c'}  # All three nodes form a complete triangle
    """
    def bron_kerbosch(R: set, P: set, X: set, cliques: list):
        """
        Bron-Kerbosch algorithm to find all maximal cliques.

        Args:
            R: Current clique being built
            P: Candidate vertices that could extend R
            X: Vertices already processed
            cliques: List to collect all maximal cliques
        """
        if not P and not X:
            # Found a maximal clique
            cliques.append(R.copy())
            return

        # Iterate over a copy of P since we modify it
        for v in list(P):
            neighbors = graph.get(v, set())
            bron_kerbosch(
                R | {v},           # Add v to current clique
                P & neighbors,     # Candidates must be neighbors of v
                X & neighbors,     # Processed must be neighbors of v
                cliques
            )
            P.remove(v)           # Remove v from candidates
            X.add(v)              # Add v to processed

    cliques = []
    vertices = set(graph.keys())
    bron_kerbosch(set(), vertices, set(), cliques)

    # Return the largest clique found
    return max(cliques, key=len) if cliques else set()


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure for tracking connected components.

    Supports dynamic element addition and works with any hashable type.
    Uses path compression and union by rank for efficiency.
    """

    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.size = {}

    def find(self, x):
        """Find the root of the set containing x with path compression."""
        # Auto-add new elements
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.size[x] = 1

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union the sets containing x and y. Returns True if they were in different sets."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1

        return True

    def get_component_sizes(self):
        """Get a dictionary mapping each root to its component size."""
        sizes = {}
        for element in list(self.parent.keys()):
            root = self.find(element)
            if root not in sizes:
                sizes[root] = self.size[root]
        return sizes

    def count_components(self):
        """Count the number of disjoint components."""
        roots = set()
        for element in list(self.parent.keys()):
            roots.add(self.find(element))
        return len(roots)


__all__ = [
    "bfs",
    "dfs",
    "bfs_grid_path",
    "dfs_grid_path",
    "flood_fill",
    "flood_fill_mark",
    "dijkstra",
    "count_paths_dag",
    "count_paths_cyclic",
    "find_max_clique",
    "UnionFind",
]
