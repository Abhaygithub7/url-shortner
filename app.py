from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT NOT NULL,
                    short_url TEXT NOT NULL UNIQUE
                )""")
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Shorten URL
@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form["url"]
    short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_id))
    conn.commit()
    conn.close()

    return f"Shortened URL: <a href='/{short_id}'>http://127.0.0.1:5000/{short_id}</a>"

# Redirect
@app.route("/<short_id>")
def redirect_url(short_id):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return redirect(row[0])
    else:
        return "URL not found!", 404

if __name__ == "__main__":
    app.run(debug=True)