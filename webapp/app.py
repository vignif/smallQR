"""Flask application entrypoint (kept for gunicorn import).

Refactored to use a service & utility layer. All heavy logic moved out
for easier testing and future extension.
"""
from __future__ import annotations
import logging
import os
import time
import base64
from typing import Any, Dict
from flask import Flask, request, render_template, session
from werkzeug.middleware.proxy_fix import ProxyFix

from config import get_config
from utils.captcha import generate_captcha, validate_captcha
from utils.counter import get_counter, increment_counter
from services.qr_service import generate_qr_min_version, generate_qr_manual, decode_qr

ConfigClass = get_config()

app = Flask(
    __name__,
    static_url_path="/smallqr/static",  # ensure path prefix for proxy
    static_folder="static",
    template_folder="templates",
)
app.config.from_object(ConfigClass)
app.secret_key = app.config["SECRET_KEY"]
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_prefix=1)

# Security & session hardening
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

app_data = {
    "name": "Smallest QR Code Generator for links",
    "description": "Effortlessly create ultra-compact, high-quality QR codes for your links or text. Fast, private, and beautifully simple. Just paste, click, and share your scannable magic.",
    "author": "Francesco Vigni",
    "html_title": "smallQR",
    "project_name": "SmallestQR",
    "keywords": "flask, webapp, qrcode, qr",
}

COUNTER_FILE = app.config["COUNTER_FILE"]
BASE_PATH = app.config["BASE_PATH"]
ALLOWED_ERROR_LEVELS = app.config["ALLOWED_ERROR_LEVELS"]
DEFAULT_ERROR_LEVEL = app.config["DEFAULT_ERROR_LEVEL"]
MAX_INPUT_LENGTH = app.config["MAX_INPUT_LENGTH"]


@app.route("/smallqr/", methods=["GET", "POST"])
def smallqr_index():  # pragma: no cover - proxy convenience
    return index()

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle QR generation UI."""
    state: Dict[str, Any] = {
        "version": 0,
        "minimal_version": None,
        "err": None,
        "error_level": None,
        "img_data": None,
        "input_string": None,
        "decoded_string": None,
        "time": None,
        "qr_count": get_counter(COUNTER_FILE),
        "captcha_question": None,
        "captcha_error": None,
    }

    # GET: issue captcha
    if request.method == "GET":
        q, a = generate_captcha()
        session["captcha_answer"] = a
        state["captcha_question"] = q
        return _render(state)

    # POST processing
    start = time.time()
    raw_input = (request.form.get("link", "") or "").strip()
    error_level = request.form.get("check", DEFAULT_ERROR_LEVEL)
    version = int(request.form.get("version", 0) or 0)
    captcha_input = request.form.get("captcha", "")
    expected = session.get("captcha_answer", "")

    # Always refresh captcha
    q_new, a_new = generate_captcha()
    session["captcha_answer"] = a_new
    state["captcha_question"] = q_new

    state["input_string"] = raw_input
    state["error_level"] = error_level
    state["version"] = version

    # Validation
    if not raw_input:
        state["err"] = "Input cannot be empty"
        return _render(state)
    if len(raw_input) > MAX_INPUT_LENGTH:
        state["err"] = f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters"
        return _render(state)
    if error_level not in ALLOWED_ERROR_LEVELS:
        state["err"] = "Invalid error correction level"
        return _render(state)
    if not validate_captcha(captcha_input, expected):
        state["captcha_error"] = "Captcha answer is incorrect. Please try again."
        return _render(state)

    try:
        if version:
            qr_bytes = generate_qr_manual(raw_input, version, error_level)
        else:
            qr_bytes, minimal_version = generate_qr_min_version(raw_input, error_level)
            state["minimal_version"] = minimal_version
        state["time"] = f"{time.time() - start:.2f}"
        state["img_data"] = base64.b64encode(qr_bytes).decode("utf-8")
        state["decoded_string"] = decode_qr(qr_bytes)
        state["qr_count"] = increment_counter(COUNTER_FILE)
    except Exception as exc:  # broad to surface error to user
        logging.exception("Error generating QR code")
        state["err"] = str(exc)

    return _render(state)


def _render(state: Dict[str, Any]):
    payload = {
        "app_data": app_data,
        "base_path": BASE_PATH,
        **state,
    }
    return render_template("index.html", **payload)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", app_data=app_data, base_path=BASE_PATH)


@app.after_request
def _security_headers(resp):  # pragma: no cover - header-level
    resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    # Allow current CDNs + data images (QR) - tighten later if self-hosting assets
    csp = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; "
        "script-src 'self' https://cdn.jsdelivr.net https://code.jquery.com; "
        "object-src 'none'; "
        "base-uri 'self'; form-action 'self'"
    )
    resp.headers.setdefault("Content-Security-Policy", csp)
    return resp


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    app.run(debug=app.config.get("DEBUG", False), host="0.0.0.0", port=app.config["PORT"])
