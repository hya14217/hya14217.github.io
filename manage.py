import os
import json
import webbrowser
from gevent import pywsgi as wsgi
from pathlib import Path
from flask import Flask, request
from preprocess import preprocess
from hashlib import md5


HOST = "localhost"
PORT = 8088

def web_app():
    app = Flask(__name__, static_folder="static", static_url_path="/")

    def get_file_index():
        indices = []
        for img_file in Path("assets/upload/").glob("*.jpg"):
            idx = int(img_file.name.split(".")[0])
            indices.append(idx)
        indices.sort()
        prev_i = 0
        for i in indices:
            if i - prev_i > 1:
                return prev_i + 1
            prev_i = i
        return prev_i + 1

    @app.route("/upload", methods=["POST"])
    def upload():
        file = request.files["file"]
        content = file.stream.read()
        suffix = file.filename.split(".")[-1]
        filename = md5(content).hexdigest() + "." + suffix
        path = os.path.join("static/assets/upload", filename)
        with open(path, "wb") as fout:
            fout.write(content)
        preprocess(Path(path))
        return filename
    
    @app.route("/sync_photo_data", methods=["POST"])
    def sync_photo_data():
        photos = request.form["photos"]
        with open("data.js", "w", encoding="utf-8") as fout:
            fout.write("var photos=" + photos)
        os.system("commit.cmd")
        return photos
    
    @app.route("/")
    def index():
        with open("templates/index.html", "r", encoding="utf-8") as fin:
            return fin.read()

    webbrowser.open(f"http://{HOST}:{PORT}")
    server = wsgi.WSGIServer((HOST, PORT), app)
    server.serve_forever()
    return app


if __name__ == "__main__":
    app = web_app()
    server = wsgi.WSGIServer((HOST, PORT), app)
    server.serve_forever()
