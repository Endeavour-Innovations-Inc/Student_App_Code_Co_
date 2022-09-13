from app import db
from app.models import Student
from app.models import Class
from app.models import enrolled

c1 = Class.query.filter_by(coursenum = '321').filter_by(major='CptS').first()
c2 = Class.query.filter_by(coursenum = '322').filter_by(major='CptS').first()
c3 = Class.query.filter_by(coursenum = '331').filter_by(major='CptS').first()
c4 = Class.query.filter_by(coursenum = '421').filter_by(major='CptS').first()

s1 = Student.query.filter_by(username='sakire').first()

s1.classes.append()
s1.classes.append()
s1.classes.append()
db.session.commit()

s1.classes.remove(c4)
db.session.commit()

for c in s1.classes:
    print(c)

enrolledClasses = Class.query.join(enrolled, (enrolled.c.classid == Class.id)).filter(enrolled.c.studentid == s1.id).order_by(Class.coursenum).all()

s1.classes.filter(enrolled.c.classid == c2.id).count() > 0

s2 = Student.query.filter_by(username='John').first()
c2.roster.append(s2)
db.session.commit()

for c in c2.classes:
    print(c)

for s in c2.roster:
    print(s)

#create the database file, if it doesn't exist. 
db.create_all()

# import db models
from app.models import Major

# Create a major
newMajor = Major(name='CptS',department='School of EECS')
db.session.add(newMajor)
newMajor = Major(name='CE',department='Civil Engineering')
db.session.add(newMajor)
db.session.commit()
Major.query.all()
for m in Major.query.all():
    print(m)


#create class objects and write them to the database
from app.models import Class
newClass = Class(coursenum='322',major='CptS',title='Software Engineering')
db.session.add(newClass)
newClass = Class(coursenum='315',major='CE',title='Fluid Mechanics')
db.session.add(newClass)
db.session.commit()

allClasses = Class.query.all()
Class.query.filter_by(major='CptS').all()
Class.query.filter_by(major='CptS').first()
Class.query.filter_by(major='CptS').order_by(Class.title).all()
Class.query.filter_by(major='CptS').count()

myMajor = Major.query.filter_by(name='CptS').first()

# query and print classes
allClasses = Class.query.all()
Class.query.filter_by(coursenum='322').all()
Class.query.filter_by(coursenum='322').first()
myclasses = Class.query.order_by(Class.coursenum.desc()).all()

mymajor = Major.query.filter_by(name='CptS').first()

for m in s1.majorofstudent:
    print(m._major)

for s in major2.studentsmajor:
    print(s._student)
