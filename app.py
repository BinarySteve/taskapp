from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable =True)
    date_create = db.Column(db.DateTime, default= datetime.utcnow)
    

    def __repr__(self):
        return '<todo %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        todo_content = request.form['content']
        new_todo = Todo(content=todo_content)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error in adding your todo'
    else:
        todos = Todo.query.order_by(Todo.date_create).all()
        return render_template('index.html', todos=todos)
    
@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Could not delete todo'
        
@app.route('/update<int:id>', methods = ['GET', 'POST'])
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todo.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your todo'

    else:
        return render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)