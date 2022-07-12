from flask import Flask, render_template, request, flash,redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '07890ba5c9a3536e64acc021d7a02e09'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    due_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' %self.id
        # return f"Task('{self.content}', '{self.date_created}', '{self.due_date}')"

@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been loggrd in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        date = request.form['date'].split('-')
        due_date = datetime(int(date[0]), int(date[1]), int(date[2]))
        if task_content == '':
            flash(f'No task written!', 'danger')
            return redirect('/')
        else:
            new_task = Todo(content= task_content, due_date = due_date)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return "Error"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        flash(f'There was a problem deleting that task!', 'danger')
        return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        date = request.form['date'].split('-')
        task.due_date = datetime(int(date[0]), int(date[1]), int(date[2]))
        try:
            db.session.commit()
            return redirect('/')
        except:
            flash(f'Error', 'danger')
            return redirect('/update/<int:id>')
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug = True)