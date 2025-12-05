from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .model import Base

class VehiclesDB:
    def __init__(self):
        self.engine = create_engine("sqlite:///./vehicles.db", echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    def get_session(self) -> Session:
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()