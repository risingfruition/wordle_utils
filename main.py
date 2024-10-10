from filter import filter_words
from score import specify_score


class Helper:
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

    words = secret_words
    for count in range(6):
        guess = input("Input guess : ")
        result = input("Input result: ")
        helper = Helper(guess, result, words)
        words = helper.words
        for i, w in enumerate(words):
            print(i + 1, w)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

