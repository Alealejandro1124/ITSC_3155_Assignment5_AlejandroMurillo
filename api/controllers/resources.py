# api/controllers/resources.py

from fastapi import Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import models, schemas

def create(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    qs = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Resource not found")
    qs.update(resource.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return qs.first()

def delete(db: Session, resource_id: int):
    qs = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Resource not found")
    qs.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
