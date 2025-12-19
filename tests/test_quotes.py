"""
Tests for quotes.py
"""

import pytest
from src.quotes import QuoteManager, Voice, QUOTES, voice_key_to_enum


class TestQuoteManager:
    """Test QuoteManager class."""
    
    def test_initialization(self):
        manager = QuoteManager()
        assert len(manager.used_quotes) == len(Voice)
        for voice in Voice:
            assert voice in manager.used_quotes
            assert manager.used_quotes[voice] == []
    
    def test_get_quote(self):
        manager = QuoteManager()
        
        # Get a quote for each voice
        for voice in Voice:
            quote = manager.get_quote(voice)
            assert quote in QUOTES[voice]
            assert quote in manager.used_quotes[voice]
    
    def test_quote_rotation(self):
        manager = QuoteManager()
        voice = Voice.SOLEA
        
        # Get all quotes
        quotes_used = []
        for _ in range(len(QUOTES[voice])):
            quote = manager.get_quote(voice)
            quotes_used.append(quote)
        
        # Should have used all quotes
        assert set(quotes_used) == set(QUOTES[voice])
        
        # Next quote should be from the beginning again (after reset)
        quote = manager.get_quote(voice)
        assert quote in QUOTES[voice]
    
    def test_recent_quote_avoidance(self):
        manager = QuoteManager()
        voice = Voice.NYRA
        
        # Get first quote
        quote1 = manager.get_quote(voice)
        assert len(manager.used_quotes[voice]) == 1
        
        # Get second quote (should not repeat immediately)
        quote2 = manager.get_quote(voice)
        assert quote2 != quote1
        assert len(manager.used_quotes[voice]) == 2
    
    def test_get_break_quote_short(self):
        manager = QuoteManager()
        
        quotes = manager.get_break_quote(is_long_break=False)
        
        # Should have exactly one voice
        assert len(quotes) == 1
        
        # Check format
        for voice_str, quote in quotes.items():
            voice = voice_key_to_enum(voice_str)
            assert quote in QUOTES[voice]
    
    def test_get_break_quote_long(self):
        manager = QuoteManager()
        
        quotes = manager.get_break_quote(is_long_break=True)
        
        # Should have quotes from all voices
        assert len(quotes) == len(Voice)
        
        for voice_str, quote in quotes.items():
            voice = voice_key_to_enum(voice_str)
            assert quote in QUOTES[voice]
    
    def test_reset(self):
        manager = QuoteManager()
        
        # Use some quotes
        manager.get_quote(Voice.SOLEA)
        manager.get_quote(Voice.NYRA)
        
        # Reset
        manager.reset()
        
        # Should be empty again
        for voice in Voice:
            assert manager.used_quotes[voice] == []


class TestQuotesDatabase:
    """Test the quotes database."""
    
    def test_quotes_structure(self):
        assert len(QUOTES) == len(Voice)
        
        for voice in Voice:
            assert voice in QUOTES
            assert isinstance(QUOTES[voice], list)
            assert len(QUOTES[voice]) > 0
            
            # Check each quote is a non-empty string
            for quote in QUOTES[voice]:
                assert isinstance(quote, str)
                assert len(quote.strip()) > 0
    
    def test_voice_enum(self):
        assert Voice.SOLEA.value == "Soléa"
        assert Voice.NYRA.value == "Nyra"
        assert Voice.VOX.value == "VOX"
        assert Voice.ATLAS.value == "Atlas"
