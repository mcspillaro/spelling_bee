import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db import init_user_db
from logic.word_importer import import_words
from pathlib import Path
import os

def main():
    # Initialize database
    user_dir = Path.home() / ".spelling_bee" / "users" / "mikhael"
    user_dir.mkdir(parents=True, exist_ok=True)
    conn = init_user_db(user_dir)
    
    # Import words if not already
    db_path = user_dir / "progress.db"

    if hasattr(sys, '_MEIPASS'):
        csv_path = os.path.join(sys._MEIPASS, 'data', 'word_lists', 'sample_words.csv')
    else:
        csv_path = 'data/word_lists/sample_words.csv'

    import_words(csv_path, str(db_path))
    
    app = QApplication(sys.argv)
    window = MainWindow(conn)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
