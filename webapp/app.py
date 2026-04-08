from flask import Flask, jsonify
import os, socket, redis

app = Flask(__name__)
cache = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379)

@app.route("/")
def index():
    try:
        visits = cache.incr("visits")
    except:
        visits = "unavailable"
    return f"<h1>GitHub Cloud Lab</h1><p>Visited <strong>{visits}</strong> times.</p>"

@app.route("/health")
def health():
    try:
        cache.ping()
        return jsonify({"status": "ok", "redis": "ok"})
    except Exception as e:
        return jsonify({"status": "ok", "redis": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
