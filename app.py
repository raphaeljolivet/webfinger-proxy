# This is a sample Python script.

from config import *
from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

# Ensure no trailing slashes
REMOTE_BASE_URL = ("https" if REMOTE_HTTPS else "http") + "://" + REMOTE_HOST
BASE_URL = ("https" if HTTPS else "http") + "://" + HOST

WELL_KNOWN_BASE="/.well-known/"

@app.route(WELL_KNOWN_BASE + "host-meta")
@app.route(WELL_KNOWN_BASE + "host-meta.json")
def host_meta():

    resp = requests.request(
        method=request.method,
        url=REMOTE_BASE_URL + request.full_path,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False)

    output = resp.text
    output = output.replace(REMOTE_BASE_URL, BASE_URL)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(output, resp.status_code, headers)


@app.route(WELL_KNOWN_BASE + "webfinger")
def webfinger():

    request_resource = request.args.get("resource")
    remote_resource = request_resource.replace(HOST, REMOTE_HOST)

    resp = requests.request("GET",
        url=REMOTE_BASE_URL + WELL_KNOWN_BASE + "webfinger",
        params=dict(resource=remote_resource),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    out = resp.text

    remote_resource_re = re.compile(re.escape(remote_resource), re.IGNORECASE)

    out = remote_resource_re.sub(request_resource, out)

    return Response(out, resp.status_code, headers)

if __name__ == '__main__':
    app.run(debug=True)


