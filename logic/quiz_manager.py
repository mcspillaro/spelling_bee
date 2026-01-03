import random

class QuizManager:
    def __init__(self, words):
        self.words = words
        random.shuffle(self.words)
        self.index = 0

    def has_next(self):
        return self.index < len(self.words)

    def next_word(self):
        word = self.words[self.index]
        self.index += 1
        return word
