"""
Tests for timer_logic.py
"""

import pytest
import time
from src.timer_logic import PomodoroTimer, TimerConfig, TimerPhase


class TestTimerConfig:
    """Test TimerConfig class."""
    
    def test_default_config(self):
        config = TimerConfig()
        assert config.focus_duration == 25 * 60
        assert config.short_break_duration == 5 * 60
        assert config.long_break_duration == 15 * 60
        assert config.pomodoros_before_long_break == 4
    
    def test_custom_config(self):
        config = TimerConfig(
            focus_duration=30 * 60,
            short_break_duration=10 * 60,
            long_break_duration=20 * 60,
            pomodoros_before_long_break=3
        )
        assert config.focus_duration == 30 * 60
        assert config.short_break_duration == 10 * 60
        assert config.long_break_duration == 20 * 60
        assert config.pomodoros_before_long_break == 3


class TestPomodoroTimer:
    """Test PomodoroTimer class."""
    
    def test_initial_state(self):
        timer = PomodoroTimer()
        assert timer.phase == TimerPhase.FOCUS
        assert timer.pomodoros_completed == 0
        assert not timer.is_running
        assert not timer.is_paused
        assert timer.start_time is None
        assert timer.paused_elapsed == 0.0
    
    def test_reset(self):
        timer = PomodoroTimer()
        timer.start()
        time.sleep(0.1)
        timer.pause()
        timer.pomodoros_completed = 2
        
        timer.reset()
        
        assert timer.phase == TimerPhase.FOCUS
        assert timer.pomodoros_completed == 0
        assert not timer.is_running
        assert not timer.is_paused
        assert timer.start_time is None
        assert timer.paused_elapsed == 0.0
    
    def test_start_stop(self):
        timer = PomodoroTimer()
        
        # Start
        timer.start()
        assert timer.is_running
        assert not timer.is_paused
        assert timer.start_time is not None
        
        # Stop
        timer.stop()
        assert not timer.is_running
        assert not timer.is_paused
        assert timer.start_time is None
    
    def test_pause_resume(self):
        timer = PomodoroTimer()
        timer.start()
        time.sleep(0.1)
        
        # Pause
        timer.pause()
        assert not timer.is_running
        assert timer.is_paused
        assert timer.paused_elapsed > 0
        
        # Resume
        timer.start()
        assert timer.is_running
        assert not timer.is_paused
    
    def test_get_phase_duration(self):
        config = TimerConfig(
            focus_duration=10,
            short_break_duration=5,
            long_break_duration=15
        )
        timer = PomodoroTimer(config)
        
        assert timer.get_phase_duration() == 10  # Focus
        
        timer.phase = TimerPhase.SHORT_BREAK
        assert timer.get_phase_duration() == 5
        
        timer.phase = TimerPhase.LONG_BREAK
        assert timer.get_phase_duration() == 15
    
    def test_get_remaining(self):
        config = TimerConfig(focus_duration=10)  # 10 seconds
        timer = PomodoroTimer(config)
        
        # Not started
        assert timer.get_remaining() == 10.0
        
        # Started
        timer.start()
        time.sleep(0.1)
        remaining = timer.get_remaining()
        assert 9.8 < remaining < 10.0
    
    def test_get_progress(self):
        config = TimerConfig(focus_duration=10)
        timer = PomodoroTimer(config)
        
        # Not started
        assert timer.get_progress() == 0.0
        
        # Halfway
        timer.start()
        timer.start_time = time.time() - 5  # Simulate 5 seconds elapsed
        assert 0.49 < timer.get_progress() < 0.51
    
    def test_check_completion_not_complete(self):
        config = TimerConfig(focus_duration=10)
        timer = PomodoroTimer(config)
        timer.start()
        
        assert not timer.check_completion()
    
    def test_phase_transition_focus_to_short_break(self):
        config = TimerConfig(focus_duration=0.1)  # Very short for testing
        timer = PomodoroTimer(config)
        timer.start()
        
        time.sleep(0.15)  # Wait for completion
        assert timer.check_completion()
        assert timer.phase == TimerPhase.SHORT_BREAK
        assert timer.pomodoros_completed == 1
    
    def test_phase_transition_to_long_break(self):
        config = TimerConfig(
            focus_duration=0.1,
            pomodoros_before_long_break=2
        )
        timer = PomodoroTimer(config)
        
        # First pomodoro
        timer.start()
        time.sleep(0.15)
        timer.check_completion()
        assert timer.phase == TimerPhase.SHORT_BREAK
        assert timer.pomodoros_completed == 1
        
        # Short break to focus
        timer.start()
        time.sleep(0.15)
        timer.check_completion()
        assert timer.phase == TimerPhase.FOCUS
        
        # Second pomodoro (should trigger long break)
        timer.start()
        time.sleep(0.15)
        timer.check_completion()
        assert timer.phase == TimerPhase.LONG_BREAK
        assert timer.pomodoros_completed == 2
    
    def test_get_time_display(self):
        config = TimerConfig(focus_duration=125)  # 2 minutes 5 seconds
        timer = PomodoroTimer(config)
        
        minutes, seconds = timer.get_time_display()
        assert minutes == 2
        assert seconds == 5
    
    def test_get_phase_name(self):
        timer = PomodoroTimer()
        
        timer.phase = TimerPhase.FOCUS
        assert timer.get_phase_name() == "Focus"
        
        timer.phase = TimerPhase.SHORT_BREAK
        assert timer.get_phase_name() == "Short Break"
        
        timer.phase = TimerPhase.LONG_BREAK
        assert timer.get_phase_name() == "Long Break"
    
    def test_get_status_summary(self):
        timer = PomodoroTimer()
        timer.start()
        
        status = timer.get_status_summary()
        
        assert "phase" in status
        assert "phase_name" in status
        assert "remaining_minutes" in status
        assert "remaining_seconds" in status
        assert "progress" in status
        assert "is_running" in status
        assert "is_paused" in status
        assert "pomodoros_completed" in status
        assert "next_long_break" in status