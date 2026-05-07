from flask import Flask, render_template, request, redirect
import json
import os
import datetime

app = Flask(__name__)

FILE_NAME = 'tasks.json'

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form['task']
    if new_task:
          today = datetime.date.today().strftime('%Y-%m-%d')
          tasks.append({'text': new_task, 'date': today, 'done': False})
          save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)	
        save_tasks(tasks)
    return redirect('/')

@app.route('/alldelete', methods=['POST'])
def alldelete():
    if 0 < len(tasks):
        tasks.clear()
        save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404

    if request.method == 'POST':
        old_text = tasks[task_id]['text']
        new_text = request.form.get('task', '').strip()

        if new_text == '':
            return render_template('edit.html', task=['task.text'], message="Текст не может быть пустым!")

        if new_text == old_text:
            return render_template('edit.html', task=['task.text'], message="Ничего не изменено")

        if new_text:
            tasks[task_id]['text'] = new_text
            save_tasks(tasks)
        return redirect('/')

    else:
        return render_template('edit.html', task=tasks[task_id])

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect('/')

@app.route('/active')
def active_tasks():
    filtered = [t for t in tasks if not t['done']]
    return render_template('index.html', tasks=filtered)

@app.route('/completed')
def completed_tasks():
    filtered = [t for t in tasks if t['done']]
    return render_template('index.html', tasks=filtered)

@app.route('/complete_all', methods=['POST'])
def complete_all():
    for task in tasks:
        task['done'] = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/undo_all', methods=['POST'])
def undo_all():
    for task in tasks:
        task['done'] = False
    save_tasks(tasks)
    return redirect('/')

#Доделать

if __name__ == '__main__':
    app.run(debug=True)
