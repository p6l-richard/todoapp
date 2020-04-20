import sys
from flask import Flask, render_template, request, redirect, flash, url_for, abort, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
from sqlalchemy.orm import backref

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
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    # li = db.relationship('Lists', backref=backref('todo', cascade="all,delete,delete-orphan"))

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, descr: {self.description}'
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(280), nullable=False)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    todo = db.relationship('Todo',
                        cascade='all,delete,delete-orphan',
                        backref='list'
                        , lazy=True)

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, descr: {self.description}'
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }

@app.route('/lists/<list_id>', methods=['GET', 'DELETE'])
def lists(list_id):
    if request.method == 'DELETE':
        print('Going to delete')
        return delete_list(list_id)
    elif request.method == 'GET':
        return get_list_todos(list_id)

def get_list_todos(list_id):
    return render_template('index.html', todos=Todo.query.all(), lists=Lists.query.all())

def delete_list(list_id):
    print('Specifically going to delete', list_id)
    try:
        li_todelete = Lists.query.filter_by(id=list_id).first()
        db.session.delete(li_todelete)
        db.session.commit()
        print('Successfully deleted')
        return 'success', 200
    except:
        db.session.rollback()
        print(sys.exc_info())
        return 'Something went wrong' + str(sys.exc_info()), 200
    finally:
        db.session.close()

@app.route('/lists/create-new', methods=['POST'])
def new_list():
    try:
        li = Lists(title=request.json.get('title'), description=request.json.get('description'))
        db.session.add(li)
        db.session.commit()
        return jsonify({
            'data': li.serialized
            })
    except:
        print('ERROR:', sys.exc_info())
        db.session.rollback()
        return 'Something went wrong, debug: ' + str(sys.exc_info), 200 
    finally:
        db.session.close()

@app.route('/lists/update', methods=['POST'])
def update_list():
    data = request.get_json()
    print('REQUEST received')
    try:
        todo = Todo.query.get(data['id'])
        todo.completed = data['completed']
        db.session.commit()
        return jsonify({
            'data': Todo.query.get(data['id']).serialized
        })
    except exc.StatementError as e:
        db.session.rollback()
        print('No worries, I have rolled back already, because of:', e.__dict__['orig'])
        return str(e.__dict__['orig']), 400
    finally:
        db.session.close()

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/todo/create-new', methods=['GET', 'POST'])
def new_todo():
    try:
        todo = Todo(title=request.json.get('title'), description=request.json.get('description'))
        db.session.add(todo)
        db.session.commit()
        return jsonify({
            'data': todo.serialized
            })
    except:
        print('ERROR:', sys.exc_info)
        db.session.rollback()
        return 'Something went wrong, debug: ' + str(sys.exc_info), 200 
    finally:
        db.session.close()


@app.route('/todo/update', methods=['POST'])
def update_todo():
    data = request.get_json()
    print('REQUEST received')
    try:
        todo = Todo.query.get(data['id'])
        todo.completed = data['completed']
        db.session.commit()
        return jsonify({
            'data': Todo.query.get(data['id']).serialized
        })
    except exc.StatementError as e:
        db.session.rollback()
        print('No worries, I have rolled back already, because of:', e.__dict__['orig'])
        return str(e.__dict__['orig']), 400
    finally:
        db.session.close()


@app.route('/todo/<todo_id>', methods=['DELETE'])
def delete_item(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
        return 'success', 200
    except:
        db.session.rollback()
        return 'Something went wrong' + str(sys.exc_info()), 200
    finally:
        db.session.close()
    
if __name__ == '__main__':
    app.run(debug=True)