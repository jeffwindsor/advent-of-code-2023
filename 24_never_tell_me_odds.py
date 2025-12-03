from aoc import Input, extract_ints, run, TestCase
from z3 import Solver, Int, sat

# Puzzle constants
TEST_AREA_MIN_EXAMPLE = 7
TEST_AREA_MAX_EXAMPLE = 27
TEST_AREA_MIN_ACTUAL = 200000000000000
TEST_AREA_MAX_ACTUAL = 400000000000000


def parse_data(data_file):
    input_data = Input.from_file(f"./data/{data_file}")
    hailstones = []

    for line in input_data.as_lines():
        values = extract_ints(line)
        if len(values) == 6:
            hailstones.append(tuple(values))

    return hailstones


def find_2d_intersection(h1, h2):
    """Find where two hailstone paths intersect in 2D (X, Y only).

    Args:
        h1: First hailstone (px, py, pz, vx, vy, vz)
        h2: Second hailstone (px, py, pz, vx, vy, vz)

    Returns:
        Tuple (x, y, t1, t2) if intersection exists, None if parallel
        t1, t2 are the times when each hailstone reaches the intersection
    """
    x1, y1, _, vx1, vy1, _ = h1
    x2, y2, _, vx2, vy2, _ = h2

    # Calculate determinant to check if lines are parallel
    determinant = vx2 * vy1 - vx1 * vy2

    if determinant == 0:
        # Lines are parallel
        return None

    # Solve for t1 and t2 using Cramer's rule
    dx = x2 - x1
    dy = y2 - y1

    t1 = (vx2 * dy - vy2 * dx) / determinant
    t2 = (vx1 * dy - vy1 * dx) / determinant

    # Calculate intersection point
    x = x1 + t1 * vx1
    y = y1 + t1 * vy1

    return (x, y, t1, t2)


def count_future_intersections_in_area(data_file, area_min, area_max):
    """Count hailstone path intersections within the test area in the future.

    Args:
        data_file: Path to input data
        area_min: Minimum coordinate value for test area
        area_max: Maximum coordinate value for test area

    Returns:
        Number of intersections within the test area
    """
    hailstones = parse_data(data_file)
    count = 0

    # Check all pairs of hailstones
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            result = find_2d_intersection(hailstones[i], hailstones[j])

            if result is None:
                # Parallel lines
                continue

            x, y, t1, t2 = result

            # Check if intersection is in the future for both hailstones
            if t1 < 0 or t2 < 0:
                continue

            # Check if intersection is within test area
            if area_min <= x <= area_max and area_min <= y <= area_max:
                count += 1

    return count


def predict_hail_collisions_example(data_file):
    """Count future path intersections in the example test area (7 to 27)."""
    return count_future_intersections_in_area(
        data_file, TEST_AREA_MIN_EXAMPLE, TEST_AREA_MAX_EXAMPLE
    )


def predict_hail_collisions_actual(data_file):
    """Count future path intersections in the actual test area (200T to 400T)."""
    return count_future_intersections_in_area(
        data_file, TEST_AREA_MIN_ACTUAL, TEST_AREA_MAX_ACTUAL
    )


def throw_magic_rock(data_file):
    """Find the initial position to throw a rock that hits all hailstones.

    Uses Z3 constraint solver to find rock position (rx, ry, rz) and velocity
    (rvx, rvy, rvz) such that the rock collides with every hailstone.

    For each hailstone collision at time t_i:
        rx + rvx * t_i = px_i + vx_i * t_i
        ry + rvy * t_i = py_i + vy_i * t_i
        rz + rvz * t_i = pz_i + vz_i * t_i

    Returns:
        Sum of initial rock coordinates (rx + ry + rz)
    """
    hailstones = parse_data(data_file)

    # Create integer variables for rock position and velocity
    rx, ry, rz = Int('rx'), Int('ry'), Int('rz')
    rvx, rvy, rvz = Int('rvx'), Int('rvy'), Int('rvz')

    solver = Solver()

    # Use first few hailstones to constrain the problem
    # 3 is minimum for unique solution, but use more for robustness
    num_hailstones = min(5, len(hailstones))

    for i in range(num_hailstones):
        px, py, pz, vx, vy, vz = hailstones[i]

        # Create a time variable for collision with this hailstone
        t = Int(f't{i}')
        solver.add(t >= 0)

        # Add collision constraints for all three axes
        solver.add(rx + rvx * t == px + vx * t)
        solver.add(ry + rvy * t == py + vy * t)
        solver.add(rz + rvz * t == pz + vz * t)

    if solver.check() == sat:
        model = solver.model()
        rock_x = model[rx].as_long()
        rock_y = model[ry].as_long()
        rock_z = model[rz].as_long()

        return rock_x + rock_y + rock_z
    else:
        return None


if __name__ == "__main__":
    # Part 1: Example test area (7 to 27)
    run(
        predict_hail_collisions_example,
        [
            TestCase("24_example_01", 2),
        ],
    )

    # Part 1: Actual test area (200000000000000 to 400000000000000)
    run(
        predict_hail_collisions_actual,
        [
            TestCase("24_puzzle_input", 13965),
        ],
    )

    # Part 2: Find rock trajectory that hits all hailstones
    run(
        throw_magic_rock,
        [
            TestCase("24_example_01", 47),
            TestCase("24_puzzle_input", None),
        ],
    )
