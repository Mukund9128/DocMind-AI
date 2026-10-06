from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models import Chat,Message
import json
bp=Blueprint('chats',__name__,url_prefix='/api/chats')
@bp.get('')
@jwt_required()
def chats(): return jsonify([{'id':c.id,'title':c.title,'created_at':c.created_at.isoformat()} for c in Chat.query.filter_by(user_id=int(get_jwt_identity())).order_by(Chat.created_at.desc()).all()])
@bp.get('/<int:id>/messages')
@jwt_required()
def messages(id):
 c=Chat.query.filter_by(id=id,user_id=int(get_jwt_identity())).first_or_404(); ms=Message.query.filter_by(chat_id=c.id).order_by(Message.created_at).all();return jsonify([{'role':m.role,'content':m.content,'sources':json.loads(m.sources_json) if m.sources_json else []} for m in ms])
