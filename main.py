from filter import filter_words
from score import specify_score


class GuessResults:
    def __init__(self, guess, result, words):
        self.guess = guess
        self.score = specify_score(result)
        self.words = filter_words(words, self.guess, self.score)


def main():
    secret_words = []
    with open("secret_words.csv", encoding="utf-8") as f:
        word = f.readline()
        while word:
            secret_words.append(word.strip())
            word = f.readline()

    for i, w in enumerate(secret_words):
        print(i + 1, w)

    guesses = []
    words = secret_words
    for count in range(6):
        guess_results = record_guess(words)
        guesses.append(guess_results)
        words = guess_results.words
        for i, w in enumerate(words):
            print(i + 1, w)


def record_guess(words):
    guess = input("Input guess : ")
    result = input("Input result: ")
    guess_results = GuessResults(guess, result, words)
    return guess_results


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

