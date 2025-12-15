from aoc import read_data_as_lines, run, TestCase
from math import prod

SPEED_INCREASE_PER_MS = 1
STARTING_SPEED = 0


def parse_races(data_file):
    lines = read_data_as_lines(data_file)
    times = [int(x) for x in lines[0].split()[1:]]
    distances = [int(x) for x in lines[1].split()[1:]]
    return list(zip(times, distances))


def parse_single_race(data_file):
    lines = read_data_as_lines(data_file)
    time = int("".join(lines[0].split()[1:]))
    distance = int("".join(lines[1].split()[1:]))
    return time, distance


def count_ways_to_win(race_time, record_distance):
    ways = 0
    for hold_time in range(race_time + 1):
        travel_time = race_time - hold_time
        speed = STARTING_SPEED + (hold_time * SPEED_INCREASE_PER_MS)
        distance = speed * travel_time
        if distance > record_distance:
            ways += 1
    return ways


def count_winning_strategies(data_file):
    races = parse_races(data_file)
    return prod(count_ways_to_win(time, distance) for time, distance in races)


def count_winning_mega_race(data_file):
    race_time, record_distance = parse_single_race(data_file)
    return count_ways_to_win(race_time, record_distance)


if __name__ == "__main__":
    run(
        count_winning_strategies,
        [
            TestCase("06_example_01", 288),
            TestCase("06_puzzle_input", None),
        ],
    )

    run(
        count_winning_mega_race,
        [
            TestCase("06_example_01", 71503),
            TestCase("06_puzzle_input", None),
        ],
    )
