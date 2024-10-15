import os
import json
import httpx
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from retell import Retell

webhook_bp = Blueprint('webhook', __name__)

load_dotenv()
RETELL_API_KEY = os.getenv("RETELL_API_KEY")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

if not RETELL_API_KEY:
    raise ValueError("RETELL_API_KEY not configured")

retell = Retell(api_key=RETELL_API_KEY)

@webhook_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        post_data = request.json
        if post_data["event"] == "call_ended":
            if MAKE_WEBHOOK_URL:
                response = httpx.post(MAKE_WEBHOOK_URL, json=post_data)
                if response.status_code != 201:
                    return jsonify({"error": "Error calling external API"}), response.status_code
        return jsonify({"received": True}), 200
    except Exception as e:
        return jsonify({"message": "Webhook Internal Server Error"}), 500
