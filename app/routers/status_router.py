from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import StatusCreateUpdate, StatusDetail
from app.services import StatusService


router = APIRouter(prefix="/statuses", tags=["statuses"])


@router.get("", response_model=list[StatusDetail])
def get_statuses(db: Session = Depends(get_db)):
    return StatusService(db).list()


@router.post("", response_model=StatusDetail, status_code=status.HTTP_201_CREATED)
def create_status(init: StatusCreateUpdate, db: Session = Depends(get_db)):
    try:
        return StatusService(db).create(init)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Status with name = {init.name} already exists")


@router.put("/{status_id}", response_model=StatusDetail)
def update_status(status_id: int, init: StatusCreateUpdate, db: Session = Depends(get_db)):
    try:
        updated = StatusService(db).update(status_id, init)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Status with name = {init.name} already exists")

    if updated is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Status with id = {status_id} not found")

    return updated


@router.get("/{status_id}", response_model=StatusDetail)
def get_status(status_id: int, db: Session = Depends(get_db)):
    found = StatusService(db).retrieve(status_id)
    if found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Status with id = {status_id} not found")

    return found


@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status(status_id: int, db: Session = Depends(get_db)):
    try:
        deleted = StatusService(db).delete(status_id)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Status is used by tasks")

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Status with id = {status_id} not found")
