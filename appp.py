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
    app.run(host="0.0.0.0", port=5000, debug=False)