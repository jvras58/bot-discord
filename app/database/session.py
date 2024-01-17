from config.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(get_settings().DB_URL)


def get_session():
    with Session(engine) as session:
        yield session
