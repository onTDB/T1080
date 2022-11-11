from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask import Flask
from streamlink import Streamlink
from gc import collect
import requests
import os

server = "SRVNAME"
app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)
session = Streamlink()

app.token = ""
app.clientid = ""
app.clientsecret = ""


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
    if "vod/" in path:
        try:
            s = session.streams("https://www.twitch.tv/videos/" + path.split("/")[-1].replace(".m3u8", ""))
        except:
            #print("Using API")
            return twitch(path.split("/")[-1].replace(".m3u8", ""))
    else:
        s = session.streams("https://www.twitch.tv/" + path.split("/")[-1].replace(".m3u8", ""))
    if s:
        rtn = requests.get(s["best"].url_master).content
        status = 200
    else:
        rtn = "Can not find channel"
        status = 404
    
    del(s)
    collect()
    return rtn, status

def twitch_generate():
    rtn = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={app.clientid}&client_secret={app.clientsecret}&grant_type=client_credentials").json()
    app.token = rtn["access_token"]

def twitch(videoid):
    if not app.token: twitch_generate()
    print(app.clientid, app.clientsecret, app.token)
    data = requests.get(f"https://api.twitch.tv/helix/videos?id={videoid}", headers={"Client-ID": app.clientid, "Authorization": f"Bearer {app.token}"}).json()
    print(data)
    s = data["data"][0]["thumbnail_url"].split("/")
    region = s[4]
    videouid = s[5]
    qual = {}
    
    cloudfront = "https://{region}.cloudfront.net/{videouid}/{quality}/index-dvr.m3u8"
    qualities = ["chunked", "1080p60", "1080p30", "720p60", "720p30", "480p30", "360p30", "160p30"] #"2160p60", "2160p30", "1440p60", "1440p30", 
    check = False
    for quality in qualities:
        url = cloudfront.format(region=region, videouid=videouid, quality=quality)
        if requests.get(url).status_code == 200:
            if check == True: 
                chunked = "1080p60" if quality == "720p60" else "720p60" if quality == "480p30" else "480p30" if quality == "360p30" else "360p30"
                check = False
            if quality == "chunked": check = True
            qual[quality] = url
    print(qual)
    return m3u8(qual, chunked)

def m3u8(qual, chunked):
    rtn = "#EXTM3U\n"
    resolution = {"1080p60": "1920x1080", "1080p30": "1920x1080", "720p60": "1280x720", "720p30": "1280x720", "480p30": "852x480", "360p30": "640x360", "160p30": "284x160"}
    fps = {"60": "59.999", "30": "30.101"}
    for quality in qual.keys():
        if quality == "chunked": 
            rtn += f"#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID=\"chunked\",NAME=\"{chunked}\",AUTOSELECT=NO,DEFAULT=NO\n"
            #EXT-X-STREAM-INF:CODECS="avc1.64002A,mp4a.40.2",RESOLUTION=1920x1080,VIDEO="chunked",FRAME-RATE=59.999
            rtn += f"#EXT-X-STREAM-INF:CODECS=\"avc1.64002A,mp4a.40.2\",RESOLUTION={resolution[chunked]},VIDEO=\"chunked\",FRAME-RATE={fps[chunked.split('p')[1]]}\n"
            rtn += f"{qual[quality]}\n"
        else: 
            rtn += f"#EXT-X-MEDIAL:TYPE=VIDEO,GROUP-ID=\"{quality}\",NAME=\"{quality}\",AUTOSELECT=YES,DEFAULT=YES\n"
            rtn += f"#EXT-X-STREAM-INF:CODECS=\"avc1.64002A,mp4a.40.2\",RESOLUTION={resolution[quality]},VIDEO=\"{quality}\",FRAME-RATE={fps[quality.split('p')[1]]}\n"
            rtn += f"{qual[quality]}\n"
    return rtn


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=8888)