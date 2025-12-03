"""
Input parsing utilities for Advent of Code puzzles.

This module provides flexible parsing for common Advent of Code input patterns
through the Input class, which handles both file-based and string-based parsing.

Supported Parsing Scenarios
----------------------------

**Single line of integers** - ``parse_lines(int)``
    Parse each line as a single integer using parse_lines with int converter.

    Example: ``"123\\n456\\n789"`` → ``[123, 456, 789]``

**Column-based parsing** - ``as_columns()``
    Parse whitespace-separated values into columns (transpose rows to columns).

    Example: ``"3   4\\n8   10"`` → ``[('3', '8'), ('4', '10')]``

    With converter: ``as_columns(converter=int)`` → ``[(3, 8), (4, 10)]``

**Line-by-line data** - ``as_lines()``
    Split content into list of strings, one per line.

    Example: ``"line one\\nline two\\nline three"`` → ``['line one', 'line two', 'line three']``

**Character grid** - ``as_char_grid()``, ``as_grid()``
    Parse content as 2D array of characters. Use ``as_grid()`` for Grid wrapper with coordinate access.

    Example: ``"XMAS\\nMASX"`` → ``[['X', 'M', 'A', 'S'], ['M', 'A', 'S', 'X']]``

**Numeric grid** - ``as_int_grid()``
    Parse digit characters into 2D integer array (non-digits become -1 by default).

    Example: ``"0123\\n4567\\n89.."`` → ``[[0,1,2,3], [4,5,6,7], [8,9,-1,-1]]``

**Coordinate pairs** - ``as_coord_pairs()``
    Parse comma-separated coordinate pairs into list of (x, y) tuples.

    Example: ``"6,1\\n8,3\\n12,5"`` → ``[(6, 1), (8, 3), (12, 5)]``

**Graph edges** - ``as_graph_edges()``
    Parse node connections into adjacency dictionary (undirected by default).

    Example: ``"kh-tc\\ntc-wh\\nwh-yn"`` → ``{'kh': {'tc'}, 'tc': {'kh', 'wh'}, ...}``

**Dense single-line string** - ``.content``
    Access raw content string for character-by-character processing.

    Example: ``"2333133121414131402"`` → raw string

**Key-value pairs** - ``as_key_value_pairs()``
    Parse colon-separated key-value format (values default to list of integers).

    Example: ``"190: 10 19\\n3267: 81 40 27"`` → ``[(190, [10, 19]), (3267, [81, 40, 27])]``

**Pipe-separated ordering rules** - ``as_pipe_rules()``
    Parse ordering/dependency rules in "X|Y" format into dictionary.

    Example: ``"47|53\\n97|13\\n75|29"`` → ``{47: [53], 97: [13], 75: [29]}``

**Comma-separated values per line** - ``as_csv_lines()``
    Parse each line as comma-separated values (default: integers).

    Example: ``"75,47,61,53,29\\n97,61,53,29,13"`` → ``[[75,47,61,53,29], [97,61,53,29,13]]``

**Multi-pattern regex extractor** - ``as_regex_groups()``
    Extract regex capture groups from each line.

    Example: ``"p=100,351 v=-10,25\\np=50,100 v=5,-3"`` → ``[('100','351','-10','25'), ('50','100','5','-3')]``

**Structured integers extractor** - ``as_structured_ints()``
    Extract all integers from complex text using regex (validates count per line).

    Example: ``"p=100,351 v=-10,25"`` → ``(100, 351, -10, 25)``

**Multi-section split** - ``as_sections()``
    Split content on blank lines into list of Input objects.

    Example: ``"sec1\\n\\nsec2\\n\\nsec3"`` → ``[Input('sec1'), Input('sec2'), Input('sec3')]``

    Two sections: ``part1, part2 = input.as_sections()`` unpacks directly

Usage Examples
--------------

File-based parsing::

    from aoc import Input

    # Read and parse file
    input = Input("data/05_puzzle_input")
    lines = input.as_lines()

    # Or use factory method explicitly
    input = Input.from_file("data/05_puzzle_input")

    # Split into two sections
    rules, updates = input.as_sections()

String-based parsing::

    from aoc import Input

    # Parse string content
    input = Input.from_string("1,2,3\\n4,5,6")
    data = input.as_csv_lines()  # [[1, 2, 3], [4, 5, 6]]

Classes
-------
Input
    Flexible text parser with composable methods for file or string content
"""

