import matplotlib.pyplot as plt
import os

from flask import Flask, render_template, request, redirect, session
import sqlite3

from model import train_model
from db import init_db

app = Flask(__name__)
app.secret_key = "secret123"

init_db()
model = train_model()


# ---------------- MAIN PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    prediction = None

    if request.method == "POST":
        volume = float(request.form["volume"])
        temperature = float(request.form["temperature"])

        result = model.predict([[volume, temperature]])
        prediction = round(result[0], 2)

        # save to DB
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions (volume, temperature, result)
            VALUES (?, ?, ?)
        """, (volume, temperature, prediction))

        conn.commit()
        conn.close()

    return render_template("index.html", prediction=prediction)


# ---------------- HISTORY PAGE ----------------
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, volume, temperature, result
        FROM predictions
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("history.html", data=data)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- PLOT ----------------
@app.route("/plot")
def plot():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT volume, result
        FROM predictions
    """)

    data = cursor.fetchall()
    conn.close()

    # filter anomalies
    data = [(v, r) for v, r in data if r < 50]

    volumes = [x[0] for x in data]
    results = [x[1] for x in data]

    plt.figure(figsize=(6, 4))
    plt.scatter(volumes, results)

    plt.xlabel("Обʼєм басейну (м³)")
    plt.ylabel("Витрата хімії (кг)")
    plt.title("Історія прогнозів")

    os.makedirs("static", exist_ok=True)
    plt.savefig("static/plot.png")
    plt.close()

    return render_template("plot.html")


# ---------------- TEST ----------------
@app.route("/test")
def test():
    return "WORKS"


if __name__ == "__main__":
    app.run(debug=True)