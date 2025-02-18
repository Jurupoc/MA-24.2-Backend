from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.crud import emotion_crud

import app.models.emotion_model as emotion_model
import app.models.emotion_record_model as emotion_record_model

from app.models.user_model import UserInDB

from app.databases.sqlite_database import get_db

from app.utils.constants import Errors, Role
from app.utils.logger import logger

from app.routers.authentication import get_current_active_user

router = APIRouter(
    prefix="/emotion",
    tags=["emotions"],
)


@router.post("/", response_model=emotion_model.Emotion)
def create_emotion(
        emotion: emotion_model.Emotion,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug("call to create a new emotion")

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION
    
    response = emotion_crud.create_emotion(db, emotion, current_user.id)
    if response is None:
        raise Errors.INVALID_PARAMS

    return response


@router.get("/{emotion_id}", response_model=emotion_record_model.AllEmotionReportsResponse)
def get_emotion_by_id(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        emotion_id: int,
        db: Session = Depends(get_db),
):
    logger.debug("call to get an emotion by its id: %s", emotion_id)

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION
    
    response = emotion_crud.get_emotion_by_id(db, emotion_id, current_user.id)
    if response is None:
        logger.error(f"no emotion report found for this id: ", emotion_id)
        raise Errors.REPORT_NOT_FOUND
    
    return {"reports": response}


@router.get("/", response_model=emotion_model.EmotionsResponse)
def get_all_emotions(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug("call to get all emotions")

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION

    response = emotion_crud.get_all_emotions(db, current_user.id)
    if response is None:
        logger.error(f"no emotions found in the database")
        raise Errors.REPORT_NOT_FOUND
    
    return {"emotions": response}


@router.put("/{emotion_id}", response_model=emotion_model.Emotion)
def update_emotion_by_id(
        emotion_id: int,
        emotion_update: dict,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug(f"Call to update emotion by id: {emotion_id}")

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION

    updated_emotion = emotion_crud.update_emotion(db, emotion_id, emotion_update, current_user.id)
    if updated_emotion is None:
        logger.error(f"Failed to update emotion with name: {emotion_id}")
        raise Errors.INVALID_PARAMS

    return updated_emotion


@router.delete("/{emotion_id}")
def delete_emotion(
        emotion_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug(f"Call to delete emotion by ID: {emotion_id}")

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION

    success = emotion_crud.delete_emotion(db, emotion_id, current_user.id)
    if not success:
        raise Errors.REPORT_NOT_FOUND

    return {"message": f"Emotion with ID {emotion_id} was deleted successfully."}