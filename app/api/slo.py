from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core import models, schemas

router = APIRouter(tags=["slo"])

@router.post("/slos", response_model=schemas.SLO)
def create_slo(slo: schemas.SLOCreate, db: Session = Depends(get_db)):
    db_slo = models.SLO(**slo.model_dump())
    db.add(db_slo)
    db.commit()
    db.refresh(db_slo)
    return db_slo

@router.get("/slos", response_model=List[schemas.SLO])
def list_slos(db: Session = Depends(get_db)):
    return db.query(models.SLO).all()

@router.get("/slo/status", response_model=List[schemas.SLOStatus])
def get_slo_status(db: Session = Depends(get_db)):
    slos = db.query(models.SLO).all()
    results = []

    for slo in slos:
        since = datetime.utcnow() - timedelta(days=slo.window_days)
        total_checks = db.query(models.HealthCheck).filter(
            models.HealthCheck.service_id == slo.service_id,
            models.HealthCheck.checked_at >= since
        ).count()

        if total_checks == 0:
            current_availability = 1.0
        else:
            up_checks = db.query(models.HealthCheck).filter(
                models.HealthCheck.service_id == slo.service_id,
                models.HealthCheck.checked_at >= since,
                models.HealthCheck.status == "up"
            ).count()
            current_availability = up_checks / total_checks

        results.append(schemas.SLOStatus(
            service_name=slo.service.name,
            target=slo.target_availability,
            current_availability=current_availability,
            status="healthy" if current_availability >= slo.target_availability else "breaching"
        ))

    return results
