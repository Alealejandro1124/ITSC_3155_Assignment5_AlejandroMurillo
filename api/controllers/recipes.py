# api/controllers/recipes.py

from fastapi import Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import models, schemas

def create(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    qs = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Recipe not found")
    qs.update(recipe.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return qs.first()

def delete(db: Session, recipe_id: int):
    qs = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not qs.first():
        raise HTTPException(status_code=404, detail="Recipe not found")
    qs.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)