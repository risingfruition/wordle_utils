RIGHT_POS = 1
WRONG_POS = 2
LESS_THAN = 3


def score(guess: str, secret: str) -> list[int]:
    result = no_similar_letters()
    guess_positions = positions_of_letter_from(guess)
    secret_positions = positions_of_letter_from(secret)
    for c in guess_positions:
        if c in secret_positions:
            result = set_results_for_one_letter(guess_positions[c], secret_positions[c], result)
    return result


def no_similar_letters():
    return [LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN]


def positions_of_letter_from(word: str) -> dict:
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


def test__aabbb__returns_a_0_1_b_2_3_4():
    word = 'aabbb'
    expect = {'a': [0, 1], 'b': [2, 3, 4]}
    result = positions_of_letter_from(word)
    assert result == expect


class TestSetResultsForOneLetter:
    def test__one_wrong_pos__adds_wrong_pos_in_correct_spot(self):
        guess_position = 4
        guess = [guess_position]
        secret_position = 3
        secret = [secret_position]
        initial_result = no_similar_letters()
        result = set_results_for_one_letter(guess, secret, initial_result)
        assert guess_position != secret_position
        assert result[guess_position] == WRONG_POS

    def test__one_right_pos__adds_right_pos_in_correct_spot(self):
        guess_position = 3
        guess = [guess_position]
        secret_position = guess_position  # because the letter is in the correct position
        secret = [secret_position]
        initial_result = no_similar_letters()
        result = set_results_for_one_letter(guess, secret, initial_result)
        assert result[guess_position] == RIGHT_POS


class TestScore:
    def test__more_of_a_letter_in_guess__extra_letters_get_less_than(self):
        guess_ = 'mommy'  # one more 'm' in guess than in secret.
        secret = '-m--m'  # no RIGHT_POS 'm's in secret.
        wrong_pos_1_position = 0
        wrong_pos_2_position = 2
        less_than_position = 3
        expect = no_similar_letters()
        expect[wrong_pos_1_position] = WRONG_POS
        expect[wrong_pos_2_position] = WRONG_POS
        expect[less_than_position] = LESS_THAN
        result = score(guess_, secret)
        assert result == expect

    def test__guess_matches_secret__returns_right_pos(self):
        guess = 'abcde'
        secret = guess
        expect = [RIGHT_POS, RIGHT_POS, RIGHT_POS, RIGHT_POS, RIGHT_POS]
        result = score(guess, secret)
        assert result == expect

    def test__no_common_letters__returns_less_than(self):
        guess = 'abcde'
        secret = 'lmnop'
        expect = [LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN]
        result = score(guess, secret)
        assert result == expect
