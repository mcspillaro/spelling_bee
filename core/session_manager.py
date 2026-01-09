from dataclasses import dataclass
import random
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont
from core.tts_manager import TTSManager

# Organizing word data structure into a dataclass over 'dict'
@dataclass
class Word:
    text: str
    definition: str
    sentence: str
    learned_tier: int = 0
    review_tier: int = 0

# Creating session manager to handle word sessions
class SessionManager:
    # quiz_size=N >>> refers to the amount of words needed to practice before showing quiz
    def __init__(self, words_per_session=10, quiz_size=5): # Defines each session as 10 words to practice
        self.words_per_session = words_per_session
        
        self.words = [] # List to hold words that are being practiced
        self.all_words = []  # List to hold all available words
        self.session_words = []  # List to hold words for the current session
        self.current_index = 0  # Index to track the current word in the session
        
        self.learned_tier = 0 # Tier index to track learn tier
        self.review_tier = 0 # Tier index to track review tier

        self.practice_complete = False  # Flag to indicate if the practice session is complete
        self.quiz_mode = False  # Flag to indicate if the session is in quiz mode
        self.quiz_size = quiz_size
        self.recent_words = [] # Stores the last N words for mini-quiz

    # Track recent words for quiz
    def add_recent_word(self, word: Word):
        self.recent_words.append(word)
        # Keep only the last quiz_size words
        if len(self.recent_words) > self.quiz_size: 
            self.recent_words.pop(0)

    def get_recent_words(self):
        """Return only the words practiced in the most recent batch."""
        return list(self.recent_words)

    def clear_recent_words(self):
        self.recent_words = []

    # Loading the words
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
        self.recent_words = []  # Clear recent words for new session

    # Practice flow
    def get_current_word(self):
        """Return the current word to practice."""
        if self.current_index < len(self.session_words):
            return self.session_words[self.current_index]
        return None

    def advance_word(self):
        """Advance to the next word in the session."""
        word = self.get_current_word()
        if word:
            self.add_recent_word(word)  # Track recent words for quiz

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