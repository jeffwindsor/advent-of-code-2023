# Advent of Code 2023 - Project Preferences

This file contains project-specific workflows and preferences for Claude Code assistance.

## Puzzle Setup Workflow

When user provides a puzzle description, follow these steps:

### Step 1: Create Files
1. **Python file**: `{day:02d}_{puzzle_name}.py`
   - Example: `22_monkey_market.py`

2. **Example data**: `data/{day:02d}_example_{counter:02d}`
   - Use underscore before counter: `data/22_example_01`, `data/22_example_02`
   - Extract example inputs from puzzle description

3. **Puzzle input**: `data/{day:02d}_puzzle_input`
   - Create placeholder, user will fill from AoC website

### Step 2: Python File Structure
```python
from aoc import read_data_as_lines, run, TestCase
from collections import defaultdict  # or other needed imports

# Puzzle constants (extract all magic numbers)
CONSTANT_NAME = value

def parse_data(data_file):
    """Parse the input data."""
    lines = read_data_as_lines(data_file)
    # parsing logic
    return parsed_data

def {descriptive_name}_part1(data_file):
    """Descriptive docstring for part 1."""
    # implementation
    pass

def {descriptive_name}_part2(data_file):
    """Descriptive docstring for part 2."""
    # implementation
    pass

if __name__ == "__main__":
    run(
        {descriptive_name}_part1,
        [
            TestCase("{day}_example_01", expected_value),
            TestCase("{day}_puzzle_input", None),
        ],
    )

    run(
        {descriptive_name}_part2,
        [
            TestCase("{day}_example_01", expected_value),
            TestCase("{day}_puzzle_input", None),
        ],
    )
```

### Step 3: Part 2 Updates
When part 2 description arrives:
1. Add new example file if needed: `data/{day}_example_02`
2. Implement part2 function
3. Uncomment/update test cases

## Code Style Preferences

### 1. Function Naming
- **DO NOT** use generic `part1` and `part2`
- **USE** fun, thematic names based on puzzle narrative
- Examples:
  - Day 22: `sum_final_secrets` and `maximize_banana_profit`
  - Should be memorable and relate to puzzle theme

### 2. Magic Numbers
- **Extract ALL magic numbers** as named constants at top of file
- Group logically with comments
- Example:
  ```python
  # Puzzle constants
  PRUNE_MODULO = 16777216  # 2^24
  SECRET_MULTIPLY_1 = 64
  ITERATIONS = 2000
  SEQUENCE_LENGTH = 4
  ```

### 3. Readability Best Practices
- Use `defaultdict` instead of manual dict initialization
- Extract complex nested logic into helper functions
- Descriptive parameter names (`initial_secret` not `initial`, `iterations` not `n`)
- Enhanced docstrings with return type documentation
- Business context in docstrings (explain the "why")

### 4. Code Organization
- Helper functions above the main part1/part2 functions
- Clear separation of concerns
- Stream processing over intermediate lists when possible

## Testing
- Always verify tests pass after changes: `python {day}_{puzzle_name}.py`
- Example format: `data/{day}_example_01` with expected answers from description
- Puzzle input: User provides from AoC website

## File Naming Pattern Examples
```
01_historian_hysteria.py
data/01_example
data/01_puzzle_input

22_monkey_market.py
data/22_example_01
data/22_example_02
data/22_puzzle_input
```

## Summary
- Fun thematic function names (not part1/part2)
- Extract magic numbers as constants
- Clear, readable, well-documented code
- Follow existing aoc.py utilities pattern
- no doc comments
- functional, pythonic, readable, understandable