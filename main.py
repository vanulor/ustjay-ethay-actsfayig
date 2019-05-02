import os
from re import sub

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    payload = {
        "input_text": sub('[^A-Za-z0-9 ]+', '', get_fact())
    }  #regex cleans out anything that isn't alphanum or space
    r = requests.post(
        "https://hidden-journey-62459.herokuapp.com/piglatinize/",
        data=payload)
    return f"<HTML><body><a href='{r.url}'>{r.url}</a><p>{r.text}</body></HTML>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run('0.0.0.0', port=port)
