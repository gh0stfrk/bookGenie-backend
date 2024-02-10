import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///ip_logs.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class IPLog(Base):
    __tablename__ = "ip_logs"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True)
    request_count = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)  


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
