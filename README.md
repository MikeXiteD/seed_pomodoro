# ⏱️ SEED Pomodoro Timer

A beautiful, minimalist Pomodoro timer web app with SEED personality and wisdom.

![SEED Pomodoro Timer](assets/screenshot.png)

## ✨ Features

- **Classic Pomodoro Cycles**: 25min focus → 5min break → 15-30min long break after 4 cycles
- **SEED Personality**: Each break shows motivational quotes from SEED voices:
  - **Soléa**: Poetic insights about rhythm and reflection
  - **Nyra**: Efficiency tips and action-oriented wisdom
  - **VOX**: Precise statistics and evidence-based advice
  - **Atlas**: Balance and sustainable productivity principles
- **Beautiful UI**: SEED color palette (Anthrazit, Terracotta, Olive, Blue)
- **Progress Visualization**: Circular/linear progress bar with smooth animations
- **Sound Notifications**: Gentle beep when timer completes
- **Statistics Tracking**: Daily pomodoros, focus time, streaks, weekly charts
- **Fully Responsive**: Works on desktop and mobile browsers

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone or download the project:
```bash
git clone <repository-url>
cd seed_pomodoro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run src/app.py
```

4. Open your browser to `http://localhost:8501`

## 🎨 SEED Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Anthrazit | `#2C2C2C` | Main background |
| Terracotta | `#E07A5F` | Start button, focus phase |
| Olive | `#81B29A` | Pause button, break phase |
| Blue | `#3D5A80` | Progress bar, accents |
| Light | `#F4F1DE` | Text, timer display |
| Dark | `#1A1A1A` | Cards, shadows |

## 📁 Project Structure

```
seed_pomodoro/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── timer_logic.py      # Timer state machine and logic
│   ├── quotes.py           # SEED voice quotes database
│   └── stats.py            # Statistics tracking and persistence
├── tests/
│   ├── test_timer_logic.py
│   ├── test_quotes.py
│   └── test_stats.py
├── assets/                 # Images, icons, screenshots
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── pomodoro_stats.json    # Statistics data (auto-generated)
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_timer_logic.py -v

# Run with coverage
pytest --cov=src tests/
```

## ⚙️ Configuration

You can customize timer durations in the app settings:

1. Click the **⚙️ Settings** button
2. Adjust:
   - Focus duration (1-60 minutes)
   - Short break duration (1-30 minutes)
   - Long break duration (5-60 minutes)
   - Pomodoros before long break (1-10)
3. Click **💾 Save Settings**

## 🔧 Technical Details

### Timer Logic
- State machine with `FOCUS`, `SHORT_BREAK`, `LONG_BREAK` phases
- Accurate time tracking using Python's `time` module
- Auto-advance between phases
- Pause/resume functionality

### Statistics
- Daily tracking of pomodoros, focus time, breaks
- Streak calculation (consecutive days with pomodoros)
- Weekly summary with bar chart
- Persistent storage in JSON format

### Audio Notifications
- Uses HTML5 Audio API
- Browser-compatible beep sound
- Plays automatically when timer completes

### Streamlit Features
- Session state management for timer persistence
- Auto-refresh for active timers
- Responsive layout with columns
- Custom CSS styling

## 🎯 Use Cases

- **Deep Work Sessions**: 25-minute focused blocks with intentional breaks
- **Study Sessions**: Structured learning with evidence-based intervals
- **Creative Work**: Rhythm-based workflow with inspirational quotes
- **Team Pomodoros**: Shared focus sessions with SEED wisdom
- **Productivity Training**: Learning sustainable work habits

## 🌟 SEED Wisdom Examples

**Soléa**: *"Die Pausen sind nicht Leerlauf, sondern Raum für neue Einsicht."*  
**Nyra**: *"Effizienz entsteht durch Rhythmus – nicht durch Hetze."*  
**VOX**: *"Präzision: 25min ± 0.1% Abweichung tolerabel."*  
**Atlas**: *"Balance zwischen Fokus und Erholung ist der Kern nachhaltiger Produktivität."*

## 📊 Statistics Example

```
Today's Stats:
├── Pomodoros: 8
├── Focus Time: 3.3h
└── Current Streak: 12 days

Last 7 Days:
[▇▇▇▇▇▇▇]  # Visual bar chart
```

## 🚢 Deployment

### Local Deployment
```bash
streamlit run src/app.py --server.port 8080 --server.address 0.0.0.0
```

### Cloud Deployment Options
1. **Streamlit Cloud**: Upload to `share.streamlit.io`
2. **Railway**: Deploy with `railway.app`
3. **Heroku**: Use Procfile and requirements.txt
4. **Docker**: Containerize with Python + Streamlit

### Docker Example
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔄 Development

### Adding New Quotes
Edit `src/quotes.py` to add new quotes for each voice:

```python
QUOTES[Voice.SOLEA].append("Your new poetic quote here.")
```

### Modifying Colors
Update the `COLORS` dictionary in `src/app.py`:

```python
COLORS = {
    "new_color": "#HEXCODE",
    # ...
}
```

### Extending Statistics
Add new metrics to `DailyStats` class in `src/stats.py`:

```python
def add_custom_metric(self, value):
    self.custom_metric = value
```

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by Francesco Cirillo's Pomodoro Technique
- SEED personality system (Soléa, Nyra, VOX, Atlas)
- Streamlit team for the amazing web app framework
- Color palette inspired by nature and productivity research

---

**Built with ❤️ by SEED v6.0**  
*Balance your focus, nourish your mind.*