from collections import defaultdict
from re import findall, error, search
from .d2 import Coord, Grid


def extract_ints(text: str, pattern: str = r"-?\d+") -> list[int]:
    """
    Extract integers from text using regex pattern.

    Args:
        text: Text to extract from
        pattern: Regex pattern (default: matches integers including negatives)

    Returns:
        List of extracted integers

    Raises:
        ValueError: If pattern is invalid or produces non-integer matches

    Example:
        >>> extract_ints("x=10 y=-5")
        [10, -5]
    """

    try:
        return [int(m) for m in extract_pattern(text, pattern)]
    except error as e:
        raise ValueError(f"Invalid regex pattern: {e}")
    except ValueError as e:
        raise ValueError(f"Pattern matched non-integer values: {e}")


def extract_pattern(text: str, pattern: str) -> list[str]:
    """
    Extract pattern matches from text (generic version).

    Args:
        text: Text to extract from
        pattern: Regex pattern

    Returns:
        List of matched strings

    Raises:
        ValueError: If pattern is invalid

    Example:
        >>> input = Input.from_string("")
        >>> input.extract_pattern("a1 b2 c3", r"[a-z]\\d")
        ['a1', 'b2', 'c3']
    """

    try:
        return findall(pattern, text)
    except error as e:
        raise ValueError(f"Invalid regex pattern: {e}")


def pattern_to_bools(text: str, true_char: str = '#') -> list[bool]:
    """
    Convert character pattern to boolean list.

    Args:
        text: String pattern (e.g., ".##.#")
        true_char: Character representing True (default: '#')

    Returns:
        List of booleans

    Examples:
        >>> pattern_to_bools(".##.#")
        [False, True, True, False, True]
        >>> pattern_to_bools("..##", true_char='#')
        [False, False, True, True]
        >>> pattern_to_bools("0110", true_char='1')
        [False, True, True, False]
    """
    return [c == true_char for c in text]


def extract_bracketed(text: str) -> str | None:
    """
    Extract content from square brackets [...].

    Args:
        text: Text to extract from

    Returns:
        Content inside first square brackets, or None if not found

    Example:
        >>> extract_bracketed("[.##.#] data")
        '.##.#'
    """
    match = search(r"\[([^\]]+)\]", text)
    return match.group(1) if match else None


def extract_parenthesized(text: str) -> list[str]:
    """
    Extract all content from parentheses (...).

    Args:
        text: Text to extract from

    Returns:
        List of all content inside parentheses

    Example:
        >>> extract_parenthesized("(1,2) text (3,4)")
        ['1,2', '3,4']
    """
    return findall(r"\(([^\)]+)\)", text)


def extract_braced(text: str) -> str | None:
    """
    Extract content from curly braces {...}.

    Args:
        text: Text to extract from

    Returns:
        Content inside first curly braces, or None if not found

    Example:
        >>> extract_braced("data {3,5,4}")
        '3,5,4'
    """
    match = search(r"\{([^\}]+)\}", text)
    return match.group(1) if match else None


def parse(content: str, sep: str | None, skip_empty: bool = True, strip: bool = True) -> list[str]:
    """
    Split content by separator.

    Args:
        content: String content to split
        sep: Separator to split on (if empty/None, returns char array)
        skip_empty: Skip empty parts after stripping whitespace (default: True)
        strip: Strip whitespace from parts (default: True)

    Returns:
        List of strings (or list of characters if sep is empty/None)
    """
    if not sep:
        return list(content)

    parts = content.split(sep)
    if skip_empty:
        if strip:
            return [stripped for part in parts if (stripped := part.strip())]
        else:
            return [part for part in parts if part]
    return parts


