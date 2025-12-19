"""
SEED Pomodoro Timer - Main Streamlit App
"""

import streamlit as st
import time
from datetime import datetime
import json

from timer_logic import PomodoroTimer, TimerConfig
from quotes import quote_manager
from stats import stats_tracker

# Page configuration
st.set_page_config(
    page_title="SEED Pomodoro Timer",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# SEED Color Palette
COLORS = {
    "anthrazit": "#2C2C2C",
    "terracotta": "#E07A5F",
    "olive": "#81B29A",
    "blue": "#3D5A80",
    "light": "#F4F1DE",
    "dark": "#1A1A1A"
}

# Custom CSS
def inject_custom_css():
    css = f"""
    <style>
    /* Main background */
    .stApp {{
        background-color: {COLORS["anthrazit"]};
        color: {COLORS["light"]};
    }}
    
    /* Timer display */
    .timer-display {{
        font-family: 'Courier New', monospace;
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        color: {COLORS["light"]};
        margin: 1rem 0;
    }}
    
    /* Progress bar */
    .stProgress > div > div > div > div {{
        background-color: {COLORS["blue"]};
    }}
    
    /* Buttons */
    .stButton > button {{
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    
    /* Start button */
    .start-btn > button {{
        background-color: {COLORS["terracotta"]};
        color: white;
    }}
    .start-btn > button:hover {{
        background-color: #D2694A;
        transform: translateY(-2px);
    }}
    
    /* Pause button */
    .pause-btn > button {{
        background-color: {COLORS["olive"]};
        color: white;
    }}
    .pause-btn > button:hover {{
        background-color: #6A9C7D;
        transform: translateY(-2px);
    }}
    
    /* Stop/Reset buttons */
    .stop-btn > button {{
        background-color: #6C757D;
        color: white;
    }}
    .stop-btn > button:hover {{
        background-color: #5A6268;
        transform: translateY(-2px);
    }}
    
    /* Cards */
    .card {{
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid {COLORS["blue"]};
    }}
    
    /* Quote cards */
    .quote-card {{
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid;
    }}
    
    .solea-quote {{
        border-left-color: {COLORS["terracotta"]};
    }}
    
    .nyra-quote {{
        border-left-color: {COLORS["olive"]};
    }}
    
    .vox-quote {{
        border-left-color: {COLORS["blue"]};
    }}
    
    .atlas-quote {{
        border-left-color: #9B59B6;
    }}
    
    /* Phase indicators */
    .focus-phase {{
        color: {COLORS["terracotta"]};
        font-weight: bold;
    }}
    
    .break-phase {{
        color: {COLORS["olive"]};
        font-weight: bold;
    }}
    
    .long-break-phase {{
        color: {COLORS["blue"]};
        font-weight: bold;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'timer' not in st.session_state:
        config = TimerConfig(
            focus_duration=25 * 60,
            short_break_duration=5 * 60,
            long_break_duration=15 * 60,
            pomodoros_before_long_break=4
        )
        st.session_state.timer = PomodoroTimer(config)
    
    if 'last_check' not in st.session_state:
        st.session_state.last_check = time.time()
    
    if 'current_quotes' not in st.session_state:
        st.session_state.current_quotes = {}
    
    if 'notification_sent' not in st.session_state:
        st.session_state.notification_sent = False
    
    if 'audio_played' not in st.session_state:
        st.session_state.audio_played = False


def play_sound():
    """Play notification sound using HTML5 Audio."""
    audio_html = """
    <audio autoplay>
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
    st.session_state.audio_played = True


def show_timer_display(timer):
    """Display the timer with progress bar."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Timer display
        minutes, seconds = timer.get_time_display()
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        st.markdown(f'<div class="timer-display">{time_str}</div>', unsafe_allow_html=True)
        
        # Progress bar
        progress = timer.get_progress()
        st.progress(progress)
        
        # Phase indicator
        phase_name = timer.get_phase_name()
        phase_class = ""
        if timer.phase.value == "focus":
            phase_class = "focus-phase"
        elif timer.phase.value == "short_break":
            phase_class = "break-phase"
        else:
            phase_class = "long-break-phase"
        
        st.markdown(f'<div class="{phase_class}" style="text-align: center; font-size: 1.2rem;">{phase_name}</div>', 
                   unsafe_allow_html=True)


def show_controls(timer):
    """Display control buttons."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not timer.is_running:
            st.markdown('<div class="start-btn">', unsafe_allow_html=True)
            if st.button("▶ Start", use_container_width=True):
                timer.start()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="pause-btn">', unsafe_allow_html=True)
            if st.button("⏸ Pause", use_container_width=True):
                timer.pause()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        if st.button("⏹ Stop", use_container_width=True):
            timer.stop()
            st.session_state.notification_sent = False
            st.session_state.audio_played = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            timer.reset()
            st.session_state.notification_sent = False
            st.session_state.audio_played = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.show_settings = not st.session_state.get('show_settings', False)
            st.rerun()


def show_quotes():
    """Display motivational quotes."""
    if st.session_state.current_quotes:
        st.markdown("### 🌟 SEED Wisdom")
        
        for voice, quote in st.session_state.current_quotes.items():
            voice_class = f"{voice.lower()}-quote"
            st.markdown(f'<div class="quote-card {voice_class}"><strong>{voice}:</strong> {quote}</div>', 
                       unsafe_allow_html=True)


def show_stats():
    """Display statistics."""
    st.markdown("### 📊 Today's Stats")
    
    today = stats_tracker.get_today_summary()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pomodoros", today["pomodoros"])
    
    with col2:
        focus_hours = today["focus_time"] / 3600
        st.metric("Focus Time", f"{focus_hours:.1f}h")
    
    with col3:
        st.metric("Current Streak", f"{stats_tracker.get_streak()} days")
    
    # Weekly summary
    weekly = stats_tracker.get_weekly_summary()
    if weekly:
        st.markdown("#### 📈 Last 7 Days")
        weekly_data = [{"Day": w["date"][5:], "Pomodoros": w["pomodoros"]} for w in weekly]
        st.bar_chart({w["Day"]: w["Pomodoros"] for w in weekly_data})


def show_settings():
    """Display settings panel."""
    st.markdown("### ⚙️ Timer Settings")
    
    timer = st.session_state.timer
    
    col1, col2 = st.columns(2)
    
    with col1:
        focus_min = st.number_input("Focus (minutes)", min_value=1, max_value=60, 
                                   value=timer.config.focus_duration // 60)
        short_break_min = st.number_input("Short Break (minutes)", min_value=1, max_value=30,
                                         value=timer.config.short_break_duration // 60)
    
    with col2:
        long_break_min = st.number_input("Long Break (minutes)", min_value=5, max_value=60,
                                        value=timer.config.long_break_duration // 60)
        pomodoros_before_long = st.number_input("Pomodoros before Long Break", min_value=1, max_value=10,
                                               value=timer.config.pomodoros_before_long_break)
    
    if st.button("💾 Save Settings"):
        timer.config.focus_duration = focus_min * 60
        timer.config.short_break_duration = short_break_min * 60
        timer.config.long_break_duration = long_break_min * 60
        timer.config.pomodoros_before_long_break = pomodoros_before_long
        st.success("Settings saved!")
        time.sleep(1)
        st.rerun()


def main():
    """Main app function."""
    inject_custom_css()
    initialize_session_state()
    
    timer = st.session_state.timer
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #F4F1DE;'>⏱️ SEED Pomodoro Timer</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #81B29A;'>Balance your focus with SEED wisdom</p>", 
                unsafe_allow_html=True)
    
    # Timer display
    show_timer_display(timer)
    
    # Controls
    show_controls(timer)
    
    # Check for timer completion
    current_time = time.time()
    if current_time - st.session_state.last_check > 0.5:  # Check every 500ms
        if timer.check_completion():
            # Timer phase completed
            if not st.session_state.notification_sent:
                # Play sound
                play_sound()
                
                # Get quotes for the new phase
                is_long_break = timer.phase.value == "long_break"
                st.session_state.current_quotes = quote_manager.get_break_quote(is_long_break)
                
                # Record statistics
                if timer.phase.value == "focus":
                    # Just finished a break, starting focus
                    pass
                elif timer.phase.value == "short_break":
                    # Finished focus, record pomodoro
                    stats_tracker.record_pomodoro(timer.config.focus_duration)
                    stats_tracker.record_break(timer.config.short_break_duration)
                    stats_tracker.record_cycle()
                else:  # long_break
                    stats_tracker.record_break(timer.config.long_break_duration, is_long=True)
                
                st.session_state.notification_sent = True
                st.rerun()
        else:
            st.session_state.notification_sent = False
        
        st.session_state.last_check = current_time
    
    # Auto-rerun for active timer
    if timer.is_running:
        time.sleep(0.1)
        st.rerun()
    
    # Show quotes if available
    if st.session_state.current_quotes:
        show_quotes()
    
    # Statistics
    show_stats()
    
    # Settings (conditional)
    if st.session_state.get('show_settings', False):
        show_settings()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6C757D; font-size: 0.9rem;'>"
        "SEED v6.0 · Built with Streamlit · "
        "<a href='https://github.com' style='color: #81B29A;'>GitHub</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()