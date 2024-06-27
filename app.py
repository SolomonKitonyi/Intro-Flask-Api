from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///school.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

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


#TM Routes
@app.route('/tms',methods=["Get"])
def get_tms():
    tms = TM.query.all()
    return jsonify([{"id":tm.id, "first_name": tm.first_name, "last_name": tm.last_name} for tm in tms])

@app.route('/tms/<int:id>',methods=['GET'])
def get_tm(id):
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message':'TM not found'}),404
    return jsonify({'id': tm.id,'first_name':tm.first_name,'last_name':tm.last_name})

@app.route('/tms',methods=['POST'])
def create_tm():
    data = request.get_json()
    new_tm = TM(first_name =data["first_name"],last_name=data['last_name'])
    db.session.add(new_tm)
    db.session.commit()
    return jsonify({"Message":"TM created successfully"}),201

@app.route('/tms/<int:id>',methods=['PUT'])
def update_tm(id):
    data = request.get_json()
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message':'TM not found'}),404
    tm.first_name = data['first_name']
    tm.last_name = data['last_name']
    db.session.commit()
    return jsonify({'message':'TM Updated successfully'})

@app.route('/tms/<int:id>',methods=['DELETE'])
def delete(id):
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message': 'TM not found'}),404
    db.session.delete(tm)
    db.session.commit()
    return jsonify({'message':'TM deleted successfully'})

@app.route('/tms/<int:id>/students',methods=['GET'])
def get_tm_students(id):
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message':'TM not found'}),404
    students = Student.query.filter_by(tm_id=id).all()
    return jsonify([{'id':student.id,'first_name':student.first_name,'last_name':student.last_name,'course':student.course} for student in students])

#student Routes
@app.route('/students',methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id':student.id,'first_name':student.first_name,'last_name':student.last_name,'course':student.course,'tm_id': student.tm_id} for student in students])

@app.route('/students/<int:id>',methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message':'Student not found'}),404
    return jsonify({'id': student.id,'first_name': student.first_name,'last_name': student.last_name,'course': student.course,'tm_idd':student.tm_id})

@app.route('/students',methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(first_name = data['first_name'],last_name = data['last_name'],course = data['course'],tm_id=data['tm_id'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': "Student created successfully"}),201
@app.route('/students/<int:id>',methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)
    if not student:
        return jsonify({'message':'Student not found'}),404
    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.course = data['course']
    student.tm_id = data['tm_id']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@app.route('/students/<int:id>',methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}),404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message':'Student deleted successfully'})

@app.route('/students/<int:id>/tm',methods=['GET'])
def get_student_tm(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}),404
    tm = TM.query.get(student.tm_id)
    return jsonify({'id': tm.id, 'first_name': tm.first_name,'last_name':tm.last_name})


if __name__== '__main__':
    app.run(debug=True)