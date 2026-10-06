import io
from app import create_app
from app.extensions import db

def app():
 a=create_app({'TESTING':True,'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:','JWT_SECRET_KEY':'test'}); return a

def test_register_login_protected():
 a=app(); c=a.test_client(); r=c.post('/api/auth/register',json={'name':'Demo','email':'demo@example.com','password':'secret1'}); assert r.status_code==201
 r=c.post('/api/auth/login',json={'email':'demo@example.com','password':'secret1'}); assert r.status_code==200; t=r.json['access_token']; assert c.get('/api/auth/me',headers={'Authorization':'Bearer '+t}).status_code==200

def test_reject_bad_file():
 a=app(); c=a.test_client(); c.post('/api/auth/register',json={'name':'Demo','email':'d@e.com','password':'secret1'}); t=c.post('/api/auth/login',json={'email':'d@e.com','password':'secret1'}).json['access_token']; r=c.post('/api/documents/upload',data={'file':(io.BytesIO(b'x'),'bad.exe')},headers={'Authorization':'Bearer '+t},content_type='multipart/form-data'); assert r.status_code==400
