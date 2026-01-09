import os
import threading
import time
from TTS.api import TTS
import platform
import subprocess

# Optional simpleaudio
try:
    import simpleaudio as sa
    SIMPLEAUDIO_AVAILABLE = True
except ImportError:
    SIMPLEAUDIO_AVAILABLE = False

class TTSManager:
    """
    Async TTS manager using Coqui TTS.
    Adds a slight delay before playback to avoid cut-off.
    """
    def __init__(self, delay_before_playback: float = 0.1):
        # Force Coqui TTS to store models in project folder
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(project_dir, "models")
        os.makedirs(models_dir, exist_ok=True)
        os.environ["TTS_HOME"] = models_dir

        # Initialize TTS
        self.tts = TTS(model_name="tts_models/en/ljspeech/neural_hmm", progress_bar=False, gpu=False)
        self.delay = delay_before_playback  # seconds

    def speak(self, text: str):
        threading.Thread(target=self._play, args=(text,), daemon=True).start()

    def _play(self, text: str):
        tmp_path = os.path.join("/tmp", "tts_output.wav") if platform.system() != "Windows" else os.path.join(os.getenv("TEMP", "."), "tts_output.wav")
        try:
            # Generate WAV file
            self.tts.tts_to_file(text=text, file_path=tmp_path)

            # Add slight delay before starting playback
            time.sleep(self.delay)

            # Play via simpleaudio if available
            if SIMPLEAUDIO_AVAILABLE:
                try:
                    wave_obj = sa.WaveObject.from_wave_file(tmp_path)
                    play_obj = wave_obj.play()
                    play_obj.wait_done()
                    return
                except Exception as e:
                    print(f"[TTS WARNING] simpleaudio playback failed: {e}")

            # Linux fallback
            if platform.system() == "Linux":
                try:
                    subprocess.run(["aplay", tmp_path], check=True)
                    return
                except Exception as e:
                    print(f"[TTS WARNING] aplay playback failed: {e}")

            # Windows fallback
            if platform.system() == "Windows":
                try:
                    os.startfile(tmp_path)
                    return
                except Exception as e:
                    print(f"[TTS WARNING] Windows playback failed: {e}")

            # macOS fallback
            if platform.system() == "Darwin":
                try:
                    subprocess.run(["afplay", tmp_path], check=True)
                    return
                except Exception as e:
                    print(f"[TTS WARNING] macOS playback failed: {e}")

            print(f"[TTS ERROR] No playback method available for your platform.")

        except Exception as e:
            print(f"[TTS ERROR] Generating TTS failed: {e}")