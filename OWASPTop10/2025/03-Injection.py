#!/usr/bin/env python3
import sqlite3
from flask import Flask, request

app = Flask(__name__)
cDB = "inj.db"

def fInit():
  conn = sqlite3.connect(cDB)
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT)")
  cur.execute("INSERT INTO users VALUES ('admin','admin123')")
  conn.commit()
  conn.close()

@app.route("/login", methods=["GET","POST"])
def fLogin():
  if request.method == "GET":
    return """
    <form method='POST'>
      User:<input name='u'><br>
      Pass:<input name='p'><br>
      <input type='submit'>
    </form>
    """
  vU = request.form.get("u","")
  vP = request.form.get("p","")
  conn = sqlite3.connect(cDB)
  cur = conn.cursor()

  # VULN SQLi
  query = f"SELECT user FROM users WHERE user='{vU}' AND pass='{vP}'"
  cur.execute(query)
  row = cur.fetchone()
  conn.close()

  if row:
    return f"Logged in como {row[0]}<br><pre>{query}</pre>"
  return f"Fallo<br><pre>{query}</pre>"

if __name__ == "__main__":
  fInit()
  app.run(host="0.0.0.0", port=5003, debug=True)
