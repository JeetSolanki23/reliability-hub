from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core import models, schemas

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/", response_model=List[schemas.Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = db.query(models.Service).offset(skip).limit(limit).all()
    return services

@router.get("/{service_id}", response_model=schemas.Service)
def read_service(service_id: UUID, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@router.patch("/{service_id}", response_model=schemas.Service)
def update_service(service_id: UUID, service: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = service.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/{service_id}")
def delete_service(service_id: UUID, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(db_service)
    db.commit()
    return {"message": "Service deleted"}
