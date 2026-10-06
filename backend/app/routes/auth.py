from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from ..extensions import db
from ..models import User
bp=Blueprint('auth',__name__,url_prefix='/api/auth')
@bp.post('/register')
def register():
 d=request.get_json() or {}; name=d.get('name','').strip(); email=d.get('email','').strip().lower(); pwd=d.get('password','')
 if not name or not email or len(pwd)<6:return jsonify(error='Name, email and password (6+ chars) are required'),400
 if User.query.filter_by(email=email).first():return jsonify(error='Email already registered'),409
 u=User(name=name,email=email);u.set_password(pwd);db.session.add(u);db.session.commit();return jsonify(message='Registered successfully'),201
@bp.post('/login')
def login():
 d=request.get_json() or {}; u=User.query.filter_by(email=d.get('email','').lower()).first()
 if not u or not u.check_password(d.get('password','')):return jsonify(error='Invalid email or password'),401
 return jsonify(access_token=create_access_token(identity=str(u.id)),user={'id':u.id,'name':u.name,'email':u.email})
@bp.get('/me')
@jwt_required()
def me():
 u=db.session.get(User,int(get_jwt_identity())); return jsonify(id=u.id,name=u.name,email=u.email)
