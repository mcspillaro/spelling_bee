# Importing libraries and modules required
import sys, random
from PySide6 import QtCore as qtc, QtWidgets as qtw, QtGui as qtg
# Imports ui.main_window module element
from ui.main_window import MainWindow

def main(): 
    # Creates the application instance
    app = qtw.QApplication(sys.argv)

    # Calls the main window instance from ui.main_window
    window = MainWindow()
    window.show()

    # Starts the application's event loop
    sys.exit(app.exec())

# Run the main function if this script is executed
if __name__ == "__main__":
    main()