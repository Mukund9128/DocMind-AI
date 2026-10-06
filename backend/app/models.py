from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from .extensions import db
class User(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(100),nullable=False); email=db.Column(db.String(150),unique=True,index=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)
 def set_password(self,p): self.password_hash=generate_password_hash(p)
 def check_password(self,p): return check_password_hash(self.password_hash,p)
class Document(db.Model):
 id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False,index=True); original_filename=db.Column(db.String(255),nullable=False); stored_filename=db.Column(db.String(255),nullable=False); file_type=db.Column(db.String(10)); file_size=db.Column(db.Integer); page_count=db.Column(db.Integer,default=0); processing_status=db.Column(db.String(30),default='ready'); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class DocumentChunk(db.Model):
 id=db.Column(db.Integer,primary_key=True); document_id=db.Column(db.Integer,db.ForeignKey('document.id',ondelete='CASCADE'),nullable=False,index=True); page_number=db.Column(db.Integer); chunk_index=db.Column(db.Integer); content=db.Column(db.Text,nullable=False)
class Chat(db.Model):
 id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False,index=True); title=db.Column(db.String(200),default='Document Chat'); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Message(db.Model):
 id=db.Column(db.Integer,primary_key=True); chat_id=db.Column(db.Integer,db.ForeignKey('chat.id',ondelete='CASCADE'),nullable=False,index=True); role=db.Column(db.String(20),nullable=False); content=db.Column(db.Text,nullable=False); sources_json=db.Column(db.Text); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Summary(db.Model):
 id=db.Column(db.Integer,primary_key=True); document_id=db.Column(db.Integer,db.ForeignKey('document.id',ondelete='CASCADE'),nullable=False,index=True); summary_type=db.Column(db.String(30),nullable=False); content=db.Column(db.Text,nullable=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)
