from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

class TypingWidget(QWidget):
    completed = Signal()

    def __init__(self, sentence, target_word, parent=None):
        super().__init__(parent)
        self.sentence = sentence
        self.target_word = target_word.lower()
        self.index = 0
        self.results = [None] * len(sentence)

        self.setFocusPolicy(Qt.StrongFocus)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.display_edit = QTextEdit()
        self.display_edit.setFont(QFont("Segoe UI", 24))
        self.display_edit.setAlignment(Qt.AlignCenter)
        self.display_edit.setReadOnly(True)
        self.display_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.display_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.display_edit)

        self.update_display()
        self.setFocus()

    def update_display(self):
        text = ""
        i = 0
        while i < len(self.sentence):
            char = self.sentence[i]
            if i < self.index:
                if self.results[i] is True:
                    text += f'<span style="color: green;">{char}</span>'
                elif self.results[i] is False:
                    text += f'<span style="color: red;">{char}</span>'
                else:
                    text += char
            elif i == self.index:
                text += f'<span style="background-color: yellow;">{char}</span>'
            else:
                # Check if this is the start of the target word
                if self._is_target_word_start(i):
                    word_end = self._find_word_end(i)
                    word = self.sentence[i:word_end]
                    if word.lower() == self.target_word:
                        text += f'<span style="background-color: lightblue; font-weight: bold;">{word}</span>'
                        i = word_end - 1
                    else:
                        text += char
                else:
                    text += char
            i += 1
        self.display_edit.setHtml(text)

    def _is_target_word_start(self, index):
        if index == 0 or self.sentence[index-1] in ' \n\t':
            return True
        return False

    def _find_word_end(self, start):
        for i in range(start, len(self.sentence)):
            if self.sentence[i] in ' \n\t':
                return i
        return len(self.sentence)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.is_complete_and_correct():
                self.completed.emit()
            return

        if self.index >= len(self.sentence):
            return

        key = event.text()

        if event.key() == Qt.Key_Backspace:
            if self.index > 0:
                self.index -= 1
                self.results[self.index] = None
                self.update_display()
            return

        if not key:
            return

        expected = self.sentence[self.index]

        if key == expected:
            self.results[self.index] = True
            self.index += 1
        else:
            self.results[self.index] = False

        self.update_display()

    def is_complete_and_correct(self):
        return (
            self.index == len(self.sentence) and
            all(r is True for r in self.results)
        )
