from flask import *
from flask_cors import CORS
import os
from streamlink import streams
import requests

app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)

@app.route('/<path:path>', methods=['GET'])
def gql_get(path):
    reqheader = dict(request.headers)
    reqheader["Host"] = "gql.twitch.tv"
    data = requests.get(f"https://gql.twitch.tv/{path}", params=request.args, headers=reqheader)
    rtn = Response(data.content)
    for key in data.headers:
        rtn.headers[key] = data.headers[key]
    return rtn

@app.route('/<path:path>', methods=['POST'])
def gql_post(path):
    reqheader = dict(request.headers)
    reqheader["Host"] = "gql.twitch.tv"
    data = requests.post(f"https://gql.twitch.tv/{path}", params=request.args, headers=reqheader)
    rtn = Response(data.content)
    for key in data.headers:
        rtn.headers[key] = data.headers[key]
    return rtn

@app.route('/<path:path>', methods=['OPTIONS'])
def gql_options(path):
    reqheader = dict(request.headers)
    reqheader["Host"] = "gql.twitch.tv"
    data = requests.options(f"https://gql.twitch.tv/{path}", params=request.args, headers=reqheader)
    rtn = Response(data.content)
    for key in data.headers:
        rtn.headers[key] = data.headers[key]
    return rtn

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=8888)
