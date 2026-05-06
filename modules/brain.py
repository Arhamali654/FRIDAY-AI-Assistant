from groq import Groq
from config import GROQ_API_KEY, AI_SYSTEM_PROMPT

client = None
conversation_history = []

def init_groq():
    global client, conversation_history
    client = Groq(api_key=GROQ_API_KEY)
    _load_memory_into_history()

def _load_memory_into_history():
    global conversation_history
    try:
        from modules.memory import get_recent_conversations
        recent = get_recent_conversations(limit=6)
        recent.reverse()
        for timestamp, user_input, jarvis_response in recent:
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            conversation_history.append({
                "role": "assistant",
                "content": jarvis_response
            })
    except Exception:
        pass

def think(prompt: str) -> str:
    global client, conversation_history

    if client is None:
        init_groq()

    conversation_history.append({
        "role": "user",
        "content": prompt
    })

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    messages = [{"role": "system", "content": AI_SYSTEM_PROMPT}] + conversation_history

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content.strip()

        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except Exception as e:
        err = str(e)
        if "401" in err or "api_key" in err.lower():
            return "Invalid Groq API key. Please check config.py."
        elif "429" in err or "rate" in err.lower():
            return "Groq rate limit hit. Please wait a moment and try again."
        elif "503" in err or "unavailable" in err.lower():
            return "Groq service temporarily unavailable. Try again shortly."
        else:
            return f"Brain error: {err}"

def clear_history():
    global conversation_history
    conversation_history = []
    return "Conversation history cleared."
