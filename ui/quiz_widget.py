from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class QuizWidget(QWidget):
    answered = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        self.prompt_label = QLabel("Spell the word")
        self.prompt_label.setFont(QFont("Segoe UI", 36))
        self.prompt_label.setAlignment(Qt.AlignCenter)

        self.hidden_label = QLabel("████████")
        self.hidden_label.setFont(QFont("Segoe UI", 48))
        self.hidden_label.setAlignment(Qt.AlignCenter)

        self.input = QLineEdit()
        self.input.setFont(QFont("Segoe UI", 28))
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setFixedWidth(400)
        self.input.returnPressed.connect(self.check_answer)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.hidden_label)
        layout.addWidget(self.input)

        self.correct_word = ""

    def set_word(self, word: str):
        self.correct_word = word
        self.hidden_label.setText("█" * len(word))
        self.input.clear()
        self.input.setFocus()

    def check_answer(self):
        answer = self.input.text().strip()
        correct = answer.lower() == self.correct_word.lower()
        self.answered.emit(correct)
