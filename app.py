from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask import Flask
from streamlink import streams
from gc import collect
import requests
import os


app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/<path:path>')
def static_file(path):
    s = streams("https://www.twitch.tv/" + path.replace(".m3u8", ""))
    if s:
        rtn = requests.get(s["best"].url_master).content
        status = 200
    else:
        rtn = "Can not find channel"
        status = 404
    
    del(s)
    collect()
    return rtn, status

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=8888)