class Input:
    """
    Flexible text parser with composable methods for various input formats.

    Input provides primitive parsing operations (parse_lines, parse_sections,
    convert_values, extract_ints) that compose into high-level methods for
    common Advent of Code patterns. Create Input from files using from_file()
    or from strings using from_string().

    Example:
        >>> input = Input.from_string("1,2,3\\n4,5,6")
        >>> input.as_csv_lines()
        [[1, 2, 3], [4, 5, 6]]
    """

    LINE_SEPARATOR = "\n"
    SECTION_SEPARATOR = "\n\n"

    def __init__(self, content: str, line_sep: str = None, section_sep: str = None, strip_content: bool = True):
        """
        Initialize Input with content and separators.

        Args:
            content: Text content to parse
            line_sep: Separator between lines (default: newline)
            section_sep: Separator between sections (default: blank line)
            strip_content: Strip whitespace from content (default: True)
        """
        # Skip initialization if already initialized by __new__/from_file/from_string
        if hasattr(self, "_content"):
            return
        self._content = content
        self._line_sep = line_sep or self.LINE_SEPARATOR
        self._section_sep = section_sep or self.SECTION_SEPARATOR
        self._strip_content = strip_content

    def __new__(cls, filepath: str):
        """
        Create Input from file path.

        Always reads from file - use Input.from_string() for string content.

        Args:
            filepath: Path to input file

        Returns:
            Input instance with file contents
        """
        return cls.from_file(filepath)

    @staticmethod
    def from_file(
        filepath: str,
        line_sep: str = None,
        section_sep: str = None,
        strip_content: bool = True,
    ) -> "Input":
        """
        Create Input from file (reads immediately).

        Args:
            filepath: Path to input file
            line_sep: Separator between lines (default: newline)
            section_sep: Separator between sections (default: blank line)
            strip_content: Strip whitespace from content (default: True)

        Returns:
            Input instance with file contents

        Example:
            >>> input = Input.from_file("data/01_puzzle_input")
            >>> input.as_lines()
            ['123', '456', '789']
        """
        with open(filepath) as f:
            content = f.read()
            if strip_content:
                content = content.strip()
        return Input.from_string(content, line_sep, section_sep, strip_content)

    @staticmethod
    def from_string(
        content: str,
        line_sep: str = None,
        section_sep: str = None,
        strip_content: bool = True,
    ) -> "Input":
        """
        Create Input from string content.

        Args:
            content: String content to parse
            line_sep: Separator between lines (default: newline)
            section_sep: Separator between sections (default: blank line)
            strip_content: Strip whitespace from content (default: True)

        Returns:
            Input instance

        Example:
            >>> input = Input.from_string("1,2,3\\n4,5,6")
            >>> input.as_csv_lines()
            [[1, 2, 3], [4, 5, 6]]
        """
        # Create instance directly to avoid __new__ logic
        instance = object.__new__(Input)
        instance._content = content
        instance._line_sep = line_sep or Input.LINE_SEPARATOR
        instance._section_sep = section_sep or Input.SECTION_SEPARATOR
        instance._strip_content = strip_content
        return instance

    @property
    def content(self) -> str:
        """
        Get raw content string.

               Returns:
                   The unparsed content string
        """
        return self._content

    def parse(self, sep: str | None, skip_empty: bool = True) -> list[str]:
        """
        Split content by separator.

        Args:
            sep: Separator to split on (if empty/None, returns char array)
            skip_empty: Skip empty parts after stripping whitespace (default: True)

        Returns:
            List of strings (or list of characters if sep is empty/None)
        """
        return parse(self._content, sep, skip_empty, strip=self._strip_content)

    def as_lines(self, skip_empty: bool = True) -> list[str]:
        """
            Parse content as list of lines.

        Args:
            skip_empty: Skip empty lines after stripping (default: True)

        Returns:
            List of line strings

        Example:
            >>> Input.from_string("line1\\nline2\\n\\nline3").as_lines()
            ['line1', 'line2', 'line3']
        """
        return self.parse(self._line_sep, skip_empty=skip_empty)

    def as_grid(self, converter: type | None = None) -> Grid:
        """
        Parse content as 2D character grid.

        Args:
            converter: Optional type function to apply to each character

        Returns:
            Grid instance wrapping character grid

        Examples:
            Default (character grid):
            >>> Input.from_string("ABC\\nDEF").as_grid()
            Grid([['A', 'B', 'C'], ['D', 'E', 'F']])

            With converter:
            >>> Input.from_string("abc\\ndef").as_grid(converter=str.upper)
            Grid([['A', 'B', 'C'], ['D', 'E', 'F']])
        """
        if converter is None:
            return Grid([list(line) for line in self.as_lines()])
        return Grid([[converter(char) for char in line] for line in self.as_lines()])

    def as_int_grid(self, empty_value: int = -1) -> Grid:
        """
        Parse content as 2D integer grid (digit characters only).

        Args:
            empty_value: Value for non-digit characters (default: -1)

        Returns:
            Grid instance wrapping integer grid

        Example:
            >>> Input.from_string("012\\n345\\n6.8").as_int_grid()
            Grid([[0, 1, 2], [3, 4, 5], [6, -1, 8]])
        """
        return self.as_conditional_grid(
            check=str.isdigit, converter=int, empty_value=empty_value
        )

    def as_conditional_grid(
        self, check: callable, converter: type, empty_value: any = None
    ) -> Grid:
        """
        Parse content as 2D grid with conditional conversion.

        Args:
            check: Function to test each character (returns bool)
            converter: Type function to apply when check passes
            empty_value: Value to use when check fails

        Returns:
            Grid instance with conditionally converted values

        Example:
            >>> Input.from_string("1a2\\n3b4").as_conditional_grid(
            ...     check=str.isdigit, converter=int, empty_value=-1
            ... )
            Grid([[1, -1, 2], [3, -1, 4]])
        """
        return Grid(
            [
                [converter(char) if check(char) else empty_value for char in line]
                for line in self.as_lines()
            ]
        )

    def as_float_grid(self, empty_value: float = 0.0) -> Grid:
        """
        Parse content as 2D float grid.

        Args:
            empty_value: Value for non-numeric characters (default: 0.0)

        Returns:
            Grid instance wrapping float grid

        Example:
            >>> Input.from_string("1.5 2.7\\n3.2 4.8").as_float_grid()
            Grid([[1.5, 2.7], [3.2, 4.8]])
        """

        def is_float_char(c: str) -> bool:
            return c.isdigit() or c == "." or c == "-"

        return self.as_conditional_grid(
            check=is_float_char, converter=float, empty_value=empty_value
        )

    def as_columns(
        self, separator: str | None = None, converter: type = None
    ) -> list[tuple]:
        """
        Parse content as columns (transpose rows to columns).

        Args:
            separator: Delimiter between values (default: whitespace)
            converter: Type function to apply to each value (default: None, no conversion)

        Returns:
            List of tuples, one per column

        Examples:
            >>> Input.from_string("1 2 3\\n4 5 6").as_columns()
            [('1', '4'), ('2', '5'), ('3', '6')]

            >>> Input.from_string("1 2 3\\n4 5 6").as_columns(converter=int)
            [(1, 4), (2, 5), (3, 6)]
        """
        lines = self.as_lines()
        if converter is None:
            rows = [line.split(separator) for line in lines]
        else:
            rows = [list(map(converter, line.split(separator))) for line in lines]
        return list(zip(*rows))

    def as_coords(self, separator: str = ",") -> list[Coord]:
        """
        Parse content as coordinates.

        Args:
            separator: Delimiter between row and col (default: ",")

        Returns:
            List of Coord objects

        Example:
            >>> Input.from_string("1,2\\n3,4\\n5,6").as_coords()
            [Coord(1, 2), Coord(3, 4), Coord(5, 6)]
        """
        return [
            Coord(int(row), int(col))
            for row, col in (line.split(separator) for line in self.as_lines())
        ]

    def as_adjacency_list(
        self, separator: str = "-", directed: bool = False
    ) -> dict[str, set[str]]:
        """
        Parse content as graph adjacency list.

        Args:
            separator: Delimiter between nodes (default: "-")
            directed: If False, create bidirectional edges (default: False)

        Returns:
            Dictionary mapping each node to set of connected nodes

        Example:
            >>> Input.from_string("A-B\\nB-C\\nA-C").as_adjacency_list()
            {'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'B', 'A'}}
        """
        graph = defaultdict(set)
        lines = self.as_lines()

        for line in lines:
            node1, node2 = line.split(separator)
            graph[node1].add(node2)
            if not directed:
                graph[node2].add(node1)

        return dict(graph)

    def as_delimited_lines(
        self, separator: str = ",", converter: type = int
    ) -> list[list]:
        """
        Parse each line as delimited values.

        Args:
            separator: Delimiter between values (default: ",")
            converter: Type function to apply to each value (default: int)

        Returns:
            List of lists, one per line with converted values

        Examples:
            Default usage (comma-separated integers):
            >>> input = Input.from_string("75,47,61\\n97,61,53\\n75,29")
            >>> input.as_delimited_lines()
            [[75, 47, 61], [97, 61, 53], [75, 29]]

            Custom separator:
            >>> input = Input.from_string("1;2;3\\n4;5;6")
            >>> input.as_delimited_lines(separator=";")
            [[1, 2, 3], [4, 5, 6]]

            String values:
            >>> input = Input.from_string("a,b,c\\nx,y,z")
            >>> input.as_delimited_lines(converter=str)
            [['a', 'b', 'c'], ['x', 'y', 'z']]

            Float values:
            >>> input = Input.from_string("1.5,2.7\\n3.2,4.8")
            >>> input.as_delimited_lines(converter=float)
            [[1.5, 2.7], [3.2, 4.8]]
        """
        return [
            [converter(v.strip()) for v in line.split(separator)]
            for line in self.parse(self._line_sep)
        ]

    def as_key_value_pairs(
        self,
        key_converter: type = int,
        value_parser=extract_ints,
        separator: str = ":",
    ) -> list[tuple]:
        """
        Parse lines with "key: value" format.

        Args:
            key_converter: Type function for key (default: int)
            value_parser: Function to parse value side (default: extract_ints)
            separator: Delimiter between key and value (default: ":")

        Returns:
            List of tuples: [(key, parsed_value), ...]

        Examples:
            Default usage (key as int, values as list of ints):
            >>> input = Input.from_string("190: 10 19\\n3267: 81 40 27")
            >>> input.as_key_value_pairs()
            [(190, [10, 19]), (3267, [81, 40, 27])]

            Custom value parser:
            >>> input = Input.from_string("test: hello world\\nfoo: bar baz")
            >>> input.as_key_value_pairs(key_converter=str, value_parser=str.split)
            [('test', ['hello', 'world']), ('foo', ['bar', 'baz'])]

            Single value per key:
            >>> input = Input.from_string("x: 42\\ny: 99")
            >>> input.as_key_value_pairs(value_parser=int)
            [('x', 42), ('y', 99)]
        """
        result = []
        for line in self.parse(self._line_sep):
            key_str, value_str = line.split(separator, 1)
            key = key_converter(key_str.strip())
            value = value_parser(value_str.strip())
            result.append((key, value))

        return result

    def as_sections(self, strip: bool = True) -> list["Input"]:
        """
        Split input into multiple sections separated by blank lines.

        Args:
            strip: Whether to strip whitespace from each section (default: True)

        Returns:
            List of Input instances, one for each section

        Examples:
            Two sections (unpack directly):
            >>> input = Input.from_string("section1\\ndata\\n\\nsection2\\nmore")
            >>> part1, part2 = input.as_sections()
            >>> part1.content
            'section1\\ndata'

            Three sections:
            >>> input = Input.from_string("sec1\\n\\nsec2\\n\\nsec3")
            >>> sections = input.as_sections()
            >>> [s.content for s in sections]
            ['sec1', 'sec2', 'sec3']

            With whitespace preservation:
            >>> input = Input.from_string("  a  \\n\\n  b  ")
            >>> sections = input.as_sections(strip=False)
            >>> sections[0].content
            '  a  '
        """
        parts = self.parse(self._section_sep, skip_empty=False)
        return [
            Input.from_string(
                s.strip() if strip else s, self._line_sep, self._section_sep, self._strip_content
            )
            for s in parts
        ]


__all__ = [
    "Input",
    "extract_ints",
    "extract_pattern",
    "pattern_to_bools",
    "extract_bracketed",
    "extract_parenthesized",
    "extract_braced",
    "parse",
]
