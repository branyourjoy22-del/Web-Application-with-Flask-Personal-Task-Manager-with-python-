from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global list of tasks with incremental ids
tasks = []
_next_id = 1


def add_task(text):
    """Add a task with the given text. Returns the new task's id."""
    global _next_id
    task_id = _next_id
    _next_id += 1
    tasks.append({"id": task_id, "text": text, "completed": False})
    return task_id


def complete_task(id):
    """Mark the task with the given id as completed. Returns True if found, False otherwise."""
    for task in tasks:
        if task["id"] == id:
            task["completed"] = True
            return True
    return False


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    text = request.form.get('text', '').strip()
    if text:
        add_task(text)
    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    complete_task(task_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
