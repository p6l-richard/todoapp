from flask import Flask, render_template, request, redirect, flash, url_for 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:234107@localhost:5432/todo_app'
app.secret_key = 'super secret'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(280), nullable=False)
    # status = db.Column(db.Boolean, nullable=False, default=False)
    # usr = db.Column(db.Integer, nullable=False, default=0)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, descr: {self.description}'

# db.create_all()

# if not Todo.query.all():
#     todos = [
#         Todo(
#             title=f'{i + 1} - thing to do',
#             description=f'The number {i + 1} thing to do for me.'
#         ) for i in range(5)]
#     db.session.bulk_save_objects(todos)

# db.session.commit()
# db.drop_all()
# db.session.commit()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todo/create-new', methods=['GET', 'POST'])
def new_item():
    if request.form.get('title', None):
        db.session.add(Todo(title=request.form['title'], description=request.form['description']))
        db.session.commit()
        flash(f'Item added to DB:\n{Todo.query.order_by(Todo.id.desc()).limit(1).all()}', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)