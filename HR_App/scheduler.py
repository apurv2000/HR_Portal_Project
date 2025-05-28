from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import send_weekly_logs
from apscheduler.executors.pool import ThreadPoolExecutor

executors = {
    'default': ThreadPoolExecutor(1),
}

job_defaults = {
    'coalesce': True,       # Run only the most recent missed job
    'misfire_grace_time': 3600,  # Allow running if missed by ≤ 1 hour
}
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_weekly_logs,
        trigger='cron',
        day_of_week='wed',
        hour=13,
        minute=00,
        id='weekly_log_email_job',
        replace_existing=True,
    )
    scheduler.start()
