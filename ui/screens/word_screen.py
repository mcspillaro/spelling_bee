# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal, QTimer
from core.tts_manager import TTSManager
import threading

# Creating default class for the screen
class WordScreen(QWidget):
    # Defining a signal to indicate continuation
    continue_requested = Signal()
    _enable_continue_signal = Signal()  # internal signal to enable button safely

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
        self.continue_button.setEnabled(False)  # Defaults to False first
        self.continue_button.clicked.connect(
            self.continue_requested.emit
        )

        # Generating the layout for the screen
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.word_label)
        layout.addWidget(self.definition_label)
        layout.addWidget(self.continue_button)

        # Connect internal signal
        self._enable_continue_signal.connect(lambda: self.continue_button.setEnabled(True))

    def set_word(self, word):
        """Receive a word object and update the UI elements accordingly."""
        self.word_label.setText(word.text)
        self.definition_label.setText(word.definition)
        self.continue_button.setEnabled(False)  # Reset button

        # Speak the word asynchronously with delay
        threading.Thread(target=self._speak_and_enable, args=(word.text,), daemon=True).start()

    def _speak_and_enable(self, word_text: str):
        import time

        # Optional short delay before starting TTS to avoid cutoff
        time.sleep(0.2)  # 200ms delay

        # Speak the word
        self.tts.speak(word_text)

        # Estimate duration roughly 0.3s per character, min 0.5s
        duration = max(0.5, len(word_text) * 0.3)
        time.sleep(duration)

        # Emit signal to enable continue button on main thread
        self._enable_continue_signal.emit()
