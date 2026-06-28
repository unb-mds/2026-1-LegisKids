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
    """Inicia o BackgroundScheduler com o job de sync da Câmara (diário ao meio-dia)."""
    global _scheduler

    sync_hour = int(os.getenv("CAMARA_SYNC_HOUR", "12"))
    sync_minute = int(os.getenv("CAMARA_SYNC_MINUTE", "0"))

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        func=_run_sync_job,
        args=[app],
        trigger="cron",
        hour=sync_hour,
        minute=sync_minute,
        id="camara_sync",
        coalesce=True,
        misfire_grace_time=300,
    )
    _scheduler.start()
    logger.info("Scheduler iniciado: sync diário às %02d:%02d.", sync_hour, sync_minute)


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler encerrado.")
