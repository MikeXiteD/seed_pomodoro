"""
SEED Pomodoro Timer Logic
Handles timer states, phase transitions, and time calculations.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple
import time


class TimerPhase(Enum):
    """Current phase of the Pomodoro cycle."""
    FOCUS = "focus"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


@dataclass
class TimerConfig:
    """Configuration for Pomodoro timer."""
    focus_duration: int = 25 * 60  # 25 minutes in seconds
    short_break_duration: int = 5 * 60  # 5 minutes
    long_break_duration: int = 15 * 60  # 15 minutes
    pomodoros_before_long_break: int = 4


class PomodoroTimer:
    """Main timer class managing state and transitions."""
    
    def __init__(self, config: Optional[TimerConfig] = None):
        self.config = config or TimerConfig()
        self.reset()
    
    def reset(self):
        """Reset timer to initial state."""
        self.phase = TimerPhase.FOCUS
        self.pomodoros_completed = 0
        self.is_running = False
        self.is_paused = False
        self.start_time: Optional[float] = None
        self.paused_elapsed: float = 0.0
        self.total_elapsed: float = 0.0
    
    def start(self):
        """Start or resume the timer."""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_time = time.time() - self.paused_elapsed
    
    def pause(self):
        """Pause the timer."""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.paused_elapsed = self.get_elapsed()
            self.is_running = False
    
    def stop(self):
        """Stop the timer completely."""
        self.is_running = False
        self.is_paused = False
        self.paused_elapsed = 0.0
        self.start_time = None
    
    def get_elapsed(self) -> float:
        """Get elapsed time in seconds for current phase."""
        if not self.is_running or self.start_time is None:
            return self.paused_elapsed
        
        return time.time() - self.start_time
    
    def get_phase_duration(self) -> int:
        """Get total duration of current phase in seconds."""
        if self.phase == TimerPhase.FOCUS:
            return self.config.focus_duration
        elif self.phase == TimerPhase.SHORT_BREAK:
            return self.config.short_break_duration
        else:  # LONG_BREAK
            return self.config.long_break_duration
    
    def get_remaining(self) -> float:
        """Get remaining time in seconds for current phase."""
        elapsed = self.get_elapsed()
        duration = self.get_phase_duration()
        remaining = max(0, duration - elapsed)
        return remaining
    
    def get_progress(self) -> float:
        """Get progress as ratio (0.0 to 1.0)."""
        elapsed = self.get_elapsed()
        duration = self.get_phase_duration()
        
        if duration == 0:
            return 0.0
        
        progress = min(1.0, elapsed / duration)
        return progress
    
    def check_completion(self) -> bool:
        """Check if current phase is complete. Returns True if phase changed."""
        if self.get_remaining() <= 0:
            self._advance_phase()
            return True
        return False
    
    def _advance_phase(self):
        """Move to next phase in the cycle."""
        if self.phase == TimerPhase.FOCUS:
            self.pomodoros_completed += 1
            
            if self.pomodoros_completed % self.config.pomodoros_before_long_break == 0:
                self.phase = TimerPhase.LONG_BREAK
            else:
                self.phase = TimerPhase.SHORT_BREAK
                
        else:  # Coming from a break
            self.phase = TimerPhase.FOCUS
        
        # Reset timer for new phase
        self.paused_elapsed = 0.0
        if self.is_running:
            self.start_time = time.time()
    
    def get_time_display(self) -> Tuple[int, int]:
        """Get remaining time as (minutes, seconds)."""
        remaining = self.get_remaining()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return minutes, seconds
    
    def get_phase_name(self) -> str:
        """Get human-readable phase name."""
        names = {
            TimerPhase.FOCUS: "Focus",
            TimerPhase.SHORT_BREAK: "Short Break",
            TimerPhase.LONG_BREAK: "Long Break"
        }
        return names[self.phase]
    
    def get_status_summary(self) -> dict:
        """Get comprehensive status dictionary."""
        minutes, seconds = self.get_time_display()
        
        return {
            "phase": self.phase.value,
            "phase_name": self.get_phase_name(),
            "remaining_minutes": minutes,
            "remaining_seconds": seconds,
            "progress": self.get_progress(),
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "pomodoros_completed": self.pomodoros_completed,
            "next_long_break": self.config.pomodoros_before_long_break - (self.pomodoros_completed % self.config.pomodoros_before_long_break)
        }