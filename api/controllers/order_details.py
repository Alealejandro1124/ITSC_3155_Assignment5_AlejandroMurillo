# api/controllers/order_details.py

from fastapi import Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import models, schemas

def create(db: Session, order_detail: schemas.OrderDetailCreate):
    db_order_detail = models.OrderDetail(**order_detail.dict())
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def read_all(db: Session):
    return db.query(models.OrderDetail).all()

def read_one(db: Session, order_detail_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()

def update(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    qs = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Order detail not found")
    qs.update(order_detail.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return qs.first()

def delete(db: Session, order_detail_id: int):
    qs = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Order detail not found")
    qs.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
