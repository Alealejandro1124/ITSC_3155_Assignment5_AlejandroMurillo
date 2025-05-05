# api/controllers/sandwiches.py

from fastapi import Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import models, schemas

def create(db: Session, sandwich: schemas.SandwichCreate):
    db_sandwich = models.Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def read_all(db: Session):
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()

def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    qs = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")
    qs.update(sandwich.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return qs.first()

def delete(db: Session, sandwich_id: int):
    qs = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")
    qs.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
