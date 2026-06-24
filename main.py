import sys
from PyQt6.QtWidgets import QApplication
from config import ConfigManager
from core import PomodoroTimer
from ui import MainWindow

def main() -> None:
    app = QApplication(sys.argv)
    
    app.setApplicationName("Pomaro")
    app.setOrganizationName("DevTools")
    
    # NEW: Tells Wayland to link this window to 'pomaro.desktop'
    app.setDesktopFileName("pomaro.desktop") 

    config = ConfigManager.load_config()
    timer_core = PomodoroTimer(config)
    window = MainWindow(timer_core)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()