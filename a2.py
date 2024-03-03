import random
from random import choice
from collections.abc import MutableSet


class WordleWords(MutableSet):
    """A class to manage a set of words for a Wordle game."""

    def __init__(self, letters):
        ''' Initialize WordleWords with a specified length of letters '''
        self._words = set()
        self.length = letters

    def __contains__(self, word):
        """ Check if a word is present in the WordleWords set """
        return word in self._words

    def __iter__(self):
        # returns an iterator over all the words in the set
        return iter(self._words)

    def __len__(self):
        # returns the number of words in the set
        return len(self._words)

    def __str__(self):
        # returns a string describing the object and what it contains
        return f"This is a wordleWords object with {len(self._words)} words."

    def add(self, word):
        """ adds a word to the set Raises an error if theword is too short, or too long, or does not contain only
          letters
          """
        if not word.isalpha():
            raise NotLettersError('Word contains non-letter characters')

        if len(word) < self.length:
            raise TooShortError('Word is too short')

        if len(word) > self.length:
            raise TooLongError('Word is too long')

        # If the word passes all checks, add it to the set of words
        self._words.add(word.upper())

    def discard(self, word):
        # removes words from the set
        self._words.discard(word)

    def load_file(self, filename):
        """ opens a file and reads the content of the file, and then it adds the contents to the set  """
        try:
            with open(filename, 'r') as file:
                for line in file:
                    word = line.strip().upper()
                    if len(word) == self.length:
                        self._words.add(word)


        except FileNotFoundError:
            print(f"File {filename} not found.")
        pass

    def check_word(self, word):
        """ checks if the length of the word meets the set parameter and if not returns an appropriate error for the
        unmet condition
        """

        if len(word) < self.length:
            raise TooShortError('word is too short ')

        if len(word) > self.length:
            raise TooLongError('word is too long ')

        if not word.isalpha():
            raise NotLettersError('word not in letters')

        return True

    def letters(self):
        """Returns the number of letters in words."""
        return self.length

    def copy(self):
        # Returns a second WordleWords instance that contains the same words.
        return self._words.copy()


class Guess:
    """ this class represents a single guess in the wordle game"""
    def __init__(self, guess, answer):
        # Initialize a Guess object with a guessed word and the correct answer
        self.guess_1 = guess
        self.answer = answer

    def guess(self):
        # returns the guessed word
        return self.guess_1

    def correct(self):
        """ this function iterates through the guessed words and compares it to the answer and returns a string of
        correct letters in the guessed word
        """
        correctLetters = ''

        for i in range(len(self.answer)):

            if self.answer[i] == self.guess_1[i]:

                correctLetters += self.answer[i]
            else:

                correctLetters += '_'

        return str(correctLetters)

    def misplaced(self):
        """ this function iterates through the guessed words and compares it to the answer and returns a string of
                misplaced letters in the guessed word
                """
        misplacedLetters = ''
        answerDict = []
        for i in self.answer:
            answerDict.append(i)

        for i in range(len(self.answer)):
            if self.guess_1[i] == self.answer[i] and self.guess_1[i] in self.answer and self.guess_1[i] in answerDict:
                answerDict.remove(self.guess_1[i])

            elif self.guess_1[i] in answerDict:
                misplacedLetters += self.guess_1[i]
                answerDict.remove(self.guess_1[i])

        return misplacedLetters

    def wrong(self):
        """
         this function calls the correct and misplaced function in order to find and return the letters that are wrong

         """
        wrongLetters = ''
        correctLetter = self.correct()
        misplacedLetter = self.misplaced()

        for i in self.guess_1:
            if i not in correctLetter:
                wrongLetters += i
            correctLetter = correctLetter.replace(i, '_', 1)
            if i in misplacedLetter:
                wrongLetters = wrongLetters.replace(i, '')

        return ''.join(sorted(wrongLetters))

    def is_win(self):
        # returns true if the guess is the same as the answer and false otherwise
        return self.guess_1 == self.answer


class Wordle:
    """ THIS CLASS REPRESENTS THE WORDLE GAME """

    def __init__(self, words):
        """ initializes the wordle game  """
        self._words = words
        wordDict = []
        for word in words:
            wordDict.append(word)
        self.answer = choice(wordDict)
        self._guesses1 = 0

    def guesses(self):
        # returns the number of guesses made 
        return self._guesses1

    def guess(self, guessed):
        """
               Make a guess in the Wordle game.

               Parameters:
               - guessed (str): The word guessed by the player.

               Returns:
               - Guess: A Guess object representing the current guess.
               """
        self._guesses1 += 1

        return Guess(guessed, self.answer)


class TooShortError(Exception):
    # Raised when a word is too short for the Wordle game
    pass


class TooLongError(Exception):
    # Raised when a word is too long for the Wordle game
    pass



class NotLettersError(Exception):
    # Raised when a word contains non letter characters
    pass
