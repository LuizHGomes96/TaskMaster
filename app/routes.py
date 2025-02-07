from app import app
from flask import Flask, render_template, redirect, request, session
from app.forms import TaskForm
from app.models import Tasks, db
from flask import flash
from sqlalchemy import text #type: ignore

@app.route('/', methods = ['GET'])
def index():
    my_tasks = Tasks.query.order_by(Tasks.date_added)
    return render_template("index.html", my_tasks=my_tasks)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    form = TaskForm()
    task = None
    session.pop('_flashes', None)
    if form.validate_on_submit():

        max_order = db.session.query(db.func.max(Tasks.order)).scalar()
        new_order = (max_order + 1) if max_order is not None else 1

        newTask = Tasks(task = form.task.data, description = form.description.data, order = new_order)
        db.session.add(newTask)
        db.session.commit()

        task = form.task.data
        form.task.data = ''
        form.description.data = ''
        flash ("Task Added.")
    my_tasks = Tasks.query.order_by(Tasks.date_added)
    return render_template("add.html", form=form, task=task, my_tasks=my_tasks)

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    form = TaskForm()
    editTask = Tasks.query.get(id)
    session.pop('_flashes', None)

    if request.method == 'GET':
        form.task.data = editTask.task
        form.description.data = editTask.description

    if form.validate_on_submit():
        editTask.task = form.task.data
        editTask.description = form.description.data
        db.session.commit()
        flash("Task Updated.")
    
    return render_template("edit.html", form=form, editTask=editTask)

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()

    # REORDER IDs

    db.session.execute(text("SET @count = 0"))
    db.session.execute(text("UPDATE tasks SET id = @count := @count + 1"))
    db.session.execute(text("ALTER TABLE tasks AUTO_INCREMENT = 1"))
    db.session.commit()

    return redirect("/")


@app.route('/deleteall', methods = ['GET', 'POST'])
def deleteall():
    
    tasks = Tasks.query.all()
    for task in tasks:
        db.session.delete(task)
        db.session.commit()

        # REORDER IDs

    db.session.execute(text("SET @count = 0"))
    db.session.execute(text("UPDATE tasks SET id = @count := @count + 1"))
    db.session.execute(text("ALTER TABLE tasks AUTO_INCREMENT = 1"))
    db.session.commit()

    return redirect("/")


@app.route('/done/<int:id>', methods = ['GET', 'POST'])
def done(id):
    task = Tasks.query.get(id)
    task.status = True
    db.session.commit()
    return redirect("/")
