from aoc import read_data_as_lines, run, TestCase
from collections import defaultdict

INITIAL_POINTS = 1
POINT_MULTIPLIER = 2

def parse_card(line):
    card_part, numbers_part = line.split(': ')
    card_id = int(card_part.split()[1])
    winning_part, your_part = numbers_part.split(' | ')
    winning = set(int(n) for n in winning_part.split())
    your_numbers = set(int(n) for n in your_part.split())
    return card_id, winning, your_numbers

def count_matches(winning, your_numbers):
    return len(winning & your_numbers)

def calculate_card_points(matches):
    if matches == 0:
        return 0
    return INITIAL_POINTS * (POINT_MULTIPLIER ** (matches - 1))

def calculate_scratchcard_points(data_file):
    lines = read_data_as_lines(data_file)
    total_points = 0

    for line in lines:
        _, winning, your_numbers = parse_card(line)
        matches = count_matches(winning, your_numbers)
        total_points += calculate_card_points(matches)

    return total_points

def count_cascading_scratchcards(data_file):
    lines = read_data_as_lines(data_file)
    card_copies = defaultdict(int)

    for line in lines:
        card_id, winning, your_numbers = parse_card(line)
        card_copies[card_id] += 1

        matches = count_matches(winning, your_numbers)

        current_copies = card_copies[card_id]
        for next_card in range(card_id + 1, card_id + matches + 1):
            card_copies[next_card] += current_copies

    return sum(card_copies.values())

if __name__ == "__main__":
    run(
        calculate_scratchcard_points,
        [
            TestCase("04_example_01", 13),
            TestCase("04_puzzle_input", 22488),
        ],
    )

    run(
        count_cascading_scratchcards,
        [
            TestCase("04_example_01", 30),
            TestCase("04_puzzle_input", 7013204),
        ],
    )
