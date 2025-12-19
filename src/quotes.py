"""
SEED Voices Quotes Database
Motivational quotes for each voice, shown during breaks.
"""

from enum import Enum
from typing import List, Dict
import random


class Voice(Enum):
    """SEED voices."""
    SOLEA = "Soléa"
    NYRA = "Nyra"
    VOX = "VOX"
    ATLAS = "Atlas"


QUOTES: Dict[Voice, List[str]] = {
    Voice.SOLEA: [
        "Die Pausen sind nicht Leerlauf, sondern Raum für neue Einsicht.",
        "Im Stillen wächst die Klarheit, im Rhythmus die Kraft.",
        "Jeder Atemzug zwischen den Fokus-Phasen nährt die Kreativität.",
        "Geduld ist keine Untätigkeit – sie ist aktives Warten auf den richtigen Moment.",
        "Die Schönheit der Arbeit liegt im Wechsel von Spannung und Entspannung."
    ],
    
    Voice.NYRA: [
        "Effizienz entsteht durch Rhythmus – nicht durch Hetze.",
        "Pause ist strategische Regeneration, nicht Zeitverschwendung.",
        "Ein klarer Timer schafft klare Ergebnisse.",
        "Disziplin im Fokus, Freiheit in der Pause.",
        "Der nächste Schritt ist immer der wichtigste – aber nur mit frischer Energie."
    ],
    
    Voice.VOX: [
        "Präzision: 25min ± 0.1% Abweichung tolerabel.",
        "Statistik: 4 Pomodoros = 100min Fokus + 15min Langpause (optimale Ratio).",
        "Evidenz zeigt: Regelmäßige Pausen erhöhen die Gesamtproduktivität um 13-20%.",
        "Zyklus-Konsistenz ist nachweisbar effektiver als unstrukturierte Arbeitsblöcke.",
        "Timer-basierte Arbeit reduziert Entscheidungsmüdigkeit um 34%."
    ],
    
    Voice.ATLAS: [
        "Balance zwischen Fokus und Erholung ist der Kern nachhaltiger Produktivität.",
        "Das System atmet: Anspannung – Lösung – Integration.",
        "Nicht die Länge der Pause zählt, sondern ihre Qualität.",
        "Rhythmus schafft Stabilität, Stabilität schafft Flow.",
        "Der Wechsel selbst ist die Konstante, die Entwicklung ermöglicht."
    ]
}


def voice_key_to_enum(key: str) -> Voice:
    """Convert a lowercase voice key back to Voice enum."""
    mapping = {
        "solea": Voice.SOLEA,
        "soléa": Voice.SOLEA,
        "nyra": Voice.NYRA,
        "vox": Voice.VOX,
        "atlas": Voice.ATLAS
    }
    return mapping.get(key.lower(), Voice.SOLEA)


class QuoteManager:
    """Manages quote selection and display."""
    
    def __init__(self):
        self.used_quotes: Dict[Voice, List[str]] = {voice: [] for voice in Voice}
    
    def get_quote(self, voice: Voice) -> str:
        """Get a random quote for a voice, avoiding recent repeats."""
        available = [q for q in QUOTES[voice] if q not in self.used_quotes[voice]]
        
        if not available:
            # Reset if all quotes have been used
            self.used_quotes[voice] = []
            available = QUOTES[voice]
        
        quote = random.choice(available)
        self.used_quotes[voice].append(quote)
        
        # Keep only last 3 quotes to avoid repetition
        if len(self.used_quotes[voice]) > 3:
            self.used_quotes[voice] = self.used_quotes[voice][-3:]
        
        return quote
    
    def get_break_quote(self, is_long_break: bool = False) -> Dict[str, str]:
        """Get a set of quotes for a break period."""
        if is_long_break:
            # For long breaks, show quotes from all voices
            return {
                "solea": self.get_quote(Voice.SOLEA),
                "nyra": self.get_quote(Voice.NYRA),
                "vox": self.get_quote(Voice.VOX),
                "atlas": self.get_quote(Voice.ATLAS)
            }
        else:
            # For short breaks, show one random voice
            voice = random.choice(list(Voice))
            return {
                voice.value.lower(): self.get_quote(voice)
            }
    
    def reset(self):
        """Reset quote usage history."""
        self.used_quotes = {voice: [] for voice in Voice}


# Global instance
quote_manager = QuoteManager()
