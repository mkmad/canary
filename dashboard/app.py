import os
from flask import Flask, render_template, request
import requests

from canary.common import cli

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG=True,
)


# controllers
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/jobs")
def jobs():
    host = "0.0.0.0:8889"
    path = request.args.get('path', '')
    full_path = "http://{0}/v1.0/jobs?path={1}".format(host, path)

    return requests.get(full_path).content


@cli.runnable
def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
