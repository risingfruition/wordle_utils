from functools import partial


# Data is ordered by the value of these constants. Do not change their values.
RIGHT_POS = 1
WRONG_POS = RIGHT_POS + 1
FEWER_THAN = WRONG_POS + 1


def filter_words(words: list[str], guess: str, score: list[int]) -> list[str]:
    filters = []
    sorted_scores = sort_scores(guess, score)
    for c in sorted_scores:
        filters.extend(filters_for_letter(c, sorted_scores[c]))
    result = do_filtering(words, filters)

    return result


def filters_for_letter(char: str, score_data: list) -> list:
    result = []
    exactly = 0
    at_least = 0
    for i, score_pos in enumerate(score_data):
        if score_pos[0] == RIGHT_POS:
            result.append(partial(has_letter_at, char, score_pos[1]))
            exactly += 1
            continue
        if score_pos[0] == WRONG_POS:
            result.append(partial(has_letter_not_at, char, score_pos[1]))
            exactly += 1
            continue
        if score_pos[0] == FEWER_THAN:
            if i == 0:
                result.append(partial(has_no_letter, char))
                at_least = exactly
                exactly = 0
            else:
                # 'exactly' contains the count of current letter
                # in the secret word. Lines after the 'for' will
                # add a filter for exactly that many letters.
                pass
            continue
    if exactly > 0:
        result.append(partial(has_exactly_n, char, exactly))
    else:
        result.append(partial(has_at_least_n, char, at_least))
    return result


def partial_has_no_letter(char: str):
    return partial(has_no_letter, char)


def partial_has_letter_at_pos(letter, pos):
    return partial(has_letter_at, letter, pos)


def partial_has_letter_not_at_pos(letter, pos):
    return partial(has_letter_not_at, letter, pos)


def sort_scores(guess: str, score: list[int]) -> dict:
    d = {}
    for i, c in enumerate(guess):
        d[c] = d.get(c, list())
        d[c].append((score[i], i))
    for k in d:
        d[k].sort()
    return d


def do_filtering(words, filters):
    result = []
    for w in words:
        if should_keep_word(w, filters):
            result.append(w)
    return result


def should_keep_word(word, filters):
    for f in filters:
        if not f(word):
            return False
    return True


def has_letter(letter, word):
    return letter in word


def has_no_letter(letter, word):
    return not has_letter(letter, word)


def has_letter_at(letter, position, word):
    return word[position] == letter


def has_letter_not_at(letter, position, word):
    return letter in word and word[position] != letter


def has_exactly_n(letter, n, word):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count == n


def has_at_least_n(letter, n, word):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count >= n


def has_fewer_than_n(letter, n, word):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count < n
