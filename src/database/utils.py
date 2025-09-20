from contextlib import contextmanager
from src.models import SessionLocal

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

