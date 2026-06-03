from flask import Blueprint, render_template
import sqlite3

history_bp = Blueprint("history", __name__)

@history_bp.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT volume, temperature, result
        FROM predictions
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("history.html", data=data)