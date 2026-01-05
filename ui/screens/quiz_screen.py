# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

# Creating default class for the screen
class QuizScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Generating the layout for the screen and placeholder
        layout = QVBoxLayout(self)
        label = QLabel("Quiz Screen Placeholder", self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)