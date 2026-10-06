from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from .config import Config
from .extensions import db,jwt

def create_app(test_config=None):
    load_dotenv(Path(__file__).resolve().parents[1]/'.env')
    app=Flask(__name__); app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True,exist_ok=True); Path(app.config['VECTOR_FOLDER']).mkdir(parents=True,exist_ok=True)
    db.init_app(app); jwt.init_app(app); CORS(app,resources={r'/api/*':{'origins':'*'}})
    from .routes.auth import bp as auth; from .routes.documents import bp as docs; from .routes.ai import bp as ai; from .routes.chats import bp as chats; from .routes.dashboard import bp as dash
    for b in (auth,docs,ai,chats,dash): app.register_blueprint(b)
    with app.app_context(): db.create_all()
    @app.get('/api/health')
    def health(): return jsonify(status='ok')
    return app
