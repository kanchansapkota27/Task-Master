from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tasks.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>'%self.id

@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(task=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue Adding Task"
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Issue on deletion"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task_to_update=Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.task=request.form['content']
        if len(task_to_update.task)<1:
            return redirect('/')
        try:
            db.session.commit()
            return redirect('/')
        except:
            "Issue updating task"
    else:
        return render_template('update.html',task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)