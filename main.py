import os
from flask import Flask, render_template, redirect, url_for, request
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask (__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)

class Student(db.Model):
    __tablename__="students"

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text)
    grade= db.Column(db.Integer)

    def __init__(self,name,grade):
        self.name=name
        self.grade=grade

    def __repr__(self):
        return f"Student {self.name} got {self.grade} on midterm exam"

class AddStudentForm(FlaskForm):
    name = StringField('Student Name', [validators.Length(min=1, max=25)])
    grade = StringField('Student Grade')
    submit = SubmitField('Add Student')

class DeleteStudentForm(FlaskForm):
    id = StringField('Student Number', [validators.Length(min=1, max=25)])
    submit = SubmitField('Delete Student')

class ListStudentsButton(FlaskForm):
    submit = SubmitField('List Students')

class ListPassingStudentsButton(FlaskForm):
    submit = SubmitField('List Passing Students')

#default for results.html is to show all students
results_students = Student.query.all()


@app.route ('/', methods=['GET','POST'])
def index():
    name =False
    grade =False
    id =False
    form1 = AddStudentForm(request.form)
    if request.method == 'POST' and form1.validate():
        name = form1.name.data
        grade = form1.grade.data
        new_student = Student (name, grade)
        db.session.add(new_student)
        db.session.commit()

    form2 = DeleteStudentForm(request.form)
    if request.method == 'POST' and form2.validate():
        id = form2.id.data
        deleted_student = Student.query.get(id)
        db.session.delete(deleted_student)
        db.session.commit()

    button1 = ListStudentsButton(request.form)
    #if request.method == 'POST' and button1.submit():
        #results_students = Student.query.all()
        #return redirect(url_for('info'))

    button2 = ListPassingStudentsButton(request.form)
    #if request.method == 'POST' and button2.submit():
        #results_students = Student.query.filter(Student.grade>=85)
        #return redirect(url_for('info'))

    return render_template('home.html', form1=form1, form2=form2, name=name, grade=grade, id=id)

#showing all students
@app.route ('/results')
def info():
    results_students = Student.query.all()
    return render_template('results.html', students=results_students)

#showing only the passing students
@app.route ('/passing')
def passing():
    results_students = Student.query.filter(Student.grade>=85)
    return render_template('results.html', students=results_students)


if __name__ == '__main__':
    app.run(debug=True)
