import sys
import os
import keyboard

# Inject CUDA 12 DLLs into PATH for faster-whisper/ctranslate2
# Use absolute paths to ensure the DLLs are found regardless of how Python is launched
current_dir = os.path.dirname(os.path.abspath(__file__))
venv_bin_cublas = os.path.join(current_dir, "..", r"venv\Lib\site-packages\nvidia\cublas\bin")
venv_bin_cudnn = os.path.join(current_dir, "..", r"venv\Lib\site-packages\nvidia\cudnn\bin")

if os.path.exists(venv_bin_cublas):
    os.environ["PATH"] = venv_bin_cublas + ";" + os.environ["PATH"]
if os.path.exists(venv_bin_cudnn):
    os.environ["PATH"] = venv_bin_cudnn + ";" + os.environ["PATH"]

# Set up global hotkey listener for Ctrl+Space
ctrl_space_pressed = False
def on_ctrl_space():
    global ctrl_space_pressed
    ctrl_space_pressed = True

def consume_hotkey():
    global ctrl_space_pressed
    if ctrl_space_pressed:
        ctrl_space_pressed = False
        return True
    return False

def on_ctrl_esc():
    import os
    print("\n[System] Ctrl+Esc pressed. Force quitting...")
    os._exit(0)

keyboard.add_hotkey('ctrl+space', on_ctrl_space)
keyboard.add_hotkey('ctrl+esc', on_ctrl_esc)

from faster_whisper import WhisperModel
import warnings
import asyncio
import edge_tts
import pygame
import keyboard
import sounddevice as sd
import numpy as np
import time
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
import random
try:
    from speechbrain.inference.speaker import SpeakerRecognition
except ImportError:
    pass

voice_verifier = None
master_embedding = None
require_strict_verification = True
def init_voice_verification():
    global voice_verifier, master_embedding
    if os.path.exists("master_voice_print.pt"):
        if voice_verifier is None:
            print("\n[Loading Voice Biometrics Engine...]")
            # Force CPU to avoid CUDA deadlocks with faster-whisper
            voice_verifier = SpeakerRecognition.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb", 
                savedir="tmp_model", 
                run_opts={"device": "cpu"}
            )
            master_embedding = torch.load("master_voice_print.pt", map_location=torch.device('cpu'))

# Suppress some noisy warnings from faster-whisper/CTranslate2
warnings.filterwarnings("ignore")

# ==========================================
# 1. TEXT-TO-SPEECH (TTS) SETUP
# ==========================================

def speak(text: str):
    """Speaks the given text using Edge TTS and allows interruption."""
    print(f"\n[Jarvis Speaking]: {text}")
    print("[Press 'Esc' to interrupt]")
    
    try:
        temp_file = "temp_response.mp3"
        
        async def generate_audio():
            # Using a sophisticated British male voice (en-GB-RyanNeural) and slightly reduced speed for a composed delivery
            communicate = edge_tts.Communicate(text, "en-GB-RyanNeural", rate="-5%")
            await communicate.save(temp_file)
            
        asyncio.run(generate_audio())
        
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            if keyboard.is_pressed('esc'):
                pygame.mixer.music.stop()
                print("\n[Interrupted]")
                break
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
                
    except Exception as e:
        print(f"TTS Error: {e}")


# ==========================================
# 2. SPEECH-TO-TEXT (STT) SETUP (Local Free)
# ==========================================
# Using 'small' for much higher accuracy with accents and non-english names. 
model_size = "small" 
# Running on GPU for high performance
whisper_model = WhisperModel(model_size, device="cuda", compute_type="float16")

def capture_speech_audio():
    """Listens to the microphone and returns a numpy array of speech, trimming silence."""
    SAMPLE_RATE = 16000
    CHUNK_DURATION = 0.05 # seconds, much finer grain for catching speech exactly
    CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
    SILENCE_DURATION = 2.0
    
    print("\n[Jarvis is calibrating your microphone...]")
    # First, capture 1 second of background noise to set a baseline
    try:
        noise = sd.rec(int(SAMPLE_RATE * 1), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        baseline_energy = np.mean(np.abs(noise))
        energy_threshold = max(baseline_energy * 2.5, 0.002) # Must be at least 2.5x louder than noise
    except Exception as e:
        print(f"Mic error: {e}")
        return None
        
    print("\n[Jarvis is Listening...]")
    
    import collections
    pre_roll_buffer = collections.deque(maxlen=10) # 0.5 seconds of pre-roll
    audio_buffer = []
    is_speaking = False
    silence_time = 0.0
    wait_time = 0.0
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
        while True:
            chunk, overflow = stream.read(CHUNK_SIZE)
            energy = np.mean(np.abs(chunk))
            
            # Detect speech vs silence
            if energy > energy_threshold:
                if not is_speaking:
                    # Just started speaking, append the pre-roll first to capture the very beginning
                    for pre_chunk in pre_roll_buffer:
                        audio_buffer.append(pre_chunk)
                is_speaking = True
                silence_time = 0.0
            else:
                if is_speaking:
                    silence_time += CHUNK_DURATION
                else:
                    wait_time += CHUNK_DURATION
                    
            # If they haven't said anything for 7 seconds, give up
            if not is_speaking and wait_time > 7.0:
                print("(Debug: Listening timed out after 7 seconds of silence.)")
                return None
                
            if is_speaking:
                audio_buffer.append(chunk.flatten())
                if not getattr(stream, "printed_hearing", False):
                    sys.stdout.write("[Hearing speech...]\r")
                    sys.stdout.flush()
                    stream.printed_hearing = True
            else:
                pre_roll_buffer.append(chunk.flatten())
                
            # Stop listening if they pause for too long
            if is_speaking and silence_time > SILENCE_DURATION:
                sys.stdout.write("\n[Processing final audio...]\n")
                break
                
    if audio_buffer:
        return np.concatenate(audio_buffer)
    return None

def listen() -> str:
    """Listens to the microphone continuously and transcribes live to the console using local CPU."""
    audio_data = capture_speech_audio()
    if audio_data is None:
        return ""
        
    final_text = ""
    # Voice Biometrics (Speaker Recognition) has been disabled per user request

    try:
        # Force language="en" to stop Whisper from getting confused and switching languages.
        # Updated the initial_prompt to prime the model for an Indian English accent.
        segments, info = whisper_model.transcribe(
            audio_data, 
            beam_size=5, 
            language="en",
            initial_prompt="Jarvis, a sophisticated AI assistant, is listening to the user's commands. The user speaks with an Indian English accent and may use some common Indian words."
        )
        text = "".join([segment.text for segment in segments]).strip()
        
        # --- Auto-Correction Logic ---
        corrections = {
            "here are u": "how are u",
            "here are you": "how are you",
            "read me large emails": "read me last emails"
        }
        import re
        for wrong, right in corrections.items():
            text = re.sub(rf'\b{wrong}\b', right, text, flags=re.IGNORECASE)
            
        print(f"[Heard]: {text}")
        final_text = text
        
    except Exception as e:
        print(f"Transcription Error: {e}")
        final_text = ""
        
    return final_text
