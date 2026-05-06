import edge_tts
import asyncio
import pygame
import speech_recognition as sr
import os
import time
import tempfile
from config import VOICE_NAME, JARVIS_NAME

pygame.mixer.init()

async def _generate_audio(text: str, filename: str):
    communicate = edge_tts.Communicate(text, voice=VOICE_NAME)
    await communicate.save(filename)

def speak(text: str):
    if not text.strip():
        return
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        filename = tmp.name

        asyncio.run(_generate_audio(text, filename))

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        time.sleep(0.2)
        os.remove(filename)

    except Exception as e:
        print(f"[Voice error] {e}")

def listen(timeout=5, phrase_limit=10) -> str:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print(f"[{JARVIS_NAME}] Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )
            print(f"[{JARVIS_NAME}] Processing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        except Exception as e:
            print(f"[{JARVIS_NAME}] Mic error: {e}")
            return ""
