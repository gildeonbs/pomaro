from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from typing import Literal

class PomodoroTimer(QObject):
    """
    Pomodoro business logic.
    Emits signals for the graphical interface to react without direct coupling.
    """
    # Signals for communication with the UI
    tick = pyqtSignal(int, int)  # time_left, total_time
    cycle_finished = pyqtSignal(str) # finished_cycle_type
    state_changed = pyqtSignal(str, str) # current_state, current_cycle

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timeout)
        
        self.state: Literal["STOPPED", "RUNNING", "PAUSED"] = "STOPPED"
        self.current_cycle: Literal["FOCUS", "SHORT_BREAK", "LONG_BREAK"] = "FOCUS"
        
        self.pomodoros_completed: int = 0
        self.time_left: int = self._get_cycle_duration_sec()
        self.total_time: int = self.time_left

    def _get_cycle_duration_sec(self) -> int:
        """Returns the duration of the current cycle in seconds."""
        if self.current_cycle == "FOCUS":
            return self.config["focus_time"] * 60
        elif self.current_cycle == "SHORT_BREAK":
            return self.config["short_break"] * 60
        else:
            return self.config["long_break"] * 60

    def start(self) -> None:
        """Starts or resumes the timer."""
        if self.state != "RUNNING":
            self.state = "RUNNING"
            self.timer.start(1000) # 1000 ms = 1 second
            self.state_changed.emit(self.state, self.current_cycle)

    def pause(self) -> None:
        """Pauses the timer."""
        if self.state == "RUNNING":
            self.state = "PAUSED"
            self.timer.stop()
            self.state_changed.emit(self.state, self.current_cycle)

    def skip(self) -> None:
        """Skips the current cycle and goes to the next."""
        self.timer.stop()
        self._advance_cycle()

    def reset(self) -> None:
        """Stops the timer and restarts the current cycle."""
        self.timer.stop()
        self.state = "STOPPED"
        self.time_left = self._get_cycle_duration_sec()
        self.total_time = self.time_left
        self.tick.emit(self.time_left, self.total_time)
        self.state_changed.emit(self.state, self.current_cycle)

    def update_config(self, new_config: dict) -> None:
        """Updates configurations and resets if stopped."""
        self.config = new_config
        if self.state == "STOPPED":
            self.reset()

    def _on_timeout(self) -> None:
        """Executed every second by the QTimer."""
        if self.time_left > 0:
            self.time_left -= 1
            self.tick.emit(self.time_left, self.total_time)
        else:
            self.timer.stop()
            self._advance_cycle()

    def _advance_cycle(self) -> None:
        """Advances the state machine to the next cycle."""
        finished_cycle = self.current_cycle
        
        if finished_cycle == "FOCUS":
            self.pomodoros_completed += 1
            if self.pomodoros_completed % 4 == 0:
                self.current_cycle = "LONG_BREAK"
            else:
                self.current_cycle = "SHORT_BREAK"
        else:
            self.current_cycle = "FOCUS"

        self.state = "STOPPED"
        self.time_left = self._get_cycle_duration_sec()
        self.total_time = self.time_left
        
        self.tick.emit(self.time_left, self.total_time)
        self.state_changed.emit(self.state, self.current_cycle)
        self.cycle_finished.emit(finished_cycle)