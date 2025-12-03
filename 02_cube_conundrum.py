from aoc import Input, extract_ints, run, TestCase
from functools import reduce

BAG_CONTENTS = {'red': 12, 'green': 13, 'blue': 14}


def parse_game(line):
    game_part, reveals_part = line.split(':', 1)
    game_id = extract_ints(game_part)[0]
    reveals = reveals_part.split(';')
    return game_id, [parse_reveal(r) for r in reveals]


def parse_reveal(reveal):
    cubes = {}
    for cube in reveal.split(','):
        parts = cube.strip().split()
        count = extract_ints(parts[0])[0]
        color = parts[1]
        cubes[color] = count
    return cubes


def max_cubes_needed(reveals):
    maxes = {'red': 0, 'green': 0, 'blue': 0}
    for reveal in reveals:
        for color, count in reveal.items():
            maxes[color] = max(maxes[color], count)
    return maxes


def is_game_possible(reveals):
    needed = max_cubes_needed(reveals)
    return all(needed[color] <= BAG_CONTENTS[color] for color in BAG_CONTENTS)


def cube_power(cubes):
    return reduce(lambda a, b: a * b, cubes.values())


def sum_possible_game_ids(data_file):
    input_data = Input.from_file(f"./data/{data_file}")
    games = [parse_game(line) for line in input_data.as_lines()]
    return sum(game_id for game_id, reveals in games if is_game_possible(reveals))


def sum_minimum_cube_powers(data_file):
    input_data = Input.from_file(f"./data/{data_file}")
    games = [parse_game(line) for line in input_data.as_lines()]
    return sum(cube_power(max_cubes_needed(reveals)) for _, reveals in games)


if __name__ == "__main__":
    run(
        sum_possible_game_ids,
        [
            TestCase("02_example_01", 8),
            TestCase("02_puzzle_input", 2149),
        ],
    )

    run(
        sum_minimum_cube_powers,
        [
            TestCase("02_example_01", 2286),
            TestCase("02_puzzle_input", 71274),
        ],
    )
