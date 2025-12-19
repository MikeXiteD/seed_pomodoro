"""
Tests for stats.py
"""

import pytest
import json
import os
from datetime import date, timedelta
from src.stats import DailyStats, StatsTracker


class TestDailyStats:
    """Test DailyStats class."""
    
    def test_initialization(self):
        stats = DailyStats()
        assert stats.date == str(date.today())
        assert stats.pomodoros == 0
        assert stats.focus_time == 0
        assert stats.break_time == 0
        assert stats.completed_cycles == 0
        assert stats.long_breaks_taken == 0
    
    def test_custom_date(self):
        stats = DailyStats("2023-12-25")
        assert stats.date == "2023-12-25"
    
    def test_add_pomodoro(self):
        stats = DailyStats()
        stats.add_pomodoro(1500)  # 25 minutes
        
        assert stats.pomodoros == 1
        assert stats.focus_time == 1500
        assert stats.break_time == 0
    
    def test_add_break_short(self):
        stats = DailyStats()
        stats.add_break(300)  # 5 minutes
        
        assert stats.break_time == 300
        assert stats.long_breaks_taken == 0
    
    def test_add_break_long(self):
        stats = DailyStats()
        stats.add_break(900, is_long=True)  # 15 minutes
        
        assert stats.break_time == 900
        assert stats.long_breaks_taken == 1
    
    def test_add_cycle(self):
        stats = DailyStats()
        stats.add_cycle()
        
        assert stats.completed_cycles == 1
    
    def test_to_dict(self):
        stats = DailyStats("2023-12-25")
        stats.add_pomodoro(1500)
        stats.add_break(300)
        stats.add_cycle()
        
        data = stats.to_dict()
        
        assert data["date"] == "2023-12-25"
        assert data["pomodoros"] == 1
        assert data["focus_time"] == 1500
        assert data["break_time"] == 300
        assert data["completed_cycles"] == 1
        assert data["long_breaks_taken"] == 0
        assert data["total_time"] == 1800
    
    def test_from_dict(self):
        data = {
            "date": "2023-12-25",
            "pomodoros": 2,
            "focus_time": 3000,
            "break_time": 600,
            "completed_cycles": 1,
            "long_breaks_taken": 0
        }
        
        stats = DailyStats.from_dict(data)
        
        assert stats.date == "2023-12-25"
        assert stats.pomodoros == 2
        assert stats.focus_time == 3000
        assert stats.break_time == 600
        assert stats.completed_cycles == 1
        assert stats.long_breaks_taken == 0


