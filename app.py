from werkzeug.middleware.proxy_fix import ProxyFix
from streamlink import streams
from threading import Thread
from flask_cors import CORS
from flask import Flask
from time import sleep
import requests
import os
class storage(): pass

app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)
storage = storage()
storage.count = 0

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/<path:path>')
def static_file(path):
    if path == "restart": 
        storage.count = 200
        return str(storage.count), 200
    elif path == "count":
        return str(storage.count), 200
    elif path == "favicon.ico":
        return "", 404
    storage.count += 1
    s = streams("https://www.twitch.tv/" + path.replace(".m3u8", ""))
    if s:
        rtn = requests.get(s["best"].url_master).content
        status = 200
    else:
        rtn = "Can not find channel"
        status = 404
    return rtn, status

if __name__ == '__main__':
    if "T1080" not in os.popen("screen -ls | grep -oP '(?<=\.)\w+'").read().split("\n"):
        os.system(f"screen -dmS T1080 python3 {os.path.realpath(__file__)}")
        print("T1080 is started in screen")
        exit()
    app.debug = True
    mainapp = Thread(target=app.run, kwargs={"host": "0.0.0.0", "threaded": True, "port": 8888, "use_reloader": False})
    mainapp.daemon = True
    mainapp.start()
    while storage.count < 200:
        sleep(1)
    os.system(f"screen -dmS T1080 python3 {os.path.realpath(__file__)}")
    exit()
