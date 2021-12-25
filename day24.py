"""Day 24: finally, some assembly required"""
from day24_decompiled import (
    step_1,
    step_2,
    step_3,
    step_4,
    step_5,
    step_6,
    step_7,
    step_8,
    step_9,
    step_10,
    step_11,
    step_12,
    step_13,
    step_14,
)


def part_one() -> int:
    digits = list(range(1, 10))
    states_seen = {(1, step_1(0, 0, 0, 0, digit)): digit for digit in digits}
    for digits_so_far in range(1, 14):
        print(f"checking digit {digits_so_far + 1} ({len(states_seen)} overall)")
        next_func = {
            1: step_2,
            2: step_3,
            3: step_4,
            4: step_5,
            5: step_6,
            6: step_7,
            7: step_8,
            8: step_9,
            9: step_10,
            10: step_11,
            11: step_12,
            12: step_13,
            13: step_14,
        }[digits_so_far]
        for (digits_seen, (w, x, y, z)), best_result in list(states_seen.items()):
            for next_digit in digits[:]:
                if digits_seen + 1 < digits_so_far:
                    try:
                        del states_seen[digits_seen, (w, x, y, z)]
                    except KeyError:
                        pass
                if digits_seen != digits_so_far:
                    continue
                next_result = next_func(w, x, y, z, next_digit=next_digit)
                dict_key = digits_seen + 1, next_result
                new_digits = best_result * 10 + next_digit
                try:
                    prev_best = states_seen[dict_key]
                except KeyError:
                    states_seen[dict_key] = new_digits
                else:
                    if new_digits > prev_best:
                        states_seen[dict_key] = new_digits
    candidates = (
        val
        for (digits_seen, (_, _, _, z)), val in states_seen.items()
        if digits_seen == 14 and not z
    )
    return max(candidates)


def part_two() -> int:
    digits = list(range(1, 10))
    states_seen = {(1, step_1(0, 0, 0, 0, digit)): digit for digit in digits}
    for digits_so_far in range(1, 14):
        print(f"checking digit {digits_so_far + 1} ({len(states_seen)} overall)")
        next_func = {
            1: step_2,
            2: step_3,
            3: step_4,
            4: step_5,
            5: step_6,
            6: step_7,
            7: step_8,
            8: step_9,
            9: step_10,
            10: step_11,
            11: step_12,
            12: step_13,
            13: step_14,
        }[digits_so_far]
        for (digits_seen, (w, x, y, z)), best_result in list(states_seen.items()):
            for next_digit in digits[:]:
                if digits_seen + 1 < digits_so_far:
                    try:
                        del states_seen[digits_seen, (w, x, y, z)]
                    except KeyError:
                        pass
                if digits_seen != digits_so_far:
                    continue
                next_result = next_func(w, x, y, z, next_digit=next_digit)
                dict_key = digits_seen + 1, next_result
                new_digits = best_result * 10 + next_digit
                try:
                    prev_best = states_seen[dict_key]
                except KeyError:
                    states_seen[dict_key] = new_digits
                else:
                    if new_digits < prev_best:
                        states_seen[dict_key] = new_digits
    candidates = (
        val
        for (digits_seen, (_, _, _, z)), val in states_seen.items()
        if digits_seen == 14 and not z
    )
    return min(candidates)


def main():
    print(part_one())
    print(part_two())

if __name__ == "__main__":
    main()