class TestStatsTracker:
    """Test StatsTracker class."""
    
    @pytest.fixture
    def temp_stats_file(self, tmp_path):
        """Create a temporary stats file for testing."""
        file_path = tmp_path / "test_stats.json"
        return str(file_path)
    
    def test_initialization_no_file(self, temp_stats_file):
        """Test initialization when no stats file exists."""
        tracker = StatsTracker(temp_stats_file)
        
        assert tracker.current_day.date == str(date.today())
        assert tracker.current_day.pomodoros == 0
        assert tracker.streak == 0
        assert len(tracker.history) == 0
        
        # File should be created after first save
        tracker._save()
        assert os.path.exists(temp_stats_file)
    
    def test_initialization_with_file(self, temp_stats_file):
        """Test initialization with existing stats file."""
        # Create test data
        test_data = {
            "history": {
                "2023-12-24": {
                    "date": "2023-12-24",
                    "pomodoros": 3,
                    "focus_time": 4500,
                    "break_time": 900,
                    "completed_cycles": 3,
                    "long_breaks_taken": 0,
                    "total_time": 5400
                }
            },
            "streak": 1,
            "last_updated": "2023-12-24T10:00:00"
        }
        
        with open(temp_stats_file, 'w') as f:
            json.dump(test_data, f)
        
        tracker = StatsTracker(temp_stats_file)
        
        # Should load existing history
        assert "2023-12-24" in tracker.history
        assert tracker.history["2023-12-24"].pomodoros == 3
        assert tracker.streak == 1
        
        # Should create today's stats
        assert tracker.current_day.date == str(date.today())
    
    def test_record_pomodoro(self, temp_stats_file):
        tracker = StatsTracker(temp_stats_file)
        
        tracker.record_pomodoro(1500)
        
        assert tracker.current_day.pomodoros == 1
        assert tracker.current_day.focus_time == 1500
        
        # Check file was saved
        with open(temp_stats_file, 'r') as f:
            data = json.load(f)
            assert str(date.today()) in data["history"]
            assert data["history"][str(date.today())]["pomodoros"] == 1
    
    def test_record_break(self, temp_stats_file):
        tracker = StatsTracker(temp_stats_file)
        
        tracker.record_break(300, is_long=False)
        assert tracker.current_day.break_time == 300
        assert tracker.current_day.long_breaks_taken == 0
        
        tracker.record_break(900, is_long=True)
        assert tracker.current_day.break_time == 1200
        assert tracker.current_day.long_breaks_taken == 1
    
    def test_record_cycle(self, temp_stats_file):
        tracker = StatsTracker(temp_stats_file)
        
        tracker.record_cycle()
        assert tracker.current_day.completed_cycles == 1
    
    def test_get_today_summary(self, temp_stats_file):
        tracker = StatsTracker(temp_stats_file)
        tracker.record_pomodoro(1500)
        tracker.record_break(300)
        
        summary = tracker.get_today_summary()
        
        assert summary["date"] == str(date.today())
        assert summary["pomodoros"] == 1
        assert summary["focus_time"] == 1500
        assert summary["break_time"] == 300
    
    def test_get_weekly_summary(self, temp_stats_file):
        # Create tracker with some history
        tracker = StatsTracker(temp_stats_file)
        
        # Manually add some past days
        yesterday = date.today() - timedelta(days=1)
        tracker.history[str(yesterday)] = DailyStats(str(yesterday))
        tracker.history[str(yesterday)].add_pomodoro(1500)
        
        two_days_ago = date.today() - timedelta(days=2)
        tracker.history[str(two_days_ago)] = DailyStats(str(two_days_ago))
        tracker.history[str(two_days_ago)].add_pomodoro(3000)
        
        tracker._save()
        
        weekly = tracker.get_weekly_summary()
        
        # Should have 7 entries
        assert len(weekly) == 7
        
        # Check today is included
        today_entries = [w for w in weekly if w["date"] == str(date.today())]
        assert len(today_entries) == 1
        
        # Check past days have correct data
        yesterday_entries = [w for w in weekly if w["date"] == str(yesterday)]
        assert len(yesterday_entries) == 1
        assert yesterday_entries[0]["pomodoros"] == 1
    
    def test_streak_calculation(self, temp_stats_file):
        # Create test data with streak
        test_data = {
            "history": {
                str(date.today() - timedelta(days=1)): {
                    "date": str(date.today() - timedelta(days=1)),
                    "pomodoros": 2,
                    "focus_time": 3000,
                    "break_time": 600,
                    "completed_cycles": 2,
                    "long_breaks_taken": 0,
                    "total_time": 3600
                },
                str(date.today() - timedelta(days=2)): {
                    "date": str(date.today() - timedelta(days=2)),
                    "pomodoros": 3,
                    "focus_time": 4500,
                    "break_time": 900,
                    "completed_cycles": 3,
                    "long_breaks_taken": 0,
                    "total_time": 5400
                }
            },
            "streak": 0,  # Will be recalculated
            "last_updated": "2023-12-24T10:00:00"
        }
        
        with open(temp_stats_file, 'w') as f:
            json.dump(test_data, f)
        
        tracker = StatsTracker(temp_stats_file)
        
        # Streak should be 2 (yesterday and day before)
        assert tracker.streak == 2
    
    def test_streak_broken(self, temp_stats_file):
        # Create test data with broken streak (gap of 2 days)
        test_data = {
            "history": {
                str(date.today() - timedelta(days=3)): {
                    "date": str(date.today() - timedelta(days=3)),
                    "pomodoros": 2,
                    "focus_time": 3000,
                    "break_time": 600,
                    "completed_cycles": 2,
                    "long_breaks_taken": 0,
                    "total_time": 3600
                }
            },
            "streak": 0,
            "last_updated": "2023-12-24T10:00:00"
        }
        
        with open(temp_stats_file, 'w') as f:
            json.dump(test_data, f)
        
        tracker = StatsTracker(temp_stats_file)
        
        # Streak should be 0 (gap too large)
        assert tracker.streak == 0
    
    def test_reset_today(self, temp_stats_file):
        tracker = StatsTracker(temp_stats_file)
        
        tracker.record_pomodoro(1500)
        tracker.record_break(300)
        
        # Reset
        tracker.reset_today()
        
        assert tracker.current_day.pomodoros == 0
        assert tracker.current_day.focus_time == 0
        assert tracker.current_day.break_time == 0
        
        # Today should still be in history
        assert str(date.today()) in tracker.history