from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "tasks.json"

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

tasks = load_tasks()

# Home page - list tasks
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

# Add new task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append(task)
        save_tasks(tasks)
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

# Edit a task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        new_task = request.form.get('task')
        if new_task:
            tasks[task_id] = new_task
            save_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('edit.html', task=tasks[task_id], task_id=task_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)