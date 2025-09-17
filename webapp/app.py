import logging
import os
import time
import base64
from flask import Flask, request, render_template, redirect, url_for
from smallest_qr import smallest_qr, manual_qr, decode
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Detect if running behind reverse proxy (Caddy)
BASE_PATH = os.environ.get("BASE_PATH", "/smallqr")

# Create Flask app
app = Flask(
    __name__,
    static_url_path="/smallqr/static",
    static_folder="static",
    template_folder="templates"
)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_prefix=1)

DEVELOPMENT_ENV = os.environ.get("FLASK_ENV", "production") != "production"

app_data = {
    "name": "Smallest QR Code Generator for links",
    "description": "This app allows you to create the smallest QR code given your input data.",
    "author": "Francesco Vigni",
    "html_title": "smallQR",
    "project_name": "SmallestQR",
    "keywords": "flask, webapp, qrcode, qr",
}

@app.route("/", methods=["GET", "POST"])
def index():
    img_data = None
    error_message = None
    minimal_version = None
    decoded_string = None
    version = 0
    error_level = None
    input_string = None
    elapsed_time = None

    if request.method == "POST":
        input_string = request.form.get("link", "")
        error_level = request.form.get("check", "L")
        version = int(request.form.get("version", 0))
        start_time = time.time()

        try:
            if version:
                qr_bytes, error_message = manual_qr(input_string, version, error_level)
            else:
                qr_bytes, minimal_version = smallest_qr(input_string, error=error_level)
                error_message = False

            elapsed_time = f"{time.time() - start_time:.2f}"
            img_data = base64.b64encode(qr_bytes).decode("utf-8") if qr_bytes and not error_message else None
            decoded_string = decode(qr_bytes) if qr_bytes and not error_message else None

        except Exception as e:
            app.logger.error(f"Error generating QR code: {e}")
            error_message = str(e)

    content = {
        "app_data": app_data,
        "version": version,
        "minimal_version": minimal_version,
        "err": error_message,
        "error_level": error_level,
        "img_data": img_data,
        "input_string": input_string,
        "decoded_string": decoded_string,
        "time": elapsed_time,
        "base_path": BASE_PATH,
    }

    return render_template("index.html", **content)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get("PORT", 8002))
    host = "0.0.0.0"
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host=host, port=port)
