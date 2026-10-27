import threading
import queue

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False

class SanctumVoiceEngine:
    def __init__(self):
        self.state = "idle"
        self.audio_queue = queue.Queue()
        self.is_speaking = False
        self.engine = None
        
        if HAS_PYTTSX3:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 175)
            except Exception as e:
                print(f"⚠️ Voice Engine initialization warning: {e}")

    def set_state(self, new_state: str):
        """Updates and displays Dreamwalker's current astral state."""
        self.state = new_state
        print(f"✨ [State: {self.state.upper()}]")

    def speak(self, text: str):
        """Streams Oracle response out via text-to-speech if available."""
        if not text:
            return

        self.set_state("speaking")
        self.is_speaking = True
        
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Speech output error: {e}")
        
        self.is_speaking = False
        self.set_state("idle")

    def sever_tether(self):
        """B2: Instantly interrupts speaking and clears queued audio."""
        if self.engine and self.is_speaking:
            try:
                self.engine.stop()
            except Exception:
                pass
        with self.audio_queue.mutex:
            self.audio_queue.queue.clear()
        self.set_state("idle")
        print("⚡ Tether severed: Audio queue cleared.")