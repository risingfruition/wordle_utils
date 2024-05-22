from filter import filter_words
from score import specify_score


class TestFilterWords:
    def test__wrong_pos__word_has_guess_letter_at_pos__deletes_word(self):
        guess = "zzznz"
        score = specify_score('---W-')

        # Keep words with 'n' but not in the same position as the word "wrong".
        words = ["snail", "xthis", "wrong", "bring", "talon"]
        expect = ["snail", "talon"]
        result = filter_words(words, guess, score)
        assert result == expect

    def test__right_pos__word_has_guess_letter_in_right_pos__keeps_word(self):
        guess = 'omooo'
        result = specify_score('-R---')
        words = ['small', 'giant', 'amuck']
        expect = ['small', 'amuck']

        assert filter_words(words, guess, result) == expect

    def test__no_similar_letters__word_has_any_guess_letter_in_any_pos__deletes_word(self):
        guess = 'aeiou'
        result = specify_score('FFFFF')
        words = ['small', 'glyph', 'amuck']
        expect = ['glyph']

        assert filter_words(words, guess, result) == expect

    def test__secret_word_has_n__guess_has_more__keep_words_with_n(self):
        guess = 'mommy'
        result = specify_score('R-W--')
        words = [
            'madam',  # 2 ms, one at 0 and another not at 2. Keep
            'mince',  # 1 m at 0. Delete not enough ms.
            'harem',  # Not 1 m at 0. Delete.
            'lambs',  # 1 m at 2. Delete.
            'mmama'   # Too many ms.
        ]
        expect = ['madam']

        assert filter_words(words, guess, result) == expect

    def test__secret_word_has_n__guess_has_n__keep_words_with_n(self):
        guess = 'skill'
        result = specify_score('---WW')
        words = ['llama', 'lofty', 'level']
        expect = ['llama']

        assert filter_words(words, guess, result) == expect
