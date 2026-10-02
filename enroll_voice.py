import os
import shutil

# Monkey-patch os.symlink to avoid Windows Admin privileges error (WinError 1314)
def dummy_symlink(src, dst, target_is_directory=False):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    except FileExistsError:
        pass
os.symlink = dummy_symlink

import torch
import torchaudio
import sounddevice as sd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from speechbrain.inference.speaker import SpeakerRecognition

from voice import capture_speech_audio

def enroll():
    print("========================================")
    print("     JARVIS VOICE ENROLLMENT SYSTEM     ")
    print("========================================")
    print("Please say the following phrase clearly:")
    print("\n'Jarvis, I am the authorized user of this system. Please record my voice print for biometric verification.'\n")
    
    input("Press Enter when you are ready to start recording...")
    
    audio_data = capture_speech_audio()
    if audio_data is None:
        print("Failed to capture audio.")
        return
    print("Downloading/Loading neural network for extraction... (This may take a moment the first time)")
    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", 
        savedir="tmp_model",
        run_opts={"device": "cpu"}
    )
    
    # Extract embedding directly from memory
    signal = torch.tensor(audio_data).unsqueeze(0)
    embeddings = verification.encode_batch(signal)
    
    # Save the embedding tensor
    torch.save(embeddings, "master_voice_print.pt")
    
    print("\n[SUCCESS] Voice print securely saved as 'master_voice_print.pt'")
    print("Jarvis will now use this to verify your identity.")

if __name__ == "__main__":
    enroll()
