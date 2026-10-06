from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy import func
from ..models import Document,Chat
bp=Blueprint('dashboard',__name__,url_prefix='/api/dashboard')
@bp.get('')
@jwt_required()
def dashboard():
 uid=int(get_jwt_identity()); docs=Document.query.filter_by(user_id=uid); return jsonify(total_documents=docs.count(),total_questions=Chat.query.filter_by(user_id=uid).count(),recent_documents=[{'id':d.id,'name':d.original_filename} for d in docs.order_by(Document.created_at.desc()).limit(5)])
