from main import db,Student

#CREATE
new_student = Student ('John', 90)
db.session.add(new_student)
db.session.commit()

#READ
all_students = Student.query.all()
print (all_students)

first_student = Student.query.get(1)
print(first_student.name)

student_pass = Student.query.filter(Student.grade>=85)
print(student_pass.all())

#UPDATE
first_student = Student.query.get(1)
first_student.grade = 105
db.session.add(first_student)
db.session.commit()

#DELETE
second_student = Student.query.get(2)
db.session.delete(second_student)
db.session.commit()


all_students = Student.query.all()
print(all_students)
