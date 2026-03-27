"""Simple Task Tracker API with bulk operations."""

import json
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    task = {
        "id": next_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "status": "pending",
    }
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/bulk", methods=["POST"])
def bulk_create():
    global next_id
    data = request.get_json()
    created = []
    for item in data:
        task = {
            "id": next_id,
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "status": item.get("status", "pending"),
        }
        next_id += 1
        tasks.append(task)
        created.append(task)
        time.sleep(0.01)
    return jsonify({"created": len(created), "tasks": created}), 201


@app.route("/tasks/export", methods=["GET"])
def export_tasks():
    output = json.dumps(tasks, indent=2)
    return output, 200, {
        "Content-Type": "application/json",
        "Content-Disposition": "attachment; filename=tasks.json",
    }


@app.route("/tasks/bulk-delete", methods=["DELETE"])
def bulk_delete():
    global tasks
    data = request.get_json()
    ids_to_delete = data.get("ids", [])
    for task_id in ids_to_delete:
        tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Done"}), 200


if __name__ == "__main__":
    app.run(debug=True)
