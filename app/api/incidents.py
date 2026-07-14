from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.core import models, schemas

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=schemas.Incident)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    db_incident = models.Incident(**incident.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/", response_model=List[schemas.Incident])
def list_incidents(status: str = None, service_id: UUID = None, db: Session = Depends(get_db)):
    query = db.query(models.Incident)
    if status:
        query = query.filter(models.Incident.status == status)
    if service_id:
        query = query.filter(models.Incident.service_id == service_id)
    return query.all()

@router.patch("/{incident_id}", response_model=schemas.Incident)
def update_incident(incident_id: UUID, incident: schemas.IncidentUpdate, db: Session = Depends(get_db)):
    db_incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    update_data = incident.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_incident, key, value)

    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.post("/{incident_id}/resolve", response_model=schemas.Incident)
def resolve_incident(incident_id: UUID, db: Session = Depends(get_db)):
    db_incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    db_incident.status = "resolved"
    db_incident.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(db_incident)
    return db_incident
