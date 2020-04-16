from flask import Flask, render_template, request, redirect, flash, url_for, abort, Response, jsonify
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
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, descr: {self.description}'
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todo/create-new', methods=['GET', 'POST'])
def new_item():
    print("NOBODY CAN SEE ME", request.data, request.json, request.values)
    error = False
    try:
        todo = Todo(title=request.json.get('title'), description=request.json.get('description'))
        db.session.add(todo)
        db.session.commit()
    except:
        print('ERROR:', exc_info)
        error = True
    finally:
        db.session.close()
    if error:
        db.session.rollback()
        abort(Response(exc_info))
    else:
        record = Todo.query.order_by(Todo.id.desc()).first()
        return jsonify({
            'data': record.serialized
            })
    
if __name__ == '__main__':
    app.run(debug=True)