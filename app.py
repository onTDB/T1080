from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask import Flask, request
from streamlink import Streamlink
from gc import collect
import requests
import os

server = "SRVNAME"
app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)
session = Streamlink()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
error = "<html><head><title>{status}</title></head><body><center><h1>{status}</h1></center><hr><center>{server}</center></body></html>"

@app.after_request
def after_request(response):
    response.headers.add('LBServer', server)
    return response

@app.errorhandler(404)
def notfound(e):
    return error.format(status="404 Not Found", server=server), 404

@app.route('/<path:path>')
def static_file(path):
    s = session.streams("https://www.twitch.tv/" + path.replace(".m3u8", ""))
    if s:
        try:
            quality = request.args.get("quality")
            rtn = s[quality].url
            status = 200
        except:
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