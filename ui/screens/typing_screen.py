# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtCore import Qt, Signal

# Creating default class for the screen
class TypingScreen(QWidget):
    # Defining a signal to indicate sentence completion
    sentence_completed = Signal()

    def __init__(self):
        super().__init__()

        # Placeholder for future implementation
        self.sentence = ""
        self.typed = ""
        self.font = QFont("Consolas", 22)

        # Setting the focus policy to accept keyboard input
        self.setFocusPolicy(Qt.StrongFocus)

    # Creating the sentence functiionality
    def set_sentence(self, sentence=str):
        self.sentence = sentence
        self.typed = ""
        self.update()

    # Input handling
    def keyPressEvent(self, event):
        if not self.sentence: # Safety guard; if no sentence is set, ignore input
            return
        
        key = event.key()
        text = event.text()

        # Handles the key presses
        if key == Qt.Key_Backspace:
            self.typed = self.typed[:-1]
        elif key == Qt.Key_Space:
            if len(self.typed) < len(self.sentence):
                self.typed += ' '
        elif len(text) == 1 and text.isprintable():
            self.typed += text

        # Updates the function after the keystroke inputs
        self.update()

        if self.typed == self.sentence: # Check if the sentence is completed
            self.sentence_completed.emit()

    # Rendering the typing screen
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)

        # Dimensions of the widget
        x = 100
        y = self.height() // 2

        # Drawing the typed text
        for i, char in enumerate(self.sentence):
            if i < len(self.typed):
                if self.typed[i] == char: 
                    painter.setPen(QColor("#4CAF50")) # Green
                else: 
                    painter.setPen(QColor("#F44336")) # Red
            else:
                painter.setPen(QColor("#888888")) # Grey

            painter.drawText(x, y, char)
            x += painter.fontMetrics().horizontalAdvance(char)