# Importing widets and qtcore libraries
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
import PySide6.QtWidgets as qtw
from PySide6.QtWidgets import QStackedWidget
# Importing the config module
import ui.config
# Importing the screen stacks
from ui.screens.word_screen import WordScreen
from ui.screens.typing_screen import TypingScreen
from ui.screens.quiz_screen import QuizScreen
from ui.screens.start_screen import StartScreen

# Main window class definition
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting window title and size from config
        self.setWindowTitle(ui.config.APP_NAME)
        self.resize(ui.config.WINDOW_SIZE[0], ui.config.WINDOW_SIZE[1])

        # Screen stack setup
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
    
        # Screens
        self.word_intro_screen = WordScreen()
        self.typing_screen = TypingScreen()
        self.quiz_screen = QuizScreen()
        self.start_screen = StartScreen()

        # Connect signals to switch screens
        self.start_screen.start_practice_requested.connect(
            self.show_word_screen)

        # Adding screens to stack
        self.stack.addWidget(self.word_intro_screen)
        self.stack.addWidget(self.typing_screen)
        self.stack.addWidget(self.quiz_screen)
        self.stack.addWidget(self.start_screen)
        
        # Start screen
        self.show_start_screen()

    # Screen switch helpers
    def show_start_screen(self):
        self.stack.setCurrentWidget(self.start_screen)

    def show_word_screen(self):
        self.stack.setCurrentWidget(self.word_intro_screen)

    def show_typing_screen(self):
        self.stack.setCurrentWidget(self.typing_screen)

    def show_quiz_screen(self):
        self.stack.setCurrentWidget(self.quiz_screen)