
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from db_config import db
from models import Task
from forms import TaskForm

app = Blueprint("app", __name__)

@app.route("/")
def home():
    tasks = Task.query.order_by(Task.date_created).all()
    count_not_done = 0
    for task in tasks:
        if not task.done:
            count_not_done += 1
    return render_template("home.html", tasks=tasks, count_not_done=count_not_done)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title = form.title.data,
            description = form.description.data,
            date_limit = form.date_limit.data
        )
        db.session.add(new_task)

        db.session.commit()
        flash("Завдання успішно доданно", "success")
        return redirect(url_for("app.home"))
    return render_template("add_task.html", form=form)

@app.route("/update/<int:id>")
def update_task(id):
    task = Task.query.get_or_404(id)
    if task.done:
        task.done = False
        db.session.commit()
        flash("Завдання змінило статус", "success")
        return redirect(url_for("app.home"))
    else:
        task.done = True
        db.session.commit()
        flash("Завдання змінило статус", "success")
        return redirect(url_for("app.home"))

@app.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Завдання успішно видаленно", "success")
    return redirect(url_for("app.home"))
