from aoc import Input, run, TestCase

DIGIT_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9",
}


def replace_words_with_digits(line):
    # Padded with word before and after since some digit words share letters
    # like: ...eigh(t)wo...
    for word, digit in DIGIT_WORDS.items():
        line = line.replace(word, word + digit + word)
    return line


def calibration_value(line):
    digits = [c for c in line if c.isdigit()]
    return int(digits[0] + digits[-1]) if digits else 0


def sum_basic_calibration(data_file):
    input_data = Input.from_file(f"./data/{data_file}")
    return sum(calibration_value(line) for line in input_data.as_lines())


def sum_full_calibration(data_file):
    input_data = Input.from_file(f"./data/{data_file}")
    lines = [replace_words_with_digits(line) for line in input_data.as_lines()]
    return sum(calibration_value(line) for line in lines)


if __name__ == "__main__":
    run(
        sum_basic_calibration,
        [
            TestCase("01_example_01", 142),
            TestCase("01_puzzle_input", 55538),
        ],
    )

    run(
        sum_full_calibration,
        [
            TestCase("01_example_02", 281),
            TestCase("01_puzzle_input", 54875),
        ],
    )
