import sys
from PyQt6.QtWidgets import QApplication
from config import ConfigManager
from core import PomodoroTimer
from ui import MainWindow

def main() -> None:
    # Creates the Qt application instance
    app = QApplication(sys.argv)
    
    # Fundamental for KDE and other DEs to correctly identify the application
    app.setApplicationName("Pomaro")
    app.setOrganizationName("DevTools")

    # Modular Initialization
    config = ConfigManager.load_config()
    timer_core = PomodoroTimer(config)
    window = MainWindow(timer_core)

    window.show()
    
    # Starts the PyQt Event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()