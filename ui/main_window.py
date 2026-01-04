from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout,
    QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PySide6.QtGui import QFont
from ui.typing_widget import TypingWidget
from ui.quiz_widget import QuizWidget
from ui.spelling_practice_widget import SpellingPracticeWidget
from logic.quiz_manager import QuizManager
from logic.word_manager import WordManager
from logic.progress_manager import ProgressManager
from audio.tts import speak
import random
import config

class MainWindow(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        db_path = "users/mikhael/progress.db"  # or get from conn
        self.word_manager = WordManager(db_path)
        self.progress_manager = ProgressManager(conn)

        self.setWindowTitle("Spelling Bee Trainer")
        self.setFixedSize(1200, 1200)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #EAEAEA;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.word_intro_screen = self.create_word_intro_screen()
        self.typing_screen = self.create_typing_screen()
        self.quiz_screen = self.create_quiz_screen()
        self.spelling_screen = self.create_spelling_screen()

        self.stack.addWidget(self.word_intro_screen)
        self.stack.addWidget(self.typing_screen)
        self.stack.addWidget(self.quiz_screen)
        self.stack.addWidget(self.spelling_screen)

        self.session_words = []
        self.current_word_index = 0
        self.start_session()

    def start_session(self):
        count = random.randint(config.DEFAULT_SESSION_MIN, config.DEFAULT_SESSION_MAX)
        self.session_words = self.word_manager.get_session_words(count)
        self.current_word_index = 0
        self.show_next_word()

    def show_next_word(self):
        if self.current_word_index >= len(self.session_words):
            self.start_quiz()
            return
        
        word = self.session_words[self.current_word_index]
        self.current_word = word
        
        self.word_label.setText(word['word'].upper())
        self.definition_label.setText(word['definition'])
        self.definition_label.hide()
        
        self.stack.setCurrentWidget(self.word_intro_screen)
        
        # Speak the word
        speak(word['word'])
        
        # After 2 seconds, animate and show definition
        QTimer.singleShot(2000, self.animate_and_show_definition)

    def animate_and_show_definition(self):
        self.animate_word_to_top()
        speak(self.current_word['definition'])
        
        # After animation and speech, show typing screen
        QTimer.singleShot(3000, self.show_typing_screen)

    def show_typing_screen(self):
        sentence = self.current_word['sentence']
        target_word = self.current_word['word']
        self.typing_widget = TypingWidget(sentence, target_word)
        self.typing_widget.completed.connect(self.on_sentence_complete)
        
        # Replace the layout's widget
        layout = self.typing_screen.layout()
        if layout.count() > 0:
            layout.itemAt(0).widget().setParent(None)
        layout.addWidget(self.typing_widget)
        
        self.stack.setCurrentWidget(self.typing_screen)
        self.typing_widget.setFocus()
        self.typing_widget.setFocus()

    def on_sentence_complete(self):
        self.show_spelling_screen()

    def show_spelling_screen(self):
        self.spelling_widget.set_word(self.current_word['word'])
        speak(self.current_word['word'])
        self.stack.setCurrentWidget(self.spelling_screen)

    def on_spelling_answered(self, correct):
        self.current_word_index += 1
        self.show_next_word()

    def start_quiz(self):
        self.quiz_manager = QuizManager(self.session_words)
        self.stack.setCurrentWidget(self.quiz_screen)
        self.next_quiz_word()

    def next_quiz_word(self):
        if not self.quiz_manager.has_next():
            self.end_quiz()
            return
        word = self.quiz_manager.next_word()
        self.current_quiz_word = word

        self.quiz_widget.set_word(word["word"])
        speak(word["word"])

    def on_quiz_answered(self, correct):
        self.word_manager.update_progress(
            self.current_quiz_word["id"],
            correct
        )
        self.next_quiz_word()

    def end_quiz(self):
        # For now, just restart session
        self.start_session()

    # ─────────────────────────────────────────────
    # SCREEN 1: WORD INTRO
    # ─────────────────────────────────────────────
    def create_word_intro_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.word_label = QLabel("ABERRATION")
        self.word_label.setFont(QFont("Segoe UI", 72, QFont.Bold))
        self.word_label.setAlignment(Qt.AlignCenter)

        self.definition_label = QLabel(
            "A deviation from what is normal or expected."
        )
        self.definition_label.setFont(QFont("Segoe UI", 28))
        self.definition_label.setAlignment(Qt.AlignCenter)
        self.definition_label.setWordWrap(True)
        self.definition_label.hide()

        layout.addWidget(self.word_label)
        layout.addWidget(self.definition_label)

        return widget

    def create_typing_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        # Widget will be added dynamically
        return widget

    def create_quiz_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.quiz_widget = QuizWidget()
        self.quiz_widget.answered.connect(self.on_quiz_answered)

        layout.addWidget(self.quiz_widget)
        return widget

    def create_spelling_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.spelling_widget = SpellingPracticeWidget()
        self.spelling_widget.answered.connect(self.on_spelling_answered)

        layout.addWidget(self.spelling_widget)
        return widget

    def animate_word_to_top(self):
        start_rect = self.word_label.geometry()
        end_rect = QRect(0, 40, 1200, 120)

        self.animation = QPropertyAnimation(self.word_label, b"geometry")
        self.animation.setDuration(800)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

        self.definition_label.show()
