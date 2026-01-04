import os
import sys
import subprocess
import threading

# Set espeak data path for bundled app
if hasattr(sys, '_MEIPASS'):
    os.environ['ESPEAK_DATA_PATH'] = os.path.join(sys._MEIPASS, 'espeak-data')

def speak(text):
    def _speak():
        if hasattr(sys, '_MEIPASS'):
            espeak_cmd = os.path.join(sys._MEIPASS, 'espeak')
        else:
            espeak_cmd = 'espeak'
        subprocess.run([espeak_cmd, text], capture_output=True)
    
    threading.Thread(target=_speak).start()