# ─── FRIDAY Configuration ─────────────────────────────────────────────────────
from dotenv import load_dotenv
import os

load_dotenv()

JARVIS_NAME = "FRIDAY"
WAKE_WORD   = "friday"

# ─── AI Brain (Groq) ──────────────────────────────────────────────────────────
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")
AI_SYSTEM_PROMPT = (
    "You are FRIDAY, an advanced AI assistant inspired by Tony Stark's FRIDAY. "
    "You are intelligent, efficient, and slightly witty. Keep responses concise and helpful. "
    "You are running locally on the user's PC."
)

# ─── Voice settings ───────────────────────────────────────────────────────────
SPEECH_RATE   = 175
SPEECH_VOLUME = 1.0
VOICE_INDEX   = 0
VOICE_NAME    = "en-US-AriaNeural"

# ─── Weather & News ───────────────────────────────────────────────────────────
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_CITY        = "Hyderabad"
NEWS_API_KEY        = os.getenv("NEWS_API_KEY")

# ─── Spotify ──────────────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI  = os.getenv("SPOTIFY_REDIRECT_URI")

# ─── Tesseract OCR ────────────────────────────────────────────────────────────
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(BASE_DIR, "data", "memory.db")
MUSIC_DIR  = os.path.join(os.path.expanduser("~"), "Music")