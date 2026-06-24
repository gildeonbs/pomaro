from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QProgressBar, QListWidget,
                             QListWidgetItem, QLineEdit, QSystemTrayIcon,
                             QMenu, QApplication, QDialog, QSpinBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QFont
from core import PomodoroTimer
from config import ConfigManager


class SettingsDialog(QDialog):
    """Window for configuring cycle durations."""

    def __init__(self, parent: QWidget, current_config: dict) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.config = current_config

        layout = QFormLayout(self)

        self.focus_spin = QSpinBox()
        self.focus_spin.setRange(1, 120)
        self.focus_spin.setValue(self.config["focus_time"])

        self.short_spin = QSpinBox()
        self.short_spin.setRange(1, 30)
        self.short_spin.setValue(self.config["short_break"])

        self.long_spin = QSpinBox()
        self.long_spin.setRange(1, 60)
        self.long_spin.setValue(self.config["long_break"])

        layout.addRow("Focus (minutes):", self.focus_spin)
        layout.addRow("Short Break (minutes):", self.short_spin)
        layout.addRow("Long Break (minutes):", self.long_spin)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        layout.addRow(save_btn)

    def get_new_config(self) -> dict:
        self.config["focus_time"] = self.focus_spin.value()
        self.config["short_break"] = self.short_spin.value()
        self.config["long_break"] = self.long_spin.value()
        return self.config


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, timer_core: PomodoroTimer) -> None:
        super().__init__()
        self.timer_core = timer_core
        self.setWindowTitle("Pomaro")
        self.resize(300, 324)

        # System Tray Configuration
        self.tray_icon = QSystemTrayIcon(self)
        # It is recommended to use a real icon in your project.
        # Here, the fallback will use the native folder icon if no custom icon exists.
        # icon = QIcon.fromTheme("appointment-new", QIcon.fromTheme("document-new"))

        # Qt will look for the "pomodoro-app" icon in the system theme (KDE).
        # If not found, it will try to load the "icon.svg" file from the local directory.
        icon = QIcon.fromTheme("pomodoro-app", QIcon("icon.svg"))
        self.tray_icon.setIcon(icon)
        self.setWindowIcon(icon)
        self.tray_icon.setIcon(icon)
        self.setWindowIcon(icon)
        self._setup_tray_menu()
        self.tray_icon.show()

        # Interface Construction
        self._setup_ui()
        self._connect_signals()

    def _setup_tray_menu(self) -> None:
        """Creates the tray icon context menu."""
        tray_menu = QMenu()
        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.showNormal)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_activated)

    def _setup_ui(self) -> None:
        """Builds the main widgets."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        '''main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)'''
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # --- NERD FONT SETUP ---
        # Note: Check your OS font manager. Sometimes it's registered as "Noto Sans Nerd Font" with spaces.
        nerd_font = QFont("NotoSans Nerd Font")
        
        # Status and Time Labels
        self.lbl_state = QLabel("\uf140 FOCUS") # \uf140 is a bullseye/target icon
        self.lbl_state.setFont(nerd_font)
        self.lbl_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_state.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.lbl_time = QLabel("25:00")
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_time.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)

        # Controls
        controls_layout = QHBoxLayout()
        
        # Using Unicode hex codes for Nerd Font icons
        self.btn_start = QPushButton("\uf04b Start")  # fa-play icon
        self.btn_start.setFont(nerd_font)
        
        self.btn_pause = QPushButton("\uf04c Pause")  # fa-pause icon
        self.btn_pause.setFont(nerd_font)
        
        self.btn_skip = QPushButton("\uf051 Skip")    # fa-step-forward icon
        self.btn_skip.setFont(nerd_font)
        
        self.btn_config = QPushButton("\uf013")       # fa-cog (gear) icon
        self.btn_config.setFont(nerd_font)

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_pause)
        controls_layout.addWidget(self.btn_skip)
        controls_layout.addWidget(self.btn_config)

        # Mini To-Do List
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Add a new task and press Enter...")
        self.todo_list = QListWidget()

        main_layout.addWidget(self.lbl_state)
        main_layout.addWidget(self.lbl_time)
        main_layout.addWidget(self.progress_bar)
        main_layout.addLayout(controls_layout)

        todo_label = QLabel("Task List:")
        main_layout.addWidget(todo_label)
        main_layout.addWidget(self.todo_input)
        main_layout.addWidget(self.todo_list)

        # UI Connections
        self.btn_start.clicked.connect(self.timer_core.start)
        self.btn_pause.clicked.connect(self.timer_core.pause)
        self.btn_skip.clicked.connect(self.timer_core.skip)
        self.btn_config.clicked.connect(self._open_settings)
        self.todo_input.returnPressed.connect(self._add_task)
        self.todo_list.itemClicked.connect(self._toggle_task)

    def _connect_signals(self) -> None:
        """Connects core (logic) signals to the UI."""
        self.timer_core.tick.connect(self._update_time)
        self.timer_core.state_changed.connect(self._update_state)
        self.timer_core.cycle_finished.connect(self._on_cycle_finished)

        # Updates the initial screen based on the saved configuration
        self.timer_core.reset()

    def _update_time(self, time_left: int, total_time: int) -> None:
        """Updates visual components with the new time."""
        mins, secs = divmod(time_left, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        self.lbl_time.setText(time_str)

        # Reverse progress (100 -> 0)
        progress = int((time_left / total_time) * 100) if total_time > 0 else 0
        self.progress_bar.setValue(progress)

        # Native tray tooltip
        state_translated = {
            "FOCUS": "Focus",
            "SHORT_BREAK": "Short Break",
            "LONG_BREAK": "Long Break"
        }
        cycle_name = state_translated.get(self.timer_core.current_cycle, "")
        self.tray_icon.setToolTip(f"Pomodoro - {cycle_name}: {time_str}")

    def _update_state(self, state: str, cycle: str) -> None:
        """Updates state labels (Focus, Break)."""
        # Replaced Emojis with Nerd Font Unicode escapes
        state_translated = {
            "FOCUS": "\udb81\udcfe  Focus",              # Target icon
            "SHORT_BREAK": "\uec15  Short Break",  # Coffee cup icon
            "LONG_BREAK": "\udb81\ude8e  Long Break"     # Snooze icon
        }
        self.lbl_state.setText(state_translated.get(cycle, cycle))

    def _on_cycle_finished(self, cycle: str) -> None:
        """Triggered when a cycle reaches zero."""
        if self.timer_core.config.get("sound_enabled"):
            QApplication.beep()  # Basic system sound alert

        messages = {
            "FOCUS": "Focus session completed! Time to rest.",
            "SHORT_BREAK": "Break finished! Let's get back to work.",
            "LONG_BREAK": "Long break finished! Feeling refreshed?"
        }

        # Native notification via QSystemTrayIcon (perfect for KDE Plasma)
        self.tray_icon.showMessage(
            "Pomaro",
            messages.get(cycle, "Cycle completed!"),
            QSystemTrayIcon.MessageIcon.Information,
            5000
        )
        self.showNormal()
        self.activateWindow()

    def _open_settings(self) -> None:
        """Opens the settings modal window."""
        dialog = SettingsDialog(self, self.timer_core.config)
        if dialog.exec():
            new_config = dialog.get_new_config()
            ConfigManager.save_config(new_config)
            self.timer_core.update_config(new_config)

    def _add_task(self) -> None:
        """Adds an item to the mini To-Do list."""
        text = self.todo_input.text().strip()
        if text:
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.todo_list.addItem(item)
            self.todo_input.clear()

    def _toggle_task(self, item: QListWidgetItem) -> None:
        """Strikes through the To-Do item (visual completion feedback)."""
        font = item.font()
        if item.checkState() == Qt.CheckState.Checked:
            font.setStrikeOut(True)
            item.setForeground(Qt.GlobalColor.gray)
        else:
            font.setStrikeOut(False)
            item.setForeground(Qt.GlobalColor.black)  # Or a theme-based default color
        item.setFont(font)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Restores the window with a single tray click."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.showNormal()
                self.activateWindow()
            else:
                self.hide()

    def closeEvent(self, event) -> None:
        """Minimizes to the tray instead of closing."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Pomaro",
            "The application is still running in the background.",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )