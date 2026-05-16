from datetime import datetime
from flask import Flask, jsonify
from db.models import get_today_top

app = Flask(__name__)


@app.route("/digest")
def digest():
    items = get_today_top(limit=5)
    return jsonify({
        "date":      datetime.utcnow().date().isoformat(),
        "top_items": items,
        "count":     len(items),
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})
