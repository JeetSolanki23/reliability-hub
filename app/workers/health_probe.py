import logging
from app.core.database import SessionLocal
from app.core import models
from app.api.health import perform_health_check
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_probes():
    db = SessionLocal()
    try:
        services = db.query(models.Service).all()
        for service in services:
            logger.info(f"Probing service: {service.name} at {service.endpoint_url}")
            status, latency, code = perform_health_check(service.endpoint_url)

            check = models.HealthCheck(
                service_id=service.id,
                status=status,
                latency_ms=latency,
                response_code=code
            )
            db.add(check)

            # Auto-incident creation logic
            if status == "down":
                # Check if there is an existing open incident
                existing_incident = db.query(models.Incident).filter(
                    models.Incident.service_id == service.id,
                    models.Incident.status != "resolved"
                ).first()

                if not existing_incident:
                    logger.warning(f"Service {service.name} is DOWN. Creating incident.")
                    incident = models.Incident(
                        service_id=service.id,
                        title=f"Service {service.name} is DOWN",
                        severity="sev2",
                        status="open"
                    )
                    db.add(incident)

            db.commit()
    except Exception as e:
        logger.error(f"Error during probes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # For demonstration, we run every 60 seconds
    # In a more advanced setup, we would respect service.check_interval_seconds
    scheduler.add_job(run_probes, 'interval', seconds=60)
    logger.info("Starting background worker...")
    # Run once at startup
    run_probes()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
