# Import necessary PySide6 modules
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QKeyEvent
from PySide6.QtCore import Qt, Signal, QTimer

# Creating default class for the screen
class TypingScreen(QWidget):
    # Defining a signal to indicate sentence completion
    sentence_completed = Signal()

    def __init__(self):
        super().__init__()

        # Instance variables
        self.sentence = ""
        self.typed = ""
        self.target_word = ""
        self.target_range = None
        self.max_line_width = 800 # Width of the text block
        self.line_spacing = 10
        self.font = QFont("Consolas", 22)
        self.error_index = None
        self.locked = False
        self.caret_visible = True
        self.caret_timer = QTimer(self)
        self.caret_timer.timeout.connect(self._toggle_caret)
        self.caret_timer.start(250) # Blink every 500 ms

        # New: Press Enter message
        self.show_enter_prompt = False

        # Enter key enabled flag
        self.enter_enabled = False

        # Setting the focus policy to accept keyboard input
        self.setFocusPolicy(Qt.StrongFocus)

    # Methods
    def _toggle_caret(self): # Toggles the caret visibility
        self.caret_visible = not self.caret_visible
        self.update()

    def _wrap_sentence(self, metrics):
        max_width = min(self.max_line_width, int(self.width() * 0.7)) # 70% of widget width
        
        words = []
        start = 0

        # Build word spans (including trailing spaces)
        for part in self.sentence.split(' '):
            end = start + len(part)
            words.append((start, end))
            start = end + 1 # Skip space
        
        # Sets up for line building
        lines = []
        current_line = []
        current_width = 0

        # Build lines
        for word_start, word_end in words:
            word_text = self.sentence[word_start:word_end]
            word_width = metrics.horizontalAdvance(word_text + ' ')

            # Check if adding the word exceeds max width
            if current_line and current_width + word_width > max_width:
                lines.append(current_line)
                current_line = []
                current_width = 0
            
            # Add word characters
            for i in range(word_start, word_end):
                current_line.append(i)

            # Add space if it exists
            if word_end < len(self.sentence):
                current_line.append(word_end)

            current_width += word_width # Account for space

        if current_line: # Add last line
            lines.append(current_line)

        return lines

    # Creating the sentence functiionality
    def set_sentence(self, sentence: str, target_word: str):
        self.sentence = sentence
        self.target_word = target_word
        self.typed = ""
        self.locked = False
        self.caret_visible = True
        self.show_enter_prompt = False
        self.enter_enabled = False

        # Find target word position (first occurrence)
        start = sentence.lower().find(target_word.lower())
        if start != -1:
            self.target_range = (start, start + len(target_word))
        else:
            self.target_range = None

        self.update()

        # Automatically enable "Press Enter" after sentence is fully displayed
        duration_ms = max(500, int(len(sentence) * 300))  # Rough estimate: 0.3 sec per char
        QTimer.singleShot(duration_ms, self._enable_enter_prompt)

    # Enable Enter and show the message
    def _enable_enter_prompt(self):
        self.show_enter_prompt = True
        self.enter_enabled = True
        self.update()

    # Input handling
    def keyPressEvent(self, event: QKeyEvent):
        if not self.sentence:
            return

        key = event.key()
        text = event.text()

        # BACKSPACE
        if key == Qt.Key_Backspace:
            if self.typed:
                self.typed = self.typed[:-1]

            # Always unlock after backspace
            self.locked = False
            self.update()
            return

        # ENTER key handling
        if key in (Qt.Key_Return, Qt.Key_Enter) and self.enter_enabled:
            self.sentence_completed.emit()
            return

        # LOCKED: ignore everything else
        if self.locked:
            return

        # CHARACTER INPUT
        if key == Qt.Key_Space:
            char = " "
        elif len(text) == 1 and text.isprintable():
            char = text
        else:
            return

        index = len(self.typed)

        # Correct character
        if index < len(self.sentence) and char == self.sentence[index]:
            self.typed += char
        else:
            # Incorrect → lock immediately
            self.typed += char
            self.locked = True

        self.update()

        # Automatically show Enter prompt if fully typed
        if self.typed == self.sentence:
            self._enable_enter_prompt()

    # Rendering the typing screen
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        metrics = painter.fontMetrics()

        lines = self._wrap_sentence(metrics)

        total_height = (
            len(lines) * metrics.height()
            + (len(lines) - 1) * self.line_spacing
        )

        start_y = (self.height() - total_height) // 2 + metrics.ascent()

        # For caret position
        caret_x = None
        caret_y = None

        for line_index, line in enumerate(lines):
            line_width = sum(metrics.horizontalAdvance(self.sentence[i]) for i in line)
            start_x = (self.width() - line_width) // 2

            x = start_x
            y = start_y + line_index * (metrics.height() + self.line_spacing)

            for i in line:
                char = self.sentence[i]
                char_width = metrics.horizontalAdvance(char)

                # ── Caret position ────────────────
                if i == len(self.typed):
                    caret_x = x
                    caret_y = y

                # ── Target word highlight ──────────────
                if self.target_range and self.target_range[0] <= i < self.target_range[1]:
                    painter.fillRect(
                        x,
                        y - metrics.ascent(),
                        char_width,
                        metrics.height(),
                        QColor("#2A2A2A") # Dark highlight
                    )

                # ── Character color ────────────────────
                if i < len(self.typed):
                    if self.typed[i] == char:
                        painter.setPen(QColor("#4CAF50")) # Green
                        painter.drawText(x, y, char)
                    else:
                        # WRONG character
                        if char == " ":
                            # Draw a visible red rectangle for the wrong space
                            painter.fillRect(x, y - metrics.ascent(), char_width, metrics.height(), QColor("#F44336"))
                        else:
                            painter.setPen(QColor("#F44336")) # Red
                            painter.drawText(x, y, char)
                else:
                    painter.setPen(QColor("#888888")) # Grey
                    painter.drawText(x, y, char)

                x += char_width

            # ── Caret drawing ────────────────
            if self.caret_visible and caret_x is not None and len(self.typed) < len(self.sentence):
                painter.setPen(QColor("#E0E0E0"))
                painter.drawLine(
                    caret_x,
                    caret_y - metrics.ascent(),
                    caret_x,
                    caret_y + metrics.descent(),
                )

        # ── ENTER ARROW CUE ────────────────
        if self.typed == self.sentence:
            # Draw "↵" (Enter arrow) at the very end of the last line
            arrow = "↵"
            arrow_width = metrics.horizontalAdvance(arrow)
            painter.setPen(QColor("#FFFFFF"))  # White arrow
            painter.drawText(x, y, arrow)  # x, y already at end of line
