# app/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine("sqlite:///conversations.db")
Session = sessionmaker(bind=engine)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_text = Column(String)
    ai_reply = Column(String)
    language = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)

def save_conversation(user_text, ai_reply, language="en"):
    session = Session()
    conv = Conversation(user_text=user_text, ai_reply=ai_reply, language=language)
    session.add(conv)
    session.commit()
    session.close()
