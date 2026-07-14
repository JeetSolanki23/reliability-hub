from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime, timedelta
import requests
import time
from app.core.database import get_db
from app.core import models, schemas

router = APIRouter(prefix="/services", tags=["health"])

def perform_health_check(url: str):
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        latency = int((time.time() - start_time) * 1000)
        status = "up" if response.status_code < 400 else "down"
        return status, latency, response.status_code
    except requests.RequestException:
        latency = int((time.time() - start_time) * 1000)
        return "down", latency, None

@router.post("/{service_id}/checks/run", response_model=schemas.HealthCheck)
def run_health_check(service_id: UUID, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    status, latency, code = perform_health_check(db_service.endpoint_url)

    check = models.HealthCheck(
        service_id=service_id,
        status=status,
        latency_ms=latency,
        response_code=code
    )
    db.add(check)
    db.commit()
    db.refresh(check)
    return check

@router.get("/{service_id}/checks", response_model=List[schemas.HealthCheck])
def get_health_checks(service_id: UUID, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.HealthCheck).filter(models.HealthCheck.service_id == service_id).order_by(models.HealthCheck.checked_at.desc()).limit(limit).all()

@router.get("/{service_id}/history")
def get_service_history(service_id: UUID, days: int = 7, db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    checks = db.query(models.HealthCheck).filter(
        models.HealthCheck.service_id == service_id,
        models.HealthCheck.checked_at >= since
    ).all()
    return checks
