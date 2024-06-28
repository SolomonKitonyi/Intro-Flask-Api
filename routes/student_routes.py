from flask import Blueprint, request,jsonify
from app import db
from models import TM,Student

bp = Blueprint('student',__name__,url_prefix='/students')

#student Routes
@bp.route('/',methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id':student.id,'first_name':student.first_name,'last_name':student.last_name,'course':student.course,'tm_id': student.tm_id} for student in students])

@bp.route('/<int:id>',methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message':'Student not found'}),404
    return jsonify({'id': student.id,'first_name': student.first_name,'last_name': student.last_name,'course': student.course,'tm_idd':student.tm_id})

@bp.route('/',methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(first_name = data['first_name'],last_name = data['last_name'],course = data['course'],tm_id=data['tm_id'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': "Student created successfully"}),201
@bp.route('/<int:id>',methods=['PUT'])
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

@bp.route('/<int:id>',methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}),404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message':'Student deleted successfully'})

@bp.route('/<int:id>/tm',methods=['GET'])
def get_student_tm(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}),404
    tm = TM.query.get(student.tm_id)
    return jsonify({'id': tm.id, 'first_name': tm.first_name,'last_name':tm.last_name})