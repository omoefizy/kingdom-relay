import os, json, urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    payload = json.dumps({
        "chat_id": data["chat_id"],
        "text": data["text"],
        "message_thread_id": data["message_thread_id"],
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    return jsonify(json.loads(resp.read()))

@app.route("/")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
