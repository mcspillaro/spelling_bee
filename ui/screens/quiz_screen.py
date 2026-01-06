from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class QuizScreen(QWidget):
    # Emits True if user typed correctly, False if not
    answer_submitted = Signal(bool)

    def __init__(self):
        super().__init__()

        self.current_word = "" # Initializes the current word that was just practiced
        self.user_input = "" # Initializes the user input

        # Builds the layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        # Label for instructions
        self.prompt_label = QLabel("Type the word that was just practiced:")
        self.prompt_label.setAlignment(Qt.AlignCenter)
        self.prompt_label.setFont(QFont("Consolas", 20))
        self.layout.addWidget(self.prompt_label)

        # Blocked word placeholder
        self.word_block_label = QLabel("██████")
        self.word_block_label.setAlignment(Qt.AlignCenter)
        self.word_block_label.setFont(QFont("Consolas", 36))
        self.layout.addWidget(self.word_block_label)

        # Text input
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Consolas", 24))
        self.input_field.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.input_field)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFont(QFont("Consolas", 20))
        self.submit_button.clicked.connect(self._handle_submit)
        self.layout.addWidget(self.submit_button)

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Consolas", 18))
        self.layout.addWidget(self.feedback_label)

    # Setup quiz word
    def set_word(self, word: str):
        self.current_word = word
        self.word_block_label.setText("█" * len(word))
        self.input_field.clear()
        self.input_field.setEnabled(True)
        self.feedback_label.setText("")
        self.input_field.setFocus()

    # Handle submission
    def _handle_submit(self):
        self.user_input = self.input_field.text().strip()
        correct = self.user_input.lower() == self.current_word.lower()

        if correct:
            self.feedback_label.setText("✅ Correct!")
            self.feedback_label.setStyleSheet("color: #4CAF50;")
        else:
            self.feedback_label.setText(f"❌ Wrong! Correct: {self.current_word}")
            self.feedback_label.setStyleSheet("color: #F44336;")

        # Lock input
        self.input_field.setEnabled(False)

        # Emit signal after short delay
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.answer_submitted.emit(correct))
