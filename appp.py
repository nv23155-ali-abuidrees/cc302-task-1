import sys
import os

try:
    from flask import Flask, render_template, request, redirect, url_for
    from flask_sqlalchemy import SQLAlchemy
except ImportError:
    print("Missing required Python packages: Flask and/or Flask-SQLAlchemy.")
    print("Install them with: python3 -m pip install -r requirements.txt")
    sys.exit(1)

app = Flask(__name__)

# ---- Database configuration ----
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasks.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "dev"  # prevents some Flask warnings

db = SQLAlchemy(app)

# ---- Task Model ----
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    important = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id}>"

# ---- Create database ----
with app.app_context():
    db.create_all()

# ---- Routes ----
@app.route("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form.get("content")

    if task_content and task_content.strip():
        new_task = Task(content=task_content.strip())
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for("index"))

@app.route("/complete/<int:id>")
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form.get("content").strip()
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)

@app.route("/toggle-important/<int:id>")
def toggle_important(id):
    task = Task.query.get_or_404(id)
    task.important = not task.important
    db.session.commit()
    return redirect(url_for("index"))

# ---- Run app ----
if __name__ == "__main__":
    # Bind to all interfaces so the app is reachable from outside the container
    # When running under Gunicorn the __main__ block is not used.
    import socket

    def _find_free_port(start_port: int = 5000, max_port: int = 5100) -> int:
        for p in range(start_port, max_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("0.0.0.0", p))
                    return p
                except OSError:
                    continue
        raise OSError("no free ports available")

    # prefer PORT env var when provided
    requested = int(os.environ.get("PORT", 5000))
    port = requested
    try:
        # if requested port is busy, find next free port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
            except OSError:
                port = _find_free_port(requested + 1)
    except OSError:
        print("No available ports to bind the Flask app; exiting.")
        sys.exit(1)

    if port != requested:
        print(f"Port {requested} in use, starting on available port {port}.")

    app.run(host="0.0.0.0", port=port, debug=False)Part A — Confirm your CI workflow exists (pre-req)
Students must already have:

.github/workflows/ci.yml

It runs on pull_request (and ideally push to dev/main)

✅ Quick check: open Actions tab → verify CI runs at least once.

Part B — Create the Branch Rules (Quality Gate Setup)
Option 1 (recommended): Protect dev first, then main
Because students merge feature branches → dev first.

Steps (GitHub UI)
Go to your repo → Settings

Find Rules or Branches

Create a ruleset (or branch protection rule) for:

dev

Enable:

✅ Require a pull request before merging

✅ Require status checks to pass before merging

Select required check(s) from the list:

choose your CI job name (example: CI / test or lint-test)

Save rule

Repeat the same for main after dev is working.

Part C — Prove the gate works (Fail → Block → Fix → Pass)
This is the core of the lesson.

Step 1: Make CI fail intentionally (safe controlled failure)
Pick ONE of these:

Break a test expectation (assert 200 → assert 201)

Add a Python syntax error

Add a failing assertion

Commit to a feature branch and open PR into dev.

Step 2: Observe the gate
CI should fail (red)

Merge button should show blocked:

“Required checks have not passed”

Step 3: Fix the issue
Correct the code/test

Push again to the same branch

CI should go green

Merge becomes available

Step 4: Merge
Merge PR → dev.

Student Deliverables (Quick Formative Assessment: FA-Style)
Students must submit one evidence pack zip containing:

Evidence Required
Screenshot: Branch protection / ruleset showing:

PR required

required status checks enabled

Screenshot: PR where merge is blocked due to failed CI (red)

Screenshot: PR where CI passes and merge becomes allowed (green)

PR link (feature → dev)

Short explanation (5–7 lines):

What failed?

Why was merge blocked?

What did you change to pass?

Submission Naming
CC302_WXX_<StudentID>_Evidence.zip