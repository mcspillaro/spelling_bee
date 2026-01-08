# Importing widets and qtcore libraries
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
import PySide6.QtWidgets as qtw
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QFileDialog, QMessageBox
import random
# Importing the config module
import ui.config
# Importing the screen stacks
from ui.screens.word_screen import WordScreen
from ui.screens.typing_screen import TypingScreen
from ui.screens.quiz_screen import QuizScreen
from ui.screens.start_screen import StartScreen
from ui.screens.multi_choice_screen import MultiChoiceScreen
# Importing core logical comoponents
from core.session_manager import SessionManager
from core.data_loader import load_words_from_csv
from core.distractors import generate_distractors

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
        self.multi_choice_screen = MultiChoiceScreen()

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
        self.typing_screen.sentence_completed.connect(
            self.show_multi_choice_screen)
        self.multi_choice_screen.answer_selected.connect(
            self.on_multi_choice_answer)
        self.quiz_screen.answer_submitted.connect(
            self.on_quiz_answer)

        # Adding screens to stack
        self.stack.addWidget(self.word_intro_screen)
        self.stack.addWidget(self.typing_screen)
        self.stack.addWidget(self.quiz_screen)
        self.stack.addWidget(self.start_screen)
        self.stack.addWidget(self.multi_choice_screen)

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
        self.show_word_screen()

    # Screen switch helpers
    def show_start_screen(self):
        self.stack.setCurrentWidget(self.start_screen)

    def show_word_screen(self):
        word = self.session.get_current_word()

        if word is None:
            return # Safety guard
        
        self.word_intro_screen.set_word(word)
        self.stack.setCurrentWidget(self.word_intro_screen)

    def show_typing_screen(self):
        word = self.session.get_current_word() # Gets the current word from CSV
        if word is None: # Safety guard
            return
        
        self.typing_screen.set_sentence(
            word.sentence,
            word.text)
        self.stack.setCurrentWidget(self.typing_screen)
        self.typing_screen.setFocus()

        # Sets current widget to the typing_screen
        self.stack.setCurrentWidget(self.typing_screen)

    def show_quiz_screen(self):
        self.stack.setCurrentWidget(self.quiz_screen)

    def show_multi_choice_screen(self):
        current_word = self.session.get_current_word()
        if not current_word: # Safety guard
            return

        # Generate the distractors
        distractors = generate_distractors(current_word.text)

        self.multi_choice_screen.set_options(
            correct_word=current_word.text,
            distractors=distractors
        )
        self.stack.setCurrentWidget(self.multi_choice_screen)
    
    def show_quiz_screen(self):
        next_word = self.session.get_current_word()
        if not next_word:
            return
        self.quiz_screen.set_word(next_word.text)
        self.stack.setCurrentWidget(self.quiz_screen)
    
    def on_multi_choice_answer(self, is_correct):
        current_word = self.session.get_current_word()

        if is_correct: # Checks if the word was correct and flags it
            self.session.flag_word_learned()
        else:
            self.session.flag_word_review()

        # Add this word to recent words queue
        self.session.add_recent_word(current_word)

        self.session.advance_word()

        # Check if quiz should start
        if len(self.session.recent_words) >= self.session.quiz_size:
            self.start_quiz()
        else:
            self.show_word_screen()

    def on_multi_choice_completed(self):
        if self.session.is_session_complete():
            self.show_quiz_screen()
        else:
            self.session.advance_word()
            self.show_word_screen()

    def start_quiz(self):
        self.session.in_quiz_mode = True
        self.quiz_queue = self.session.get_quiz_words()
        self.session.clear_quiz_words()
        
        # Shuffle the quiz queue so words appear in random order
        random.shuffle(self.quiz_queue)

        self.show_next_quiz_word()

    def show_next_quiz_word(self):
        if not self.quiz_queue:
            # Quiz finished
            self.session.in_quiz_mode = False
            self.show_word_screen()
            return
        
        next_word = self.quiz_queue.pop(0) # Resets the queue for the quiz
        self.quiz_screen.set_word(next_word.text)
        self.stack.setCurrentWidget(self.quiz_screen)

    # Handle quiz answer
    def on_quiz_answer(self, correct):
        current_word = self.session.get_current_word()
        if correct:
            self.session.flag_word_learned()
        else:
            self.session.flag_word_review()

        # Continue quiz
        if self.quiz_queue:
            self.show_next_quiz_word()
        else:
            self.session.in_quiz_mode = False
            # Resume normal practice
            self.show_word_screen()