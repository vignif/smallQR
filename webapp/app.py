from flask import Flask, request, render_template
from smallest_qr import smallest_qr, manual_qr, decode
import base64
import time

app = Flask(__name__)

DEVELOPMENT_ENV = True

app_data = {
    "name": "Smallest QR Code Generator for links",
    "description": "This app allows you to create the smallest QR code given your input data. The generated QR code is held in memory, not stored on the disk. The default settings can be changed in case you would like to have a bigger QR code or you want to add some error correction.",
    "author": "Francesco Vigni",
    "html_title": "smallQR",
    "project_name": "SmallestQR",
    "keywords": "flask, webapp, qrcode, qr",
}

@app.route("/", methods=['GET', 'POST'])
def index():
    im = None
    err = False

    if request.method == 'POST':
        link = request.form.get('link')
        error = request.form.get('check')
        version = int(request.form.get('version', 0))
        t0 = time.time()
        minimal_version = None
        try:
            if version:
                im, err = manual_qr(link, version, error)
            else:
                im, minimal_version = smallest_qr(link, error=error)
            
            app_data["time"] = f"{time.time() - t0:.2f}"
            encoded_img_data = base64.b64encode(im).decode('utf-8') if not err else None

            if not err:
                sanity = decode(im)
            else:
                sanity = None
            print(sanity)
            print(encoded_img_data)
            print(minimal_version)
            
            content = {
                "app_data": app_data,
                "version": version,
                "minimal_version": minimal_version,
                "err": err,
                "error_level": error,
                "img_data": encoded_img_data,
                "input_string": link,
                "decoded_string": sanity,
            }

            return render_template("index.html", **content)
        except Exception as e:
            print(e)  # Log the exception
            # Handle the exception as needed, for now, let's proceed to rendering the template

    return render_template("index.html", app_data=app_data)

if __name__ == "__main__":
    app.run(debug=True)
