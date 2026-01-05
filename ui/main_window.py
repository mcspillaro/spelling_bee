# Importing widets and qtcore libraries
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
import PySide6.QtWidgets as qtw
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QFileDialog, QMessageBox
# Importing the config module
import ui.config
# Importing the screen stacks
from ui.screens.word_screen import WordScreen
from ui.screens.typing_screen import TypingScreen
from ui.screens.quiz_screen import QuizScreen
from ui.screens.start_screen import StartScreen
# Importing logical components
from core.session_manager import SessionManager
from core.data_loader import load_words_from_csv


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

        # Session manager
        self.session = SessionManager(words_per_session=10)
        # Load words from CSV
        words = load_words_from_csv(ui.config.WORDS_CSV_PATH)
        self.session.load_words(words)

        # Signals to switch screens
        self.start_screen.start_practice_requested.connect(
            self.start_practice)
        self.word_intro_screen.continue_requested.connect(
            self.show_typing_screen)

        # Adding screens to stack
        self.stack.addWidget(self.word_intro_screen)
        self.stack.addWidget(self.typing_screen)
        self.stack.addWidget(self.quiz_screen)
        self.stack.addWidget(self.start_screen)
        
        # Start screen
        self.show_start_screen()

    def start_practice(self):
        # Open file dialog to select CSV file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Words CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        """Initiate a new practice session."""

        # File type verification
        if not file_path.lower().endswith('.csv'):
            QMessageBox.warning(
                self, "Invalid Selection", "Please select a valid CSV file.")
            return

        # Try loading words from selected CSV
        try: 
            from core.data_loader import load_words_from_csv
            words =load_words_from_csv(file_path)

            if not words:
                raise ValueError("No words found in the selected CSV.")

            self.session.load_words(words)
            self.session.start_new_session()
            self.show_word_screen()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Failed to load words.",
                str(e)
            )

        self.session.start_new_session()
        self.show_word_screen()

    # Screen switch helpers
    def show_start_screen(self):
        self.stack.setCurrentWidget(self.start_screen)

    def show_word_screen(self):
        word = self.session.get_current_word()

        if word is None:
            return # safety guard
        
        self.word_intro_screen.set_word(word)
        self.stack.setCurrentWidget(self.word_intro_screen)

    def show_typing_screen(self):
        self.stack.setCurrentWidget(self.typing_screen)

    def show_quiz_screen(self):
        self.stack.setCurrentWidget(self.quiz_screen)