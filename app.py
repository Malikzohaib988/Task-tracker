from flask import Flask, jsonify, render_template, request
import json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("tasks.json")

ALLOWED_PRIORITIES = {"Low", "Medium", "High"}
ALLOWED_STATUSES = {"Pending", "Completed"}


def load_tasks():
    """Load tasks from the JSON file. Return an empty list if it does not exist."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Save all tasks to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def get_statistics(tasks):
    """Calculate total, pending, completed and progress values."""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["status"] == "Completed")
    pending = total - completed
    progress = round((completed / total) * 100) if total > 0 else 0

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "progress": progress
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    status_filter = request.args.get("status", "All")

    if status_filter not in {"All", "Pending", "Completed"}:
        return jsonify({"error": "Invalid status filter."}), 400

    if status_filter == "All":
        filtered_tasks = tasks
    else:
        filtered_tasks = [
            task for task in tasks if task["status"] == status_filter
        ]

    return jsonify({
        "tasks": filtered_tasks,
        "statistics": get_statistics(tasks)
    })


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}

    title = str(data.get("title", "")).strip()
    subject = str(data.get("subject", "")).strip()
    priority = data.get("priority", "Medium")

    if not title:
        return jsonify({"error": "Please enter a task title."}), 400
    if not subject:
        return jsonify({"error": "Please enter a subject."}), 400
    if priority not in ALLOWED_PRIORITIES:
        return jsonify({"error": "Please choose a valid priority."}), 400

    tasks = load_tasks()
    next_id = max((task.get("id", 0) for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "subject": subject,
        "priority": priority,
        "status": "Pending"
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify({
        "message": "Task added successfully.",
        "task": new_task,
        "statistics": get_statistics(tasks)
    }), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")

    if new_status not in ALLOWED_STATUSES:
        return jsonify({"error": "Status must be Pending or Completed."}), 400

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            save_tasks(tasks)
            return jsonify({
                "message": "Task status updated.",
                "task": task,
                "statistics": get_statistics(tasks)
            })

    return jsonify({"error": "Task not found."}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        return jsonify({"error": "Task not found."}), 404

    save_tasks(updated_tasks)
    return jsonify({
        "message": "Task deleted.",
        "statistics": get_statistics(updated_tasks)
    })


if __name__ == "__main__":
    app.run(debug=True)
