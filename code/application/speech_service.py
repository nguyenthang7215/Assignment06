class SpeechService:
    """Assignment-compliant speech-to-text simulation."""

    def transcribe(self, audio_input: str) -> str:
        if not audio_input.strip():
            raise ValueError("The simulated voice transcript cannot be empty.")
        return audio_input.strip()

