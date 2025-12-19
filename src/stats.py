"""
Statistics tracking for Pomodoro sessions.
Tracks daily pomodoros, streaks, and session history.
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import json
import os


class DailyStats:
    """Statistics for a single day."""
    
    def __init__(self, date_str: Optional[str] = None):
        self.date = date_str or str(date.today())
        self.pomodoros: int = 0
        self.focus_time: int = 0  # in seconds
        self.break_time: int = 0  # in seconds
        self.completed_cycles: int = 0  # focus + short break pairs
        self.long_breaks_taken: int = 0
    
    def add_pomodoro(self, focus_duration: int = 25 * 60):
        """Record a completed pomodoro."""
        self.pomodoros += 1
        self.focus_time += focus_duration
    
    def add_break(self, break_duration: int, is_long: bool = False):
        """Record a break."""
        self.break_time += break_duration
        if is_long:
            self.long_breaks_taken += 1
    
    def add_cycle(self):
        """Record a completed focus+break cycle."""
        self.completed_cycles += 1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "date": self.date,
            "pomodoros": self.pomodoros,
            "focus_time": self.focus_time,
            "break_time": self.break_time,
            "completed_cycles": self.completed_cycles,
            "long_breaks_taken": self.long_breaks_taken,
            "total_time": self.focus_time + self.break_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DailyStats':
        """Create from dictionary."""
        stats = cls(data["date"])
        stats.pomodoros = data["pomodoros"]
        stats.focus_time = data["focus_time"]
        stats.break_time = data["break_time"]
        stats.completed_cycles = data.get("completed_cycles", 0)
        stats.long_breaks_taken = data.get("long_breaks_taken", 0)
        return stats


class StatsTracker:
    """Main statistics tracker with persistence."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or "pomodoro_stats.json"
        self.current_day: DailyStats = DailyStats()
        self.history: Dict[str, DailyStats] = {}
        self.streak: int = 0
        self._load()
    
    def _load(self):
        """Load statistics from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                
                # Load history
                self.history = {
                    date_str: DailyStats.from_dict(stats_data)
                    for date_str, stats_data in data.get("history", {}).items()
                }
                
                # Load or create today's stats
                today = str(date.today())
                if today in self.history:
                    self.current_day = self.history[today]
                    # Recalculate streak on load
                    self._update_streak()
                else:
                    self.current_day = DailyStats(today)
                    self._update_streak()
                    
            except (json.JSONDecodeError, KeyError):
                # Corrupted file, start fresh
                self.history = {}
                self.current_day = DailyStats()
                self.streak = 0
        else:
            self.current_day = DailyStats()
            self._update_streak()
    
    def _save(self):
        """Save statistics to storage."""
        # Ensure current day is in history
        self.history[self.current_day.date] = self.current_day
        # Update streak before saving
        self._update_streak()
        
        data = {
            "history": {
                date_str: stats.to_dict()
                for date_str, stats in self.history.items()
            },
            "streak": self.streak,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _update_streak(self):
        """Update current streak based on history."""
        dates = sorted(self.history.keys(), reverse=True)
        streak = 0
        current_date = date.today()
        
        for i, date_str in enumerate(dates):
            stats_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if consecutive
            if i == 0:
                # Today or yesterday
                delta = (current_date - stats_date).days
                if delta <= 1 and self.history[date_str].pomodoros > 0:
                    streak += 1
                else:
                    break
            else:
                # Check consecutive days
                prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d").date()
                delta = (prev_date - stats_date).days
                if delta == 1 and self.history[date_str].pomodoros > 0:
                    streak += 1
                else:
                    break
        
        self.streak = streak
    
    def record_pomodoro(self, focus_duration: int = 25 * 60):
        """Record a completed pomodoro."""
        self.current_day.add_pomodoro(focus_duration)
        self._save()
    
    def record_break(self, break_duration: int, is_long: bool = False):
        """Record a break."""
        self.current_day.add_break(break_duration, is_long)
        self._save()
    
    def record_cycle(self):
        """Record a completed focus+break cycle."""
        self.current_day.add_cycle()
        self._save()
    
    def get_today_summary(self) -> Dict:
        """Get summary for today."""
        return self.current_day.to_dict()
    
    def get_weekly_summary(self) -> List[Dict]:
        """Get summary for last 7 days."""
        today = date.today()
        weekly = []
        
        for i in range(7):
            day = today - timedelta(days=i)
            day_str = str(day)
            
            if day_str in self.history:
                weekly.append(self.history[day_str].to_dict())
            else:
                weekly.append({
                    "date": day_str,
                    "pomodoros": 0,
                    "focus_time": 0,
                    "break_time": 0,
                    "completed_cycles": 0,
                    "long_breaks_taken": 0,
                    "total_time": 0
                })
        
        return weekly
    
    def get_streak(self) -> int:
        """Get current streak in days."""
        return self.streak
    
    def reset_today(self):
        """Reset today's statistics."""
        self.current_day = DailyStats()
        self.history[self.current_day.date] = self.current_day
        self._update_streak()
        self._save()


# Global instance
stats_tracker = StatsTracker()
