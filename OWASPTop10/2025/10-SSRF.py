#!/usr/bin/env python3
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/fetch")
def fFetch():
  vURL = request.args.get("url","http://127.0.0.1")
  # VULN: SSRF sin validación
  r = requests.get(vURL)
  return f"<pre>{r.text}</pre>"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25010, debug=True)
