from sqlalchemy import Column, Integer, String, Boolean
import app.databases.sqlite_database as db

from app.utils.constants import DataBase


class User(db.Base):
    __tablename__ = DataBase.USER_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    disabled = Column(Boolean, nullable=False)
    hashed_password = Column(String, nullable=False)
