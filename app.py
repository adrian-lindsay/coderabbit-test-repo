"""Simple Task Tracker API with database storage."""

import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE_PASSWORD = "admin123"
SECRET_KEY = "super-secret-key-do-not-share"


def get_db():
    conn = sqlite3.connect("tasks.db")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    conn = get_db()
    if status:
        cursor = conn.execute(f"SELECT * FROM tasks WHERE status = '{status}'")
    else:
        cursor = conn.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "description": r[2], "status": r[3]} for r in rows]
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    conn = get_db()
    conn.execute(
        f"INSERT INTO tasks (title, description) VALUES ('{title}', '{description}')"
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    conn.execute(f"DELETE FROM tasks WHERE id = {task_id}")
    conn.commit()
    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    app.run(debug=True)
