
RIGHT_POS = 1
WRONG_POS = 2
LESS_THAN = 3


def score(guess: str, secret: str) -> list[int]:
    return [LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN]


def test__no_common_letters__returns_less_than():
    guess = 'abcde'
    secret = 'lmnop'
    expect = [LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN, LESS_THAN]
    result = score(guess, secret)
    assert result == expect
