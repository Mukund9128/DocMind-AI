from flask import Blueprint,request,jsonify,current_app
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from pathlib import Path
from uuid import uuid4
from ..extensions import db
from ..models import Document,DocumentChunk
from ..utils.files import allowed_file,extension
from ..services.document_service import extract,chunks
bp=Blueprint('documents',__name__,url_prefix='/api/documents')
def ser(d): return {'id':d.id,'name':d.original_filename,'file_type':d.file_type,'file_size':d.file_size,'pages':d.page_count,'status':d.processing_status,'created_at':d.created_at.isoformat()}
@bp.get('')
@jwt_required()
def list_docs():
 uid=int(get_jwt_identity()); q=(request.args.get('q') or '').strip(); x=Document.query.filter_by(user_id=uid); x=x.filter(Document.original_filename.ilike(f'%{q}%')) if q else x; return jsonify([ser(d) for d in x.order_by(Document.created_at.desc()).all()])
@bp.post('/upload')
@jwt_required()
def upload():
 uid=int(get_jwt_identity()); f=request.files.get('file')
 if not f or not f.filename:return jsonify(error='File is required'),400
 if not allowed_file(f.filename):return jsonify(error='Only PDF and DOCX are supported'),400
 ext=extension(f.filename); stored=f'{uuid4().hex}_{secure_filename(f.filename)}'; path=Path(current_app.config['UPLOAD_FOLDER'])/stored; f.save(path)
 try: pages=extract(path,ext)
 except Exception as e: path.unlink(missing_ok=True); return jsonify(error=f'Could not process document: {e}'),400
 d=Document(user_id=uid,original_filename=f.filename,stored_filename=stored,file_type=ext,file_size=path.stat().st_size,page_count=len(pages));db.session.add(d);db.session.flush()
 for c in chunks(pages):db.session.add(DocumentChunk(document_id=d.id,page_number=c['page'],chunk_index=c['index'],content=c['content']))
 db.session.commit();return jsonify(ser(d)),201
@bp.get('/<int:id>')
@jwt_required()
def get_doc(id):
 d=Document.query.filter_by(id=id,user_id=int(get_jwt_identity())).first_or_404();return jsonify(ser(d))
@bp.delete('/<int:id>')
@jwt_required()
def delete(id):
 d=Document.query.filter_by(id=id,user_id=int(get_jwt_identity())).first_or_404(); (Path(current_app.config['UPLOAD_FOLDER'])/d.stored_filename).unlink(missing_ok=True); db.session.delete(d);db.session.commit();return jsonify(message='Deleted')
