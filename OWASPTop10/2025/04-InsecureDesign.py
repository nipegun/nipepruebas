#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/buy")
def fBuy():
  vPrecio = request.args.get("price","100")
  # VULN: El precio viene del cliente
  return f"<h1>Compra realizada por {vPrecio} euros</h1>"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5004, debug=True)
