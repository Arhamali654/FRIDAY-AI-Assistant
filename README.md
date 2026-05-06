# 🤖 FRIDAY — AI Desktop Assistant

> An Iron Man-style AI assistant built with Python. Speaks. Remembers. Acts.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Groq](https://img.shields.io/badge/AI-Groq%20API-orange) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features
- 🧠 **Groq API (Llama 3.3 70B)** — conversational AI brain
- 🗣️ **Edge-TTS + Pygame** — natural human-like voice output
- 💾 **SQLite Memory** — remembers past conversations
- 🌤️ **Weather Module** — real-time weather updates
- 🎵 **Music Control** — Spotify integration
- ⏰ **Reminders & Timers** — voice-based scheduling
- 🖥️ **Screen Reader** — reads and describes your screen
- 🤖 **Autopilot Module** — controls your PC by voice
- 🖼️ **Animated Arc Reactor UI** — built with CustomTkinter

## 🛠️ Tech Stack
`Python 3.11` · `Groq API` · `CustomTkinter` · `Edge-TTS` · `SQLite` · `Pygame` · `Spotify API` · `OpenWeather API`

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/Arhamali654/FRIDAY-AI-Assistant.git
cd FRIDAY-AI-Assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
GROQ_API_KEY=your_groq_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
NEWS_API_KEY=your_news_api_key_here

### 4. Run FRIDAY
```bash
python main.py
```

## 🎮 Modes
| Mode | Description |
|------|-------------|
| Wake Word | Say "Friday" to activate |
| Continuous | Speak freely without wake word |
| Text | Type commands instead of speaking |

## 📁 Project Structure
FRIDAY-AI-Assistant/
│
├── main.py              # Entry point
├── config.py            # Configuration (uses .env)
├── friday_ui.py         # Arc Reactor UI
├── .env.example         # Template for API keys
│
├── modules/
│   ├── brain.py         # Groq AI logic
│   ├── voice.py         # Speech input/output
│   ├── memory.py        # SQLite conversation memory
│   ├── weather.py       # Weather commands
│   ├── music.py         # Spotify music control
│   ├── reminder.py      # Reminders & timers
│   ├── screen.py        # Screen reading
│   ├── autopilot.py     # PC automation
│   └── system.py        # System commands
│
└── ui/
└── dashboard.py     # UI components

## 📌 Planned Features
- 📧 Gmail & Google Calendar integration
- 📱 WhatsApp by voice
- 🌐 Urdu/English bilingual support
- 📊 Progress bar & multi-file support

## 👨‍💻 Author
**Arham Ali** — CS Student @ SZABIST Hyderabad  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/arham-ali-a76055225)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Arhamali654)

## 📄 License
This project is open source under the [MIT License](LICENSE).
