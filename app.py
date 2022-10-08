from flask import *
from flask_compress import Compress
import os
from streamlink import streams
import requests

class stream():
    def __init__(self):
        self.threads = {}
        self.data = {}
        self.requests = {}
        pass

    def stream(self):
        while True:
            yield "Hello World"
    
    def resp(self, path):
        if not path.endswith(".m3u8"):
            pass
        return 0
    
    def manager(self, name):
        pass

    def onNewLoad(self, path):
        loaded = False
        data = {}
        req = {}
        username = path.replace(".m3u8", "")
        if username in self.data:
            return self.data[username]["m3u8"]

        s = streams("https://www.twitch.tv/" + username)
        if s:
            m3u8 = requests.get(s["best"].url_master).text.split("\n")
            for i in m3u8:
                print(i)
                ##EXT-X-MEDIA
                if i.startswith("#EXT-X-MEDIA"):
                    i = i.replace("#EXT-X-MEDIA:", "").replace('"', "").split(",")
                    for j in i:
                        j = j.split("=")
                        if j[0] == "NAME":
                            if j[1] == "audio_only":
                                del(m3u8[m3u8.index(i)+2])
                                del(m3u8[m3u8.index(i)+1])
                                del(m3u8[m3u8.index(i)])
                                continue
                            elif " (source)" in j[1]:
                                j[1] = j[1].replace(" (source)", "")
                            name = j[1]
                            req.update({name: 0})
                            loaded = True
                if loaded:
                    if i.startswith("http"): data.update({name: i})
                    m3u8[m3u8.index(i)] = "http://api1080.ontdb.com/stream_{username}_{quality}.m3u8".format(username=username, quality=name)
                    loaded = False

            data.update({"m3u8": "\n".join(m3u8)})
            self.data.update({username: data})

            return data["m3u8"]
        else:
            return "Stream not found"

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)
stream = stream()

@app.route('/<path:path>')
def static_file(path):
    if "stream_" in path:
        return stream.resp(path)
    else:
        return stream.onNewLoad(path)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=8888)