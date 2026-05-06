import edge_tts
import asyncio
import pygame
import os
import time

async def speak_test():
    text = "This is sentence one. This is sentence two. This is sentence three."
    communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural")
    await communicate.save("test_audio.mp3")

asyncio.run(speak_test())

pygame.mixer.init()
pygame.mixer.music.load("test_audio.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

pygame.mixer.music.unload()
time.sleep(0.5)
os.remove("test_audio.mp3")
print("Done!")