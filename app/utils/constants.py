from fastapi import HTTPException
from http import HTTPStatus


class Errors:
    USER_NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    EMAIL_ALREADY_EXISTS = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists")
    INVALID_PARAMS = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid params")

    REPORT_NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Emotion report not found")


class Messages:
    USER_DELETE = {"message": "Used deleted"}


class DataBase:
    DATABASE_URL = "sqlite:///./ma.db"
    EMOTION_RECORDS_TABLE_NAME = "emotion_records"
    USER_TABLE_NAME = "users"
