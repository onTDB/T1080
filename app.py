from flask import *
from flask_cors import CORS
import os
from streamlink import streams
import requests

app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)

@app.route('/<path:path>')
def static_file(path):
    s = streams("https://www.twitch.tv/" + path.replace(".m3u8", ""))
    if s:
        return requests.get(s["best"].url_master).content, 200
    else:
        return "Can not find channel", 404

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=8888)