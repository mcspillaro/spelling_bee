# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal

# Creating default class for the screen
class StartScreen(QWidget):
    # Defining a signal to indicate the start of practice
    start_practice_requested = Signal()

    def __init__(self):
        super().__init__()

        # Generating the layout for the screen and placeholder
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Generating placeholder title and button
        title = QLabel("Spelling Bee Trainer")
        title.setAlignment(Qt.AlignCenter)

        # Adds a start button to the start screen
        start_button = QPushButton("Start Practice")
        # When button is clicked on the start screen, emits a signal to start practice
        start_button.clicked.connect(self.start_practice_requested.emit)

        # Adds the widgets to the layout
        layout.addWidget(title)
        layout.addWidget(start_button)