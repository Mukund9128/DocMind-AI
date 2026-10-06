import os
from pathlib import Path
class Config:
    BASE_DIR=Path(__file__).resolve().parents[1]
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL','sqlite:///docmind.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY','dev-change-me')
    MAX_CONTENT_LENGTH=int(os.getenv('MAX_UPLOAD_MB','15'))*1024*1024
    UPLOAD_FOLDER=str(BASE_DIR/'uploads')
    VECTOR_FOLDER=str(BASE_DIR/'vector_store')
    LLM_API_KEY=os.getenv('LLM_API_KEY','')
    LLM_MODEL=os.getenv('LLM_MODEL','gpt-4.1-mini')
    LLM_BASE_URL=os.getenv('LLM_BASE_URL','https://api.openai.com/v1')
