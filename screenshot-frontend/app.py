import requests
import os
import urllib

from flask import Flask, request, render_template, redirect, url_for, flash

BACKEND_URL = os.getenv('BACKEND_URL')

app = Flask(__name__)
app.secret_key = "supersecretkey"
# required for session-based flash messages


def get_token(url):
    """Retrieve an authorization bearer token
    from the metadata server"""
    token_url = (
        f"http://metadata.google.internal/computeMetadata/v1/instance/"
        f"service-accounts/default/identity?audience={url}"
    )
    token_req = urllib.request.Request(
        token_url, headers={"Metadata-Flavor": "Google"}
    )
    token_response = urllib.request.urlopen(token_req)
    token = token_response.read()
    return token.decode()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/screenshot', methods=['POST'])
def screenshot():
    url = request.form['url']
    token = get_token(BACKEND_URL)
    headers = {'Authorization': 'Bearer ' + token}
    screenshot_url = BACKEND_URL + '/?url=' + url
    r = requests.get(screenshot_url, headers=headers)
    if r.status_code == 200:
        flash("Screenshot captured successfully, check your GCS bucket!")
    else:
        flash("Screenshot capture failed :(")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

