from score import RIGHT_POS, WRONG_POS, LESS_THAN
from score import score, letter_positions_of, no_similar_letters, set_results_for_one_letter


def test__aabbb__returns_a_0_1_b_2_3_4():
    word = 'aabbb'
    expect = {'a': [0, 1], 'b': [2, 3, 4]}
    result = letter_positions_of(word)
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
