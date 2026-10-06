from pathlib import Path
ALLOWED={'pdf','docx'}
def extension(name): return Path(name).suffix.lower().lstrip('.')
def allowed_file(name): return extension(name) in ALLOWED
