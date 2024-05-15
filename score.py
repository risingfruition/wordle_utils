RIGHT_POS = 1
WRONG_POS = 2
LESS_THAN = 3


def score(guess: str, secret: str) -> list[int]:
    result = no_similar_letters()
    guess_positions = letter_positions_of(guess)
    secret_positions = letter_positions_of(secret)
    for c in guess_positions:
        if c in secret_positions:
            result = set_results_for_one_letter(guess_positions[c], secret_positions[c], result)
    return result


def no_similar_letters():
    return [LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN]


def letter_positions_of(word: str) -> dict:
    result = {}
    for i, c in enumerate(word):
        # AttributeError: 'NoneType' object has no attribute 'append'  result[c] = (result.get(c, list())).append(i)
        result[c] = result.get(c, list())  # does work if you separate the lines
        result[c].append(i)
    return result


def set_results_for_one_letter(guess: list[int], secret: list[int], result: list[int]):
    g = guess[:]
    s = secret[:]
    r = result[:]
    for position in guess:
        if position in s:
            r[position] = RIGHT_POS
            g.remove(position)
            s.remove(position)

    guess = g[:]
    for i, position in enumerate(guess):
        if len(secret) > i:
            r[position] = WRONG_POS

    return r
