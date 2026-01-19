# ai_client.py
from openai import OpenAI
import os
from dotenv import load_dotenv
from personalidad import LLM  # tu prompt de "Justify"

load_dotenv()

# Nota: la variable estándar es OPENAI_API_KEY; tú usas API_KEY.
# Soportamos ambas por si ya tienes .env con API_KEY.
API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("No se encontró API_KEY/OPENAI_API_KEY en .env")

client = OpenAI(api_key=API_KEY)

def get_response(messages, model="gpt-4o-mini", max_tokens=250, temperature=0.4):
    """
    messages: lista de dicts tipo [{"role":"system"|"user"|"assistant","content":"..."}]
    """
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Hubo un problema consultando al modelo: {e}"


def build_messages_from(history, user_message):
    """
    Convierte tu historial del front a mensajes válidos del API.
    history: lista con objetos {role: 'user'|'bot'|'assistant'|'system', content: str}
    user_message: str
    """
    msgs = [{"role": "system", "content": LLM}]

    # Normalizamos roles del front:
    # - 'bot' -> 'assistant'
    # - 'user' -> 'user'
    # Ignoramos otros roles desconocidos.
    for m in history or []:
        role = m.get("role")
        content = m.get("content", "")
        if not content:
            continue
        if role == "bot":
            msgs.append({"role": "assistant", "content": content})
        elif role == "assistant":
            msgs.append({"role": "assistant", "content": content})
        elif role == "user":
            msgs.append({"role": "user", "content": content})

    # El mensaje actual del usuario al final:
    if user_message:
        msgs.append({"role": "user", "content": user_message})

    return msgs
