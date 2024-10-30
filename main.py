from filter import filter_words
from score import specify_score

CMD_GUESS = 'g'
CMD_HELP = 'h'
CMD_LIST = 'l'
CMD_QUIT = 'q'
CMD_UNDO_GUESS = 'u'

top_level_commands = [CMD_HELP, CMD_GUESS, CMD_LIST, CMD_QUIT, CMD_UNDO_GUESS]


class GuessResults:
    def __init__(self, guess, result, words):
        self.guess = guess
        self.result = result
        self.score = specify_score(result)
        self.words = filter_words(words, self.guess, self.score)
        self.word_count = len(self.words)


class GuessResultCollection:
    def __init__(self):
        self.goober = []
        self.guesses = self.goober

    def __iter__(self):
        return iter(self.guesses)

    def append(self, guess_results: GuessResults) -> None:
        self.guesses.append(guess_results)

    def pop(self) -> None:
        if not self.is_empty():
            self.guesses.pop(-1)

    def count(self) -> int:
        return len(self.guesses)

    def is_empty(self) -> bool:
        return len(self.guesses) == 0

    def words(self) -> list[str] | None:
        if self.is_empty():
            return None
        return self.guesses[-1].words


def main():
    secret_words = []
    with open("secret_words.csv", encoding="utf-8") as f:
        word = f.readline()
        while word:
            secret_words.append(word.strip())
            word = f.readline()

    for i, w in enumerate(secret_words):
        print(i + 1, w)

    guesses = GuessResultCollection()
    words = secret_words
    command = CMD_GUESS
    while True:
        if command == CMD_GUESS:
            while True:
                guess_results = record_guess(words)
                if not guess_results:
                    break
                guesses.append(guess_results)
                words = guess_results.words
                for i, w in enumerate(words):
                    print(i + 1, w)

        if command == CMD_LIST:
            list_guesses(guesses)

        if command == CMD_UNDO_GUESS:
            if guesses.is_empty():
                print("There are no guesses to undo.")
            else:
                guesses.pop()
                if guesses.is_empty():
                    words = secret_words
                    print("There are currently no guesses.")
                else:
                    words = guesses.words()
                    list_guesses(guesses)

        if command == CMD_QUIT:
            break

        if command == CMD_HELP:
            print(f"This program assumes you are playing Wordle. You type in the")
            print(f"  guess you made, followed by the result.")
            print(f"Create a result string with:")
            print(f"  'R' or 'r' for a character in the right position")
            print(f"  'W' or 'w' for a character in the wrong position")
            print(f"  any other character indicates the letter is not in the secret word.")
            print(f"Example: If guess was 'STUFF' and in the result the 'S' was in the ")
            print(f"  right position (green) and the 'U' was in the wrong position (yellow),")
            print(f"  and the rest of the letters were not in the secret word, the")
            print(f"  result string would be 'r-w--'.")
            print(f"Commands:")
            print(f"  {CMD_HELP} - Help. This text.")
            print(f"  {CMD_GUESS} - Guess. Stop guessing by typing in 'q'.")
            print(f"  {CMD_LIST} - List. List the guesses so far.")
            print(f"  {CMD_QUIT} - Quit the program.")
            print(f"  {CMD_UNDO_GUESS} - Undo the last guess.")

        command = input_command("Command: ")
    print('Goodbye')


def list_guesses(guesses):
    if guesses.is_empty():
        print("No guesses yet.")
    else:
        for i, guess_result in enumerate(guesses):
            n = i + 1
            print(f"{n} ----------------------------------")
            print(f"{n} guess : {guess_result.guess}")
            print(f"{n} result: {guess_result.result}")
            print(f"{n} count : {guess_result.word_count}")
            if guess_result.word_count <= 10:
                bunch = ""
                for word in guess_result.words:
                    bunch = bunch + word + " "
                print(f"All words: {bunch}")
            else:
                print(f"Lots of words.")
        print(f"------------------------------------")


def input_command(prompt):
    c = input(prompt)
    while c not in top_level_commands:
        print(f"Command must be one of: {top_level_commands}")
        c = input(prompt)
    return c


def input_len_5(prompt):
    s = input(prompt)
    while len(s) != 5:
        if s == "q":
            return s
        print("Input must be exactly 5 characters, or 'q'.")
        s = input(prompt)
    return s


def record_guess(words) -> GuessResults | None:
    guess = input_len_5("Input guess : ")
    if guess == "q":
        return None

    result = input_len_5("Input result: ")
    if result == "q":
        return None

    guess_results = GuessResults(guess, result, words)
    return guess_results


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

