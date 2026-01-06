from dataclasses import dataclass
import random

# Organizing word data structure into a dataclass over 'dict'
@dataclass
class Word:
    text: str
    definition: str
    sentence: str

# Creating session manager to handle word sessions
class SessionManager:
    def __init__(self, words_per_session=10): # Defines each session as 10 words to practice
        self.words_per_session = words_per_session

        self.all_words = []  # List to hold all available words
        self.session_words = []  # List to hold words for the current session
        self.current_index = 0  # Index to track the current word in the session
        
        self.learned_tier = 0 # Tier index to track learn tier
        self.review_tier = 0 # Tier index to track review tier

        self.practice_complete = False  # Flag to indicate if the practice session is complete
        self.quiz_mode = False  # Flag to indicate if the session is in quiz mode

    # Loading section
    def load_words(self, word_list):
        """Load words into the session manager from a provided list of Word objects."""
        self.all_words = word_list
    
    def start_new_session(self):
        """Select random words and reset session state."""
        if not self.all_words:
            raise RuntimeError("No words loaded to start a session.")

        self.session_words = random.sample(
            self.all_words,
            min(self.words_per_session, len(self.all_words))
        )

        self.current_index = 0 # Reset index for new session
        self.practice_complete = False
        self.quiz_mode = False

    # Practice flow
    def get_current_word(self):
        """Return the current word to practice."""
        if self.current_index < len(self.session_words):
            return self.session_words[self.current_index]
        return None

    def advance_word(self):
        """Advance to the next word in the session."""
        self.current_index += 1

        if self.current_index >= len(self.session_words):
            self.practice_complete = True
            self.quiz_mode = True
            self.current_index = 0  # Reset index for quiz mode

    def is_practice_complete(self):
        """Check if the practice session is complete."""
        return self.practice_complete

    # Word flagging
    def flag_word_learned(self):
        word = self.get_current_word()
        if not word: # Safety guard
            return
        
        word.learned_tier = min(getattr(word, "learned_tier", 0) + 1, 3)
        word.review_tier = min(getattr(word, "review_tier", 0) - 1, 0)
        
    def flag_word_review(self):
        word = self.get_current_word()
        if not word: # Safety guard
            return

        word.review_tier = min(getattr(word, "review_tier", 0) + 1, 3)
        word.learned_tier = max(getattr(word, "learned_tier", 0) - 1, 0)
    
    # Quiz flow
    def get_quiz_words(self):
        "Return the list of words that was just practiced in the session quiz."
        return list(self.session_words)