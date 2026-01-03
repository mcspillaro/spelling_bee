from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout,
    QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QFont
from ui.typing_widget import TypingWidget
from ui.quiz_widget import QuizWidget
from logic.quiz_manager import QuizManager
from audio.tts import speak

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.stack.addWidget(self.word_intro_screen)
        self.stack.addWidget(self.typing_screen)
        self.stack.addWidget(self.quiz_screen)

        self.stack.setCurrentWidget(self.word_intro_screen)

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

    # ─────────────────────────────────────────────
    # SCREEN 2: TYPING PRACTICE (Placeholder)
    # ─────────────────────────────────────────────
    def create_typing_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        sentence = "The wizard conjured a spell."
        target_word = "spell"

        self.typing_widget = TypingWidget(sentence, target_word)
        self.typing_widget.setFixedHeight(200)

        layout.addWidget(self.typing_widget)
        return widget

    # ─────────────────────────────────────────────
    # SCREEN 3: QUIZ (Placeholder)
    # ─────────────────────────────────────────────
    def create_quiz_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.quiz_widget = QuizWidget()
        self.quiz_widget.answered.connect(self.on_quiz_answered)

        layout.addWidget(self.quiz_widget)
        return widget

    def start_quiz(self, session_words): # Start quiz after the learning session
        self.quiz_manager = QuizManager(session_words)
        self.stack.setCurrentWidget(self.quiz_screen)
        self.next_quiz_word()

    def next_quiz_word(self): # Advance quiz
        if not self.quiz_manager.has_next():
            self.end_quiz()
            return
        word = self.quiz_manager.next_word()
        self.current_quiz_word = word

        self.quiz_widget.set_word(word["word"])
        speak(word["word"])

    def on_quiz_answered(self, correct):
        self.progress_manager.update(
            self.current_quiz_word["id"],
            correct
        )
        self.next_quiz_word()

    # ─────────────────────────────────────────────
    # ANIMATION: MOVE WORD TO TOP
    # ─────────────────────────────────────────────
    def animate_word_to_top(self):
        start_rect = self.word_label.geometry()
        end_rect = QRect(0, 40, 1200, 120)

        self.animation = QPropertyAnimation(self.word_label, b"geometry")
        self.animation.setDuration(800)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

        self.definition_label.show()

self.typing_widget.completed.connect(self.on_sentence_complete)


# ─────────────────────────────────────────────
# RUN APP
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
