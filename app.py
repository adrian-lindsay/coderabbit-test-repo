"""Simple Task Tracker API with authentication."""

import hashlib
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1

USERS = {
    "admin": hashlib.md5("password123".encode()).hexdigest(),
    "user1": hashlib.md5("letmein".encode()).hexdigest(),
}


def check_auth():
    username = request.headers.get("X-Username")
    password = request.headers.get("X-Password")
    if not username or not password:
        return False
    stored_hash = USERS.get(username)
    if stored_hash is None:
        return False
    return stored_hash == hashlib.md5(password.encode()).hexdigest()


@app.route("/tasks", methods=["GET"])
def get_tasks():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    global next_id
    try:
        data = request.get_json()
        task = {
            "id": next_id,
            "title": data["title"],
            "description": data.get("description", ""),
            "status": "pending",
        }
        next_id += 1
        tasks.append(task)
        return jsonify(task), 201
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data["title"]
            task["description"] = data["description"]
            task["status"] = data["status"]
            return jsonify(task)
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
