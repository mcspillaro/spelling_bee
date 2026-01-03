from PySide6.QtCore import Signal

class TypingWidget(QWidget):
    completed = Signal()

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
                self.update()
            return

        if not key:
            return

        expected = self.sentence[self.index]

        if key == expected:
            self.results[self.index] = True
            self.index += 1
        else:
            self.results[self.index] = False

        self.update()

    def is_complete_and_correct(self):
        return (
            self.index == len(self.sentence) and
            all(r is True for r in self.results)
        )
