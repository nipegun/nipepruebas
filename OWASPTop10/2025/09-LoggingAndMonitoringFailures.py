#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/login")
def fLogin():
  # VULN: No logging, no detección
  u = request.args.get("u","")
  p = request.args.get("p","")

  if u == "admin" and p == "admin":
    return "OK"
  else:
    return "Fallo (sin logs, sin alertas)"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5009, debug=True)
