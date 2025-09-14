from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Use ONE consistent database file for your project
DATABASE_URL = "sqlite:///./app.db"  # Or "sqlite:///./documents.db" (pick one and use everywhere)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filetype = Column(String)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    extracted_text = Column(Text)

# Create the table (only if it doesn't exist)
Base.metadata.create_all(bind=engine)
