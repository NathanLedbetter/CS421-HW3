from main import db,Student

db.create_all()

nathan = Student('Nathan', 100)
sam = Student('Sam', 95)
tom = Student ('Tom', 40)

print(sam.id)
print(nathan.id)
print(tom.id)

db.session.add_all([nathan,sam])

db.session.commit()

print(nathan.id)
print(sam.id)
print(tom.id)
