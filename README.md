# Classroom Task Tracker

A beginner-friendly, browser-based task manager built with Python, Flask, HTML, CSS, JavaScript and JSON.

## Features

- Add a task with a title, subject and priority.
- View all tasks or filter by All, Pending or Completed.
- Mark tasks as completed or reopen them.
- Delete tasks.
- View total, pending and completed task counts.
- View completion progress as a percentage and progress bar.
- Save tasks in `tasks.json`, so they remain after restarting the app.

## Project structure

```text
classroom-task-tracker/
├── app.py
├── tasks.json
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Requirements

- Python 3.10 or newer
- VS Code (recommended)
- A web browser
- Internet connection for the first Flask installation

## Run on Windows

1. Open this folder in VS Code.
2. Select **Terminal → New Terminal**.
3. Install Flask:

   ```bash
   py -m pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   py app.py
   ```

5. Open this address in your browser:

   `http://127.0.0.1:5000`

If `py` does not work but `python` does, use `python` instead.

## Run on macOS or Linux

Open a terminal in this folder and run:

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Then visit `http://127.0.0.1:5000`.

To stop the server, click the terminal and press **Ctrl + C**.

## How data is stored

Tasks are saved in `tasks.json` in the project folder. Each task has an ID, title, subject, priority and status. The file starts empty (`[]`) and is updated when tasks are added, changed or deleted.

Example task:

```json
{
    "id": 1,
    "title": "Practice Python loops",
    "subject": "Python",
    "priority": "High",
    "status": "Pending"
}
```

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Display the webpage |
| GET | `/api/tasks` | Return tasks and statistics |
| GET | `/api/tasks?status=Pending` | Return pending tasks |
| POST | `/api/tasks` | Add a task |
| PATCH | `/api/tasks/1` | Change task status |
| DELETE | `/api/tasks/1` | Delete a task |

## GitHub upload

1. Sign in to GitHub and create a repository named `classroom-task-tracker`.
2. Upload the files and folders from this project, preserving the folder structure.
3. Commit with a message such as `Add Classroom Task Tracker project`.
4. Check that all files appear in the repository.

Do not upload virtual environments (`.venv`, `venv` or `env`) or Python cache folders (`__pycache__`). The included `.gitignore` helps exclude them.

**Important:** GitHub stores and shares your code; it does not automatically host this Flask application as a live website.

## Limitations

This project runs locally and stores records in a local JSON file. It does not include user accounts, a cloud database, reminders, online hosting, machine learning or AI predictions.
