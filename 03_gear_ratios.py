from aoc import read_data_as_lines, run, TestCase

GEAR_SYMBOL = '*'
EMPTY_SPACE = '.'
REQUIRED_ADJACENT_PARTS = 2

def parse_data(data_file):
    lines = read_data_as_lines(data_file)
    return [list(line) for line in lines]

def neighbors(row, col, rows, cols):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield (nr, nc)

def is_symbol(char):
    return char != EMPTY_SPACE and not char.isdigit()

def find_numbers(grid):
    rows, cols = len(grid), len(grid[0])
    numbers = []

    for row in range(rows):
        col = 0
        while col < cols:
            if grid[row][col].isdigit():
                num_str = ''
                positions = set()

                while col < cols and grid[row][col].isdigit():
                    num_str += grid[row][col]
                    positions.add((row, col))
                    col += 1

                numbers.append((int(num_str), positions))
            else:
                col += 1

    return numbers

def is_adjacent_to_symbol(positions, grid):
    rows, cols = len(grid), len(grid[0])
    return any(
        is_symbol(grid[nr][nc])
        for row, col in positions
        for nr, nc in neighbors(row, col, rows, cols)
    )

def sum_engine_parts(data_file):
    grid = parse_data(data_file)
    numbers = find_numbers(grid)

    return sum(
        number
        for number, positions in numbers
        if is_adjacent_to_symbol(positions, grid)
    )

def find_gears(grid):
    return [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[0]))
        if grid[row][col] == GEAR_SYMBOL
    ]

def adjacent_numbers(gear_pos, numbers, grid):
    rows, cols = len(grid), len(grid[0])
    gear_neighbors = set(neighbors(gear_pos[0], gear_pos[1], rows, cols))

    return [
        number
        for number, positions in numbers
        if any(pos in gear_neighbors for pos in positions)
    ]

def sum_gear_ratios(data_file):
    grid = parse_data(data_file)
    numbers = find_numbers(grid)
    gears = find_gears(grid)

    return sum(
        adjacent[0] * adjacent[1]
        for gear_pos in gears
        if len(adjacent := adjacent_numbers(gear_pos, numbers, grid)) == REQUIRED_ADJACENT_PARTS
    )

if __name__ == "__main__":
    run(
        sum_engine_parts,
        [
            TestCase("03_example_01", 4361),
            TestCase("03_puzzle_input", None),
        ],
    )

    run(
        sum_gear_ratios,
        [
            TestCase("03_example_01", 467835),
            TestCase("03_puzzle_input", None),
        ],
    )
