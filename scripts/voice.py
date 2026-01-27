# Voice utilities for speech-to-text and text-to-speech

from __future__ import annotations

import asyncio
import io
import os
import tempfile
from pathlib import Path
from typing import Optional

# TTS
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

# STT - using SpeechRecognition library with Google API
try:
    import speech_recognition as sr
    HAS_WHISPER = True  
except ImportError:
    HAS_WHISPER = False


# Default voices for edge-tts
VOICE_OPTIONS = {
    "English (Female)": "en-US-JennyNeural",
    "English (Male)": "en-US-GuyNeural",
}

DEFAULT_VOICE = "en-US-JennyNeural"


class SpeechToText:
    
    def __init__(self, model_size: str = "base", device: str = "cpu"):
        if not HAS_WHISPER:
            raise RuntimeError("SpeechRecognition not installed.")
        
        self.recognizer = sr.Recognizer()
    
    def transcribe(self, audio_bytes: bytes) -> str:
        # Save audio to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        
        try:
            with sr.AudioFile(temp_path) as source:
                audio_data = self.recognizer.record(source)
            
            # Use Google's free speech recognition API
            text = self.recognizer.recognize_google(audio_data)
            return text.strip()
        except sr.UnknownValueError:
            return ""  # Speech not understood
        except sr.RequestError as e:
            return f"[Error: {e}]"
        finally:
            # Cleanup temp file
            os.unlink(temp_path)


class TextToSpeech:    
    def __init__(self, voice: str = DEFAULT_VOICE):
        if not HAS_EDGE_TTS:
            raise RuntimeError("edge-tts not installed.")
        self.voice = voice
    
    async def _synthesize_async(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(text, self.voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data
    
    def synthesize(self, text: str) -> bytes:
        # Run async code in sync context
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self._synthesize_async(text))
                return future.result()
        else:
            return loop.run_until_complete(self._synthesize_async(text))
    
    def set_voice(self, voice: str):
        self.voice = voice


def check_voice_dependencies() -> dict:
    return {
        "stt": HAS_WHISPER,
        "tts": HAS_EDGE_TTS,
    }


__all__ = [
    "SpeechToText", 
    "TextToSpeech", 
    "VOICE_OPTIONS", 
    "DEFAULT_VOICE",
    "check_voice_dependencies",
    "HAS_WHISPER",
    "HAS_EDGE_TTS",
]
