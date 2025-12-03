from aoc import Input, run, TestCase, bfs
from collections import defaultdict
import random


def parse_graph(lines):
    """Parse graph from adjacency list format.

    Format: 'jqt: rhn xhk nvd' → bidirectional edges jqt-rhn, jqt-xhk, jqt-nvd
    Skips blank lines automatically.

    Args:
        lines: List of line strings in 'node: conn1 conn2 ...' format

    Returns:
        Adjacency dictionary with bidirectional edges as sets
    """
    graph = defaultdict(set)
    for line in lines:
        if ":" not in line or not line.strip():
            continue
        node, connections = line.split(":", 1)
        node = node.strip()
        for conn in connections.split():
            conn = conn.strip()
            graph[node].add(conn)
            graph[conn].add(node)
    return graph


def find_path_edges(graph, start, end):
    """Find edges in shortest path from start to end"""
    path = bfs(start, lambda n: list(graph[n]), lambda n: n == end)
    if not path:
        return set()

    edges = set()
    for i in range(len(path) - 1):
        edge = tuple(sorted([path[i], path[i + 1]]))
        edges.add(edge)
    return edges


def find_bottleneck_edges(graph):
    """Find 3 edges whose removal partitions graph into 2 components"""
    nodes = list(graph.keys())

    # Try multiple random attempts
    for attempt in range(100):
        edge_counts = defaultdict(int)

        # Sample random paths
        for _ in range(1000):
            start, end = random.sample(nodes, 2)
            for edge in find_path_edges(graph, start, end):
                edge_counts[edge] += 1

        # Get top candidates
        candidates = sorted(edge_counts, key=edge_counts.get, reverse=True)[:10]

        # Try combinations of 3 edges from top candidates
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                for k in range(j + 1, len(candidates)):
                    test_edges = {candidates[i], candidates[j], candidates[k]}

                    # Check if these 3 edges partition the graph
                    def neighbors(node):
                        result = []
                        for neighbor in graph[node]:
                            edge = tuple(sorted([node, neighbor]))
                            if edge not in test_edges:
                                result.append(neighbor)
                        return result

                    distances = bfs(nodes[0], neighbors)
                    if len(distances) != len(nodes):
                        # Found a partition!
                        return list(test_edges)

    return []


def find_partition_product(data_file):
    """Find product of partition sizes after cutting 3 bottleneck edges.

    Uses probabilistic edge detection to identify graph cut edges.
    """
    input_data = Input.from_file(f"./data/{data_file}")
    graph = parse_graph(input_data.as_lines())
    if not graph:
        return 0

    edges_to_cut = set(find_bottleneck_edges(graph))
    if not edges_to_cut:
        return 0

    # Count component sizes
    start_node = next(iter(graph))

    def neighbors(node):
        result = []
        for neighbor in graph[node]:
            edge = tuple(sorted([node, neighbor]))
            if edge not in edges_to_cut:
                result.append(neighbor)
        return result

    distances = bfs(start_node, neighbors)
    size1 = len(distances)
    size2 = len(graph) - size1

    return size1 * size2


if __name__ == "__main__":
    run(
        find_partition_product,
        [
            TestCase("25_example_01", 54),
            TestCase("25_puzzle_input", None),
        ],
    )
