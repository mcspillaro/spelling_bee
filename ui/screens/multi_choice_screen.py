# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal

# Creating default class for the screen
class MultiChoiceScreen(QWidget):
    # Emits True if correct choice is selected, False otherwise
    answer_selected = Signal(bool)

    def __init__(self):
        super().__init__()

        self.correct_index = None
        self.buttons = []

        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        # Prompt label
        self.prompt_label = QLabel("Select the correctly spelled word:")
        self.prompt_label.setAlignment(Qt.AlignCenter)
        self.prompt_label.setStyleSheet("font-size: 24px; color: #111111;")
        self.layout.addWidget(self.prompt_label)

        # Option buttons
        for i in range(4):
            btn = QPushButton()
            btn.setFixedWidth(400)
            btn.setFixedHeight(60)
            btn.setStyleSheet(
                "font-size: 22px; color: white; background-color: #333333;"
            )
            btn.clicked.connect(self._handle_click)
            self.layout.addWidget(btn)
            self.buttons.append(btn)

    # Methods
    def set_options(self, correct_word, distractors):
        """
        correct_word: str
        distractors: list of 3 incorrect words
        """
        import random
        
        # Shuffle options and determine correct index
        options = distractors + [correct_word]
        random.shuffle(options)
        self.correct_index = options.index(correct_word)

        # Set text on the buttons
        for btn, word in zip(self.buttons, options):
            btn.setText(word)
            btn.setEnabled(True)
            btn.setStyleSheet(
                "font-size: 22px; color: white; background-color: #333333;"
            )

    def _handle_click(self):
        sender = self.sender()
        if not sender:
            return # Safety guard

        # Determine if the selected button is correct
        selected_index = self.buttons.index(sender)
        correct = selected_index == self.correct_index

        # Provide immediate feedback
        for i, btn in enumerate(self.buttons):
            if i == self.correct_index:
                btn.setStyleSheet(
                    "font-size: 22px; color: white; background-color: #4CAF50;" # Green
                )
            elif i == selected_index:
                btn.setStyleSheet(
                    "font-size: 22px; color: white; background-color: #F44336;" # Red
                )
            else:
                btn.setStyleSheet(
                    "font-size: 22px; color: white; background-color: #888888;" # Grey
                )
            btn.setEnabled(False)

        # Emit signal after a short delay to allow user to see feedback
        from PySide6.QtCore import QTimer
        QTimer.singleShot(700, lambda: self.answer_selected.emit(correct))