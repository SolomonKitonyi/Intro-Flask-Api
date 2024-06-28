from flask import Blueprint,request,jsonify
from app import db
from models import TM,Student

bp = Blueprint('tm',__name__,url_prefix='/tms')

#TM Routes
@bp.route('/',methods=["Get"])
def get_tms():
    tms = TM.query.all()
    return jsonify([{"id":tm.id, "first_name": tm.first_name, "last_name": tm.last_name} for tm in tms])

@bp.route('/<int:id>',methods=['GET'])
def get_tm(id):
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message':'TM not found'}),404
    return jsonify({'id': tm.id,'first_name':tm.first_name,'last_name':tm.last_name})

@bp.route('/',methods=['POST'])
def create_tm():
    data = request.get_json()
    new_tm = TM(first_name =data["first_name"],last_name=data['last_name'])
    db.session.add(new_tm)
    db.session.commit()
    return jsonify({"Message":"TM created successfully"}),201

@bp.route('/<int:id>',methods=['PUT'])
def update_tm(id):
    data = request.get_json()
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message':'TM not found'}),404
    tm.first_name = data['first_name']
    tm.last_name = data['last_name']
    db.session.commit()
    return jsonify({'message':'TM Updated successfully'})

@bp.route('/<int:id>',methods=['DELETE'])
def delete(id):
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message': 'TM not found'}),404
    db.session.delete(tm)
    db.session.commit()
    return jsonify({'message':'TM deleted successfully'})

@bp.route('/<int:id>/students',methods=['GET'])
def get_tm_students(id):
    tm = TM.query.get(id)
    if not tm:
        return jsonify({'message':'TM not found'}),404
    students = Student.query.filter_by(tm_id=id).all()
    return jsonify([{'id':student.id,'first_name':student.first_name,'last_name':student.last_name,'course':student.course} for student in students])
