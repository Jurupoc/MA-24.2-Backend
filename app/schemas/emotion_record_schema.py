from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

import datetime
import app.databases.sqlite_database as db

from app.utils.constants import DataBase


class EmotionRecord(db.Base):
    __tablename__ = DataBase.EMOTION_RECORDS_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    intensity = Column(String)
    notes = Column(String)
    emotion = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now)
