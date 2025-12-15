from aoc import Input, run, TestCase, extract_ints


def parse_almanac(data_file):
    """Parse almanac into seeds and mapping stages."""
    sections = Input.from_file(f"./data/{data_file}").as_sections()

    seeds = extract_ints(sections[0].content)

    mapping_stages = []
    for section in sections[1:]:
        lines = section.content.strip().split("\n")
        rules = []
        for line in lines[1:]:
            dest_start, source_start, length = map(int, line.split())
            rules.append((dest_start, source_start, length))
        mapping_stages.append(rules)

    return seeds, mapping_stages


def apply_mapping(number, mapping_rules):
    """Apply mapping rules to a single number."""
    for dest_start, source_start, length in mapping_rules:
        if source_start <= number < source_start + length:
            offset = number - source_start
            return dest_start + offset
    return number


def apply_mapping_to_ranges(ranges, mapping_rules):
    """Apply mapping rules to ranges, returning list of resulting ranges."""
    result_ranges = []

    for start, length in ranges:
        end = start + length - 1
        unmapped = [(start, length)]

        for dest_start, source_start, rule_length in mapping_rules:
            source_end = source_start + rule_length - 1
            new_unmapped = []

            for unmap_start, unmap_length in unmapped:
                unmap_end = unmap_start + unmap_length - 1

                overlap_start = max(unmap_start, source_start)
                overlap_end = min(unmap_end, source_end)

                if overlap_start <= overlap_end:
                    offset = dest_start - source_start
                    mapped_start = overlap_start + offset
                    mapped_length = overlap_end - overlap_start + 1
                    result_ranges.append((mapped_start, mapped_length))

                    if unmap_start < overlap_start:
                        new_unmapped.append((unmap_start, overlap_start - unmap_start))
                    if overlap_end < unmap_end:
                        new_unmapped.append((overlap_end + 1, unmap_end - overlap_end))
                else:
                    new_unmapped.append((unmap_start, unmap_length))

            unmapped = new_unmapped

        result_ranges.extend(unmapped)

    return result_ranges


def find_lowest_location_individual(data_file):
    """Find lowest location for individual seeds."""
    seeds, mapping_stages = parse_almanac(data_file)

    locations = []
    for seed in seeds:
        value = seed
        for mapping_rules in mapping_stages:
            value = apply_mapping(value, mapping_rules)
        locations.append(value)

    return min(locations)


def find_lowest_location_ranges(data_file):
    """Find lowest location considering seed ranges."""
    seeds, mapping_stages = parse_almanac(data_file)

    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append((seeds[i], seeds[i + 1]))

    current_ranges = seed_ranges
    for mapping_rules in mapping_stages:
        current_ranges = apply_mapping_to_ranges(current_ranges, mapping_rules)

    return min(start for start, _ in current_ranges)


if __name__ == "__main__":
    run(
        find_lowest_location_individual,
        [
            TestCase("05_example_01", 35),
            TestCase("05_puzzle_input", 240320250),
        ],
    )

    run(
        find_lowest_location_ranges,
        [
            TestCase("05_example_01", 46),
            TestCase("05_puzzle_input", 28580589),
        ],
    )
