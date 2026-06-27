import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def _run_sync_job(app):
    from src.backend.services.camara_service import CamaraService
    with app.app_context():
        CamaraService().run_sync()


def start_scheduler(app) -> None:
    """Inicia o BackgroundScheduler com o job de sync da Câmara."""
    global _scheduler

    interval_minutes = int(os.getenv("CAMARA_SYNC_INTERVAL_MINUTES", "60"))

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        func=_run_sync_job,
        args=[app],
        trigger="interval",
        minutes=interval_minutes,
        id="camara_sync",
        coalesce=True,
        misfire_grace_time=300,
    )
    _scheduler.start()
    logger.info("Scheduler iniciado: sync a cada %d minuto(s).", interval_minutes)


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler encerrado.")
