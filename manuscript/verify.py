import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def encode(letters, multiplier):
    return [digit for letter in letters for digit in (multiplier * letter, letter)]


def stage_words(multiplier, first, second, last_stage):
    stages = [[multiplier * first, first]]
    for index in range(last_stage):
        previous = stages[-1]
        stages.append(previous * (index + 2) + [multiplier * second, second] * (index + 1) + previous * (index + 2))
    return stages


def rational_value(word):
    value = Fraction(word[-1])
    for digit in reversed(word[:-1]):
        value = digit + 1 / value
    return value


def qualifying_lengths(word, multiplier, rational_limit):
    top_left, top_right, bottom_left, bottom_right = 1, 0, 0, 1
    lengths = []
    compared = 0
    for length, digit in enumerate(word, 1):
        top_left, top_right, bottom_left, bottom_right = (
            top_left * digit + top_right,
            top_left,
            bottom_left * digit + bottom_right,
            bottom_left,
        )
        qualifies = top_right == multiplier * bottom_left
        assert top_left * bottom_right - top_right * bottom_left == (-1) ** length
        if length <= rational_limit:
            prefix = word[:length]
            forward = rational_value(prefix)
            backward = rational_value(prefix[::-1])
            assert (forward == multiplier * backward) == qualifies
            assert forward == Fraction(top_left, bottom_left)
            compared += 1
        if qualifies:
            lengths.append(length)
    return lengths, compared


def palindrome_lengths(letters):
    return [length for length in range(1, len(letters) + 1) if letters[:length] == letters[:length][::-1]]


def expected_block_lengths(letters, multiplier):
    expected = [2 * length for length in palindrome_lengths(letters)]
    if multiplier == 1:
        initial_run = next((index for index, letter in enumerate(letters) if letter != letters[0]), len(letters))
        expected.extend(range(1, 2 * initial_run, 2))
    return sorted(expected)


def fibonacci_letters(length):
    letters = 'a'
    while len(letters) < length:
        letters = ''.join('ab' if letter == 'a' else 'a' for letter in letters)
    return letters[:length]


def run_checks():
    construction = []
    rational_comparisons = 0
    for multiplier in [1, 2, 3, 5, 11]:
        for first, second in [(1, 2), (2, 1), (2, 3), (5, 1)]:
            stages = stage_words(multiplier, first, second, 4)
            assert [len(word) for word in stages] == [2, 10, 64, 518, 5188]
            rational_limit = 518 if (first, second) == (2, 3) else 128
            lengths, compared = qualifying_lengths(stages[-1], multiplier, rational_limit)
            rational_comparisons += compared
            qualifying = set(lengths)
            clusters = []
            for index, word in enumerate(stages[:-1]):
                stage_length = len(word)
                assert stages[index + 1][:stage_length] == word
                cluster = [power * stage_length for power in range(1, index + 3)]
                assert all(length in qualifying for length in cluster)
                start = (index + 2) * stage_length
                end = start + 2 * (index + 1)
                assert stages[index + 1][start:end] == [multiplier * second, second] * (index + 1)
                assert stages[index + 1][end] == multiplier * first
                clusters.append({'k': index, 'L_k': stage_length, 'qualifying_cluster': cluster})
            construction.append({'m': multiplier, 'r': first, 's': second, 'prefix_length': len(stages[-1]), 'qualifying_lengths': lengths, 'clusters': clusters})
    letters = fibonacci_letters(1000)
    palindromes = palindrome_lengths(letters)
    fibonacci_numbers = [0, 1]
    while fibonacci_numbers[-1] - 2 <= len(letters):
        fibonacci_numbers.append(sum(fibonacci_numbers[-2:]))
    assert palindromes == [value - 2 for value in fibonacci_numbers if 0 < value - 2 <= len(letters)]
    fibonacci_results = []
    for multiplier in [1, 2, 3, 5, 11]:
        for first, second in product([1, 2, 3, 5], repeat=2):
            if first == second:
                continue
            numeric_letters = [first if letter == 'a' else second for letter in letters]
            word = encode(numeric_letters, multiplier)
            lengths, compared = qualifying_lengths(word, multiplier, 64)
            rational_comparisons += compared
            assert lengths == expected_block_lengths(numeric_letters, multiplier)
            assert lengths == ([1] if multiplier == 1 else []) + [2 * length for length in palindromes]
            fibonacci_results.append({'m': multiplier, 'r': first, 's': second, 'prefix_length': len(word), 'qualifying_lengths': lengths})
    block_cases = 0
    block_prefixes = 0
    for length in range(1, 7):
        for block_word in product([1, 2, 3], repeat=length):
            for multiplier in [1, 2, 3, 5]:
                word = encode(block_word, multiplier)
                lengths, compared = qualifying_lengths(word, multiplier, len(word))
                rational_comparisons += compared
                assert lengths == expected_block_lengths(block_word, multiplier)
                block_cases += 1
                block_prefixes += len(word)
    stage_lengths = [2]
    for index in range(80):
        stage_lengths.append(2 * (index + 2) * stage_lengths[-1] + 2 * (index + 1))
    repetition_cases = 0
    for exponent in range(2, 9):
        for index in range(2 * exponent - 2, 80):
            roots = (index + 2) // exponent
            assert roots >= 1
            assert exponent * roots <= index + 2
            assert Fraction(stage_lengths[index + 1], roots * stage_lengths[index]) <= 6 * exponent
            repetition_cases += 1
    return {
        'arithmetic': 'Exact integers and rational fractions; no rounding.',
        'construction': construction,
        'fibonacci': fibonacci_results,
        'block_code': {'alphabet': [1, 2, 3], 'block_lengths': [1, 6], 'multipliers': [1, 2, 3, 5], 'words_checked': block_cases, 'prefixes_checked': block_prefixes},
        'repetition_bounds': {'integer_exponents': [2, 8], 'stages_through': 80, 'comparisons': repetition_cases, 'growth_bound': '6 * integer_exponent'},
        'totals': {'construction_prefixes': sum(row['prefix_length'] for row in construction), 'fibonacci_prefixes': sum(row['prefix_length'] for row in fibonacci_results), 'block_prefixes': block_prefixes, 'rational_prefix_comparisons': rational_comparisons},
        'coverage': 'Finite qualifying-prefix enumeration, determinants, rational equivalence, block-code parity, repetition clusters, Fibonacci prefixes and root-length bounds.',
        'infinite_statements': 'Theorems and corollaries have written proofs in note.tex.',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    result = json.dumps(run_checks(), indent=2) + '\n'
    if arguments.output:
        arguments.output.write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
