from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:234107@localhost:5432/todo_db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(280), nullable=False)

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, descr: {self.description}'

db.create_all()

if not Todo.query.all():
    todos = [
        Todo(
            title=f'{i + 1} - thing to do',
            description=f'The number {i + 1} thing to do for me.'
        ) for i in range(5)]
    db.session.bulk_save_objects(todos)
    db.session.commit()



@app.route('/')
def index():
    return render_template('index.html', data=[
        {
            "description": "Todo1"
        }, {
            "description": "Todo2"
        }, {
            "description": "Todo3"
        }, {
            "description": "Todo4"
        }])

if __name__ == '__main__':
    app.run(debug=True)