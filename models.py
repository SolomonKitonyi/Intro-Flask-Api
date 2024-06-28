from app import db

class TM(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    students = db.relationship("Student",backref="tm", lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    course = db.Column(db.String(100))
    tm_id = db.Column(db.Integer,db.ForeignKey('tm.id'),nullable=False)