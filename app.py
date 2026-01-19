#pip # app.py
from flask import Flask, render_template, request, jsonify
from chat import get_response, build_messages_from
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # ajusta origins en prod

@app.route("/")
def index():
    return render_template("indexv3.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/login")
def login():
    return render_template("loginv2.html")

# === NUEVO: endpoint JSON del chatbot ===
@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []  # historial del front

    if not user_message:
        return jsonify({"error": "Falta 'message'"}), 400

    messages = build_messages_from(history, user_message)
    reply = get_response(messages)

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    # En prod usa un servidor WSGI/ASGI (gunicorn/uvicorn+asgiref)
    app.run(debug=True)
