# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from core.tts_manager import TTSManager

# Creating default class for the screen
class WordScreen(QWidget):
    # Defining a signal to indicate continuation
    continue_requested = Signal()

    def __init__(self):
        super().__init__()

        # Generating the word ui elements
        self.word_label = QLabel("")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        # Generating the TTS elements
        self.tts = TTSManager()

        # Generating the definition ui elements
        self.definition_label = QLabel("")
        self.definition_label.setAlignment(Qt.AlignCenter)
        self.definition_label.setWordWrap(True)
        self.definition_label.setStyleSheet("font-size: 24px;")

        # Generating continue button ui elements
        self.continue_button = QPushButton("Continue")
        self.continue_button.setEnabled(False) # Defaults to False first
        self.continue_button.clicked.connect(
            self.continue_requested.emit
        )

        # Generating the layout for the screen and placeholder
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.word_label)
        layout.addWidget(self.definition_label)
        layout.addWidget(self.continue_button)

    def set_word(self, word):
        """Receive a word object and update the UI elements accordingly."""
        self.word_label.setText(word.text)
        self.definition_label.setText(word.definition)
        # Redundancy for the continue button
        self.continue_button.setEnabled(False)

        # Speak the word asynchronously
        self.tts.speak(word.text)

        # Estimate duraiton of speech and enable button after
        # Simple approach: 0.5 sec per syllable ~ 0o.2 sec per letter
        duration_ms = max(800, len(word.text) * 200)

        QTimer.singleShot(duration_ms, lambda: self.continue_button.setEnabled(